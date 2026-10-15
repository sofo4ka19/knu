# --- Time grid ---
TICKS_PER_BEAT = 480
BEATS_PER_BAR = 4
BAR_TICKS = TICKS_PER_BEAT * BEATS_PER_BAR

# --- Range of the melody ---
BASE_NOTE = 48                  # C3, the lowest note of the melody
OCTAVES = 2

# --- Chords ---
# C = 0, D = 2, E = 4, F = 5, G = 7, A = 9, B = 11.
MAJOR_CHORDS = [
    (36, [0, 4, 7]),            # C
    (33, [9, 0, 4]),            # Am
    (41, [5, 9, 0]),            # F
    (43, [7, 11, 2]),           # G
]
MINOR_CHORDS = [
    (36, [0, 3, 7]),            # Cm
    (32, [8, 0, 3]),            # Ab
    (39, [3, 7, 10]),           # Eb
    (34, [10, 2, 5]),           # Bb
]
DOMINANT = (43, [7, 11, 2])     # G, played before the last note


def dominant_start(final_start, approach_start):
    """Time (in ticks) when the dominant chord starts.

    It starts at the last bar line before the final note, or together with
    the approach to the final note if that starts earlier.
    """
    last_bar_start = (final_start - 1) // BAR_TICKS * BAR_TICKS
    return min(last_bar_start, approach_start)


class Scale:

    def __init__(self, notes, chords, max_step, endings):
        self.notes = notes              # semitones from the root note
        self.chords = chords            # the chords the bass plays in a loop
        self.max_step = max_step        # largest jump of the melody between two notes
        self.endings = endings          # how the melody comes to the last note
        self.tonic = len(notes)         # step of the tonic (C4)
        self.top = len(notes) * OCTAVES - 1     # step of the highest note

    def pitch(self, step):
        """Scale step to MIDI format"""
        octave = step // len(self.notes)
        degree = step % len(self.notes)
        return BASE_NOTE + 12 * octave + self.notes[degree]

    def pitch_class(self, step):
        """The note without its octave (C = 0 ... B = 11)."""
        return self.pitch(step) % 12

    def chord_at(self, position, final_start, approach_start):
        """Chord that sounds at a moment (in ticks)."""
        if position >= final_start:
            return self.chords[0]
        if position >= dominant_start(final_start, approach_start):
            return DOMINANT
        return self.chords[(position // BAR_TICKS) % len(self.chords)]

    def bass_plan(self, final_start, total_ticks, approach_start):
        """List of bass chords for the whole piece."""
        start = dominant_start(final_start, approach_start)
        plan = []
        position = 0
        while position < start:
            length = min(BAR_TICKS, start - position)
            chord = self.chords[(position // BAR_TICKS) % len(self.chords)]
            plan.append((chord[0], length))
            position += length
        plan.append((DOMINANT[0], final_start - start))
        plan.append((self.chords[0][0], total_ticks - final_start))
        return plan


SCALES = {
    "Pentatonic": Scale([0, 2, 4, 7, 9], MAJOR_CHORDS, 3, {
        "rising_calm": [-2, -1], "rising_energetic": [-3, -1],
        "falling_calm": [2, 1], "falling_energetic": [3, 1]}),
    "Major": Scale([0, 2, 4, 5, 7, 9, 11], MAJOR_CHORDS, 4, {
        "rising_calm": [-2, -1], "rising_energetic": [-3, -1],
        "falling_calm": [2, 1], "falling_energetic": [4, 1]}),
    "Minor": Scale([0, 2, 3, 5, 7, 8, 10], MINOR_CHORDS, 4, {
        "rising_calm": [-3, -1], "rising_energetic": [-4, -1],
        "falling_calm": [2, 1], "falling_energetic": [4, 1]}),
}
DEFAULT_SCALE_NAME = "Pentatonic"