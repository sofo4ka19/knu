"""mapping.py: the rules that turn the prepared data into notes.

The first four columns of the table are used:
    column 1  -> pitch (a high value gives a high note); a big change between
                 two points gives a rhythmic figure; the way the data end
                 decides how the melody ends; the slow trend changes the loudness
    column 2  -> length of the notes (and the loudness, if there is no column 3)
    column 3  -> loudness (velocity)
    column 4  -> pan (left / right)

Every column is turned into ranks (0..1) first, so the units of the data do not
matter. The melody is made to sound like music: it starts and ends on the tonic,
follows the chords of the bass and keeps a steady rhythm.
"""
from dataclasses import dataclass

from data_loader import DataError
from harmony import TICKS_PER_BEAT

# --- Columns and smoothing ---
MAX_COLUMNS = 4                 # how many columns are used
SMOOTH_WINDOW = 3               # smoothing of column 1 before the melody is made
DURATION_SMOOTH_WINDOW = 5      # smoothing of column 2, so the rhythm changes in phrases
TREND_FRACTION = 0.1            # the trend window is 10% of the series

# --- Rhythm ---
STRONG_BEAT_TICKS = 2 * TICKS_PER_BEAT      # beats 1 and 3 of a bar
# Note lengths: (upper rank limit, length in beats). A high rank gives a short note.
DURATION_LEVELS = [(0.15, 2.0), (0.65, 1.0), (1.0, 0.5)]

# --- Ending ---
CADENCE_NOTES = 3               # the last three notes form the ending
FINAL_NOTE_BEATS = 4.0          # the last note is always the tonic and lasts a whole bar
ENDING_LOOKBACK = 4             # how many points before the ending are examined
ENERGETIC_RANK = 0.5            # the mean rank of the changes above this = large changes

# --- Rhythmic figures (a note is replaced by 3 or 4 fast notes) ---
RUN_ACCENT = 0.90               # change rank for 4 fast notes
TRIPLET_ACCENT = 0.80           # change rank for a triplet
FIGURE_MIN_GAP = 6              # minimum number of notes between two figures

# --- Loudness and pan ---
VELOCITY_MIN, VELOCITY_MAX = 40, 110
PAN_MIN, PAN_MAX = 10, 117


@dataclass
class Note:
    pitch: int                  # MIDI note number
    duration: int               # in ticks
    velocity: int               # loudness, 0..127
    pan: int                    # 0..127
    point: int                  # the data point this note comes from


# ------------------------------------------------------ small helpers
def moving_average(series, window):
    """Average of every value with its neighbours (smooths the series)."""
    return series.rolling(window, center=True, min_periods=1).mean()


def normalize(series):
    return (series.rank() - 1) / (len(series) - 1)


def to_duration(rank):
    """Length of a note in ticks (a high rank gives a short note)."""
    for upper_limit, beats in DURATION_LEVELS:
        if rank <= upper_limit:
            return int(beats * TICKS_PER_BEAT)


def to_velocity(rank):
    """Loudness of a note: a high rank gives a loud note."""
    return int(VELOCITY_MIN + rank * (VELOCITY_MAX - VELOCITY_MIN))


def to_pan(rank):
    return int(PAN_MIN + rank * (PAN_MAX - PAN_MIN))


# ------------------------------------------------------------ rhythm
def align_rhythm(durations):
    """Make the rhythm steady by keeping the notes on the beat.

    * A note that starts between two beats is shortened to end on the beat,
      so short notes always come in pairs.
    * A 2-beat note can only start on beat 1 or 3.
    * The last note starts on a beat; if the previous note ends between two
      beats, it is made longer up to the beat.
    """
    aligned = []
    position = 0
    for duration in durations[:-1]:
        offset = position % TICKS_PER_BEAT
        if offset != 0:
            duration = TICKS_PER_BEAT - offset
        elif duration >= 2 * TICKS_PER_BEAT and position % STRONG_BEAT_TICKS != 0:
            duration = TICKS_PER_BEAT
        aligned.append(duration)
        position += duration

    offset = position % TICKS_PER_BEAT
    if offset != 0:
        aligned[-1] += TICKS_PER_BEAT - offset
    aligned.append(durations[-1])
    return aligned


def make_durations(column):
    """Length of every note, made from column 2."""
    ranks = normalize(moving_average(column, DURATION_SMOOTH_WINDOW))
    durations = [to_duration(rank) for rank in ranks]
    durations[-1] = int(FINAL_NOTE_BEATS * TICKS_PER_BEAT)
    return align_rhythm(durations)


def note_positions(durations):
    """Start time (in ticks) of every note."""
    positions = []
    time = 0
    for duration in durations:
        positions.append(time)
        time += duration
    return positions


# ------------------------------------------------------------ melody
def classify_ending(change, change_ranks):
    """Say how the data end: rising or falling, small or large changes. Used for correct ending generation."""
    start = len(change) - CADENCE_NOTES
    window = slice(max(1, start - ENDING_LOOKBACK), start)
    if change.iloc[window].sum() >= 0:
        direction = "rising"
    else:
        direction = "falling"
    if change_ranks.iloc[window].mean() > ENERGETIC_RANK:
        energy = "energetic"
    else:
        energy = "calm"
    return direction + "_" + energy


def snap_to_chord(scale, step, previous, direction, chord_notes):
    """Move a note to the nearest note of the chord, if one is close enough.

    The move must not make the jump from the previous note bigger than
    scale.max_step, so snapping never creates a big leap.
    """
    if scale.pitch_class(step) in chord_notes:
        return step
    for distance in range(1, scale.max_step + 1):
        # try first the side the melody is moving to
        for candidate in (step + direction * distance, step - direction * distance):
            if (0 <= candidate <= scale.top
                    and abs(candidate - previous) <= scale.max_step
                    and scale.pitch_class(candidate) in chord_notes):
                return candidate
    return step


def make_melody(ranks, positions, scale, ending):
    """Scale step of every note. The melody follows the value of the data.

    The wanted step is the rank of the value spread over the whole range.
    The melody moves towards it by at most scale.max_step steps per note.
    It starts on the tonic, keeps to the chord notes on beats 1 and 3 and
    after big jumps, and comes to the ending in the last notes.
    """
    n = len(ranks)
    cadence_start = n - CADENCE_NOTES
    final_start = positions[-1]
    approach_start = positions[cadence_start]
    target = scale.tonic + ending[0]

    step = scale.tonic
    melody = [step]
    for i in range(1, n):
        if i >= cadence_start:
            melody.append(scale.tonic + ending[i - cadence_start])
            continue

        wanted = round(ranks.iloc[i] * scale.top)
        move = max(-scale.max_step, min(scale.max_step, wanted - step))
        direction = 1 if wanted >= step else -1
        step += move

        if positions[i] % STRONG_BEAT_TICKS == 0 or abs(move) >= 2:
            chord = scale.chord_at(positions[i], final_start, approach_start)
            step = snap_to_chord(scale, step, melody[-1], direction, chord[1])

        # stay close enough to the ending to reach it in time
        steps_left = cadence_start - i
        step = max(target - scale.max_step * steps_left,
                   min(target + scale.max_step * steps_left, step))
        step = max(0, min(scale.top, step))
        melody.append(step)
    return melody


def make_figure(melody, i, direction, count, top):
    """Scale steps of a figure (3 or 4 fast notes) that leads into note i.

    The figure starts at most one step away from the previous note, so it
    does not add a big leap to the melody.
    """
    previous = melody[i - 1]
    if melody[i] != previous:
        direction = 1 if melody[i] > previous else -1
    start = melody[i] - direction * (count - 1)
    start = max(previous - 1, min(previous + 1, start))

    steps = []
    for k in range(count):
        step = round(start + (melody[i] - start) * k / (count - 1))
        steps.append(max(0, min(top, step)))
    return steps


# ------------------------------------------------------------ notes
def build_notes(df, scale):
    """Main function to turn the table made by load_csv() into a list of notes."""
    if df.shape[1] < 2:
        raise DataError("At least two numeric columns are required.")
    cols = [df.iloc[:, i] for i in range(min(df.shape[1], MAX_COLUMNS))]
    n = len(df)

    # 1. Rhythm
    durations = make_durations(cols[1])
    positions = note_positions(durations)

    # 2. Melody from column 1
    smooth = moving_average(cols[0], SMOOTH_WINDOW)
    change = smooth.diff().fillna(0)
    change_ranks = normalize(change.abs())
    ending = scale.endings[classify_ending(change, change_ranks)] + [0]
    melody = make_melody(normalize(smooth), positions, scale, ending)

    # 3. Loudness and pan.
    velocity_ranks = normalize(cols[2] if len(cols) > 2 else cols[1])
    pan_ranks = normalize(cols[3]) if len(cols) > 3 else None

    # 4. One note per data point; a big change on a weak beat becomes a figure.
    notes = []
    cadence_start = n - CADENCE_NOTES
    last_figure = -FIGURE_MIN_GAP
    for i in range(n):
        velocity = to_velocity(velocity_ranks.iloc[i])
        pan = to_pan(pan_ranks.iloc[i]) if pan_ranks is not None else 64

        on_weak_beat = (positions[i] % TICKS_PER_BEAT == 0
                        and positions[i] % STRONG_BEAT_TICKS != 0)
        figure_allowed = (0 < i < cadence_start
                          and durations[i] == TICKS_PER_BEAT
                          and on_weak_beat
                          and i - last_figure >= FIGURE_MIN_GAP)
        accent = change_ranks.iloc[i]

        if figure_allowed and accent >= TRIPLET_ACCENT:
            count = 4 if accent >= RUN_ACCENT else 3
            direction = 1 if change.iloc[i] >= 0 else -1
            for step in make_figure(melody, i, direction, count, scale.top):
                notes.append(Note(scale.pitch(step), TICKS_PER_BEAT // count,
                                  velocity, pan, i))
            last_figure = i
        else:
            notes.append(Note(scale.pitch(melody[i]), durations[i],
                              velocity, pan, i))
    return notes


# ------------------------------------------------------------ for the window
def point_start_ticks(notes):
    """Time (in ticks) when the music of every data point starts."""
    starts = {}
    time = 0
    for note in notes:
        starts.setdefault(note.point, time)
        time += note.duration
    return [starts[i] for i in range(notes[-1].point + 1)]


def pitch_per_point(notes):
    """MIDI note the melody has reached at every data point (its last note)."""
    last = {}
    for note in notes:
        last[note.point] = note.pitch
    return [last[i] for i in range(notes[-1].point + 1)]