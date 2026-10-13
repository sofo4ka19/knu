"""mapping.py: rules that turn data values into MIDI parameters.

Fixed mapping by column order (the first four numeric columns are used):

    column 1  change between neighbouring values -> melody movement:
                  direction of change -> direction of the melody (up/down)
                  size of change      -> interval size (1..max step in the scale)
                  very large change   -> a rhythmic figure (triplet / fast run)
              trend -> dynamics (slow crescendo / decrescendo over the piece)
    column 2  -> duration (smoothed, then 3 levels: long / medium / short)
              -> velocity (higher value = louder note)
    column 3  -> velocity (replaces column 2 for velocity, if present)
    column 4  -> pan, MIDI CC10 (left/right position)

With only two columns, every column still affects at least one MIDI
parameter, as required by the lab assignment. Tempo is a constant
performance setting, it does not change during the piece.

Musical rules (independent of the data):
    * the melody starts on the tonic and ends with the cadence E - D - C
      and a long tonic note lasting one full bar;
    * on strong beats (1 and 3) the melody snaps to a tone of the current
      chord, so it fits the bass harmony;
    * after a large leap the melody calms down with a one-step move;
    * rhythm is aligned to the beat: short notes come in pairs and long notes
      never start off the beat;
    * rhythmic figures appear only on weak beats, never close to each other.

All values are converted to relative ranks (0..1), so the rules work
for any data set.
"""
from dataclasses import dataclass

import pandas as pd

from data_loader import (DEFAULT_MAX_NOTES, DataError, clean, downsample,
                         normalize, split_trend)
from harmony import TICKS_PER_BEAT, chord_at

# --- Musical constants ---
BASE_NOTE = 48                  # C3, the lowest note of the melody
OCTAVES = 2                     # melody range in octaves
MAX_COLUMNS = 4                 # how many columns take part in the mapping
SMOOTH_WINDOW = 3               # light smoothing before measuring changes

# Largest melodic interval in scale steps. The pentatonic scale has bigger
# gaps between its notes, so it gets a smaller limit.
MAX_STEP_BY_SCALE = {"Pentatonic": 2, "Major": 3, "Minor": 3}

STRONG_BEAT_TICKS = 2 * TICKS_PER_BEAT   # beats 1 and 3 of a bar
SNAP_DISTANCE = 2                        # how far a note may move to reach a chord tone

# Duration levels: (upper rank limit, length in beats).
# Rank 0..0.15 -> long, 0.15..0.65 -> medium, 0.65..1 -> short.
DURATION_LEVELS = [(0.15, 2.0), (0.65, 1.0), (1.0, 0.5)]
DURATION_SMOOTH_WINDOW = 5      # rhythm changes in phrases, not on every note

# Ending: three cadence notes (E - D - C) and their lengths in beats.
CADENCE_OFFSETS = [2, 1, 0]     # scale steps above the tonic
CADENCE_BEATS = [1.0, 2.0, 4.0]

# Rhythmic figures: a one-beat note is replaced by faster notes when the
# change in the data is large (rank of |change| above the limit).
RUN_ACCENT = 0.90               # 4 sixteenth notes
TRIPLET_ACCENT = 0.80           # 3 triplet notes
FIGURE_MIN_GAP = 6              # minimum number of notes between two figures

VELOCITY_MIN, VELOCITY_MAX = 40, 110
VELOCITY_TREND_SPAN = 24        # total dynamic swing given by the trend
PAN_MIN, PAN_MAX = 10, 117      # avoid extreme left/right

# Scales as semitone offsets from the root note
SCALES = {
    "Pentatonic": [0, 2, 4, 7, 9],
    "Major":      [0, 2, 4, 5, 7, 9, 11],
    "Minor":      [0, 2, 3, 5, 7, 8, 10],
}
DEFAULT_SCALE = "Pentatonic"


@dataclass(frozen=True)
class Note:
    """One melody note with every parameter already converted to MIDI units."""
    pitch: int            # 0..127
    duration: int         # in ticks
    velocity: int         # 0..127
    pan: int              # 0..127 (CC10)


# ------------------------------------------------- single-value converters
def index_to_pitch(index: int, scale_name: str = DEFAULT_SCALE,
                   base: int = BASE_NOTE) -> int:
    """Convert a scale-step index (0 = lowest note) to a MIDI pitch."""
    scale = SCALES[scale_name]
    pitch = base + 12 * (index // len(scale)) + scale[index % len(scale)]
    return max(0, min(127, pitch))


def to_duration(norm: float) -> int:
    """Map 0..1 to one of the duration levels (higher value = shorter)."""
    for upper, beats in DURATION_LEVELS:
        if norm <= upper:
            return int(beats * TICKS_PER_BEAT)
    return int(DURATION_LEVELS[-1][1] * TICKS_PER_BEAT)


def to_velocity(norm: float, trend_norm: float) -> int:
    """Velocity from the value (40..110) plus a dynamic shift from the trend."""
    base = VELOCITY_MIN + norm * (VELOCITY_MAX - VELOCITY_MIN)
    shift = (trend_norm - 0.5) * VELOCITY_TREND_SPAN
    return max(1, min(127, int(base + shift)))


def to_pan(norm: float) -> int:
    """Map 0..1 linearly to the pan range (CC10)."""
    return int(PAN_MIN + norm * (PAN_MAX - PAN_MIN))


# ---------------------------------------------------------- rhythm helpers
def align_rhythm(durations: list[int]) -> list[int]:
    """Make the rhythm steady by aligning notes to the beat.

    * A note that starts off the beat is shortened to finish the beat,
      so short notes always come in pairs.
    * A 2-beat note may only start on beats 1 and 3 of a bar.
    The cadence notes at the end keep their lengths.
    """
    aligned = []
    position = 0
    free_notes = len(durations) - len(CADENCE_BEATS)
    for i, duration in enumerate(durations):
        offset = position % TICKS_PER_BEAT
        if offset:
            duration = TICKS_PER_BEAT - offset
        elif (i < free_notes and duration >= 2 * TICKS_PER_BEAT
              and position % STRONG_BEAT_TICKS):
            duration = TICKS_PER_BEAT
        aligned.append(duration)
        position += duration
    return aligned


def note_positions(durations: list[int]) -> list[int]:
    """Start time (in ticks) of every note."""
    positions, current = [], 0
    for duration in durations:
        positions.append(current)
        current += duration
    return positions


# ---------------------------------------------------------- melody helpers
def _reflect(index: int, low: int, high: int) -> int:
    """Bounce an index back into [low, high] instead of clipping it."""
    while index < low or index > high:
        if index < low:
            index = 2 * low - index
        if index > high:
            index = 2 * high - index
    return index


def _pitch_class(index: int, scale_name: str) -> int:
    return index_to_pitch(index, scale_name) % 12


def snap_to_chord(index: int, previous: int, direction: int, chord_tones: frozenset,
                  scale_name: str, top: int, max_move: int) -> int:
    """Move to the nearest scale note that belongs to the chord (if close).

    A candidate is accepted only if the total move from the previous note
    stays within `max_move` scale steps, so snapping never creates a leap.
    """
    if _pitch_class(index, scale_name) in chord_tones:
        return index
    for distance in range(1, SNAP_DISTANCE + 1):
        # prefer continuing in the direction the melody is moving
        for candidate in (index + direction * distance, index - direction * distance):
            if (0 <= candidate <= top
                    and abs(candidate - previous) <= max_move
                    and _pitch_class(candidate, scale_name) in chord_tones):
                return candidate
    return index


def melody_indices(change: pd.Series, size_n: pd.Series, positions: list[int],
                   scale_name: str) -> list[int]:
    """Turn changes of a data series into a melody that moves step by step.

    Direction of change -> direction of the melody.
    Size of change (as a rank) -> number of scale steps.
    Starts on the tonic, snaps to chord tones on strong beats, calms down
    after a leap, and is funnelled toward the final cadence.
    """
    n = len(change)
    scale_len = len(SCALES[scale_name])
    max_step = MAX_STEP_BY_SCALE[scale_name]
    top = scale_len * OCTAVES - 1
    tonic = scale_len                          # first note of the 2nd octave (C4)
    cadence_start = n - len(CADENCE_OFFSETS)   # index of the first cadence note
    target = tonic + CADENCE_OFFSETS[0]
    final_start = positions[-1]

    index = tonic
    result = [index]
    for i in range(1, n):
        if i >= cadence_start:
            result.append(tonic + CADENCE_OFFSETS[i - cadence_start])
            continue
        direction = 1 if change.iloc[i] >= 0 else -1
        step = 1 + round(size_n.iloc[i] * (max_step - 1))
        if abs(result[-1] - (result[-2] if len(result) > 1 else result[-1])) >= max_step:
            step = 1                           # leap recovery
        index = _reflect(index + direction * step, 0, top)
        if positions[i] % STRONG_BEAT_TICKS == 0:
            chord = chord_at(positions[i], final_start, scale_name)
            index = snap_to_chord(index, result[-1], direction, chord[1],
                                  scale_name, top, max_step)
        # Funnel: stay close enough to reach the cadence in time
        left = cadence_start - i
        index = max(target - max_step * left, min(target + max_step * left, index))
        index = max(0, min(top, index))
        result.append(index)
    return result


# ------------------------------------------------------------ whole table
def build_notes(df: pd.DataFrame, scale_name: str = DEFAULT_SCALE,
                max_notes: int = DEFAULT_MAX_NOTES) -> list[Note]:
    """Convert a table of numeric columns into a list of Note objects."""
    if df.shape[1] < 2:
        raise DataError("At least two numeric columns are required.")
    if scale_name not in SCALES:
        raise DataError(f"Unknown scale: {scale_name}")

    # Clean and shorten raw values first; normalization comes later,
    # separately for every parameter.
    data = downsample(df.iloc[:, :MAX_COLUMNS].apply(clean), max_notes)
    cols = [data[c] for c in data.columns]
    n = len(data)

    # Rhythm first: melody rules need to know where the strong beats are
    smooth_rhythm = cols[1].rolling(
        DURATION_SMOOTH_WINDOW, center=True, min_periods=1).mean()
    duration_n = normalize(smooth_rhythm)
    durations = [to_duration(duration_n.iloc[i]) for i in range(n)]
    for k, beats in enumerate(CADENCE_BEATS):           # fixed ending rhythm
        durations[n - len(CADENCE_BEATS) + k] = int(beats * TICKS_PER_BEAT)
    durations = align_rhythm(durations)
    positions = note_positions(durations)

    # Melody from changes of column 1
    smooth = cols[0].rolling(SMOOTH_WINDOW, center=True, min_periods=1).mean()
    change = smooth.diff().fillna(0)
    size_n = normalize(change.abs())
    directions = [1 if c >= 0 else -1 for c in change]
    indices = melody_indices(change, size_n, positions, scale_name)

    trend, _ = split_trend(cols[0])
    trend_n = normalize(trend)
    velocity_n = normalize(cols[2] if len(cols) > 2 else cols[1])
    pan_n = normalize(cols[3]) if len(cols) > 3 else None

    scale_len = len(SCALES[scale_name])
    top = scale_len * OCTAVES - 1
    cadence_start = n - len(CADENCE_BEATS)

    notes = []
    last_figure = -FIGURE_MIN_GAP
    for i in range(n):
        velocity = to_velocity(velocity_n.iloc[i], trend_n.iloc[i])
        pan = to_pan(pan_n.iloc[i]) if pan_n is not None else 64

        accent = size_n.iloc[i]
        on_weak_beat = (positions[i] % TICKS_PER_BEAT == 0
                        and positions[i] % STRONG_BEAT_TICKS != 0)
        can_use_figure = (0 < i < cadence_start
                          and durations[i] == TICKS_PER_BEAT
                          and on_weak_beat
                          and i - last_figure >= FIGURE_MIN_GAP)

        if can_use_figure and accent >= TRIPLET_ACCENT:
            count = 4 if accent >= RUN_ACCENT else 3
            length = TICKS_PER_BEAT // count
            # The figure leads into the target note. It starts at most one
            # scale step away from the previous note, so there is no leap.
            previous = indices[i - 1]
            actual = indices[i] - previous
            direction = (1 if actual > 0 else -1) if actual else directions[i]
            start = indices[i] - direction * (count - 1)
            start = max(previous - 1, min(previous + 1, start))
            for k in range(count):
                index = round(start + (indices[i] - start) * k / (count - 1))
                index = max(0, min(top, index))
                notes.append(Note(index_to_pitch(index, scale_name),
                                  length, velocity, pan))
            last_figure = i
        else:
            notes.append(Note(index_to_pitch(indices[i], scale_name),
                              durations[i], velocity, pan))
    return notes