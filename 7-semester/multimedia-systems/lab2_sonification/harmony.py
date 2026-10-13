# --- Time grid ---
TICKS_PER_BEAT = 480
BEATS_PER_BAR = 4
BAR_TICKS = TICKS_PER_BEAT * BEATS_PER_BAR

Chord = tuple[int, frozenset]

# Key of C major: C - Am - F - G
MAJOR_LOOP: list[Chord] = [
    (36, frozenset({0, 4, 7})),     # C
    (33, frozenset({9, 0, 4})),     # Am
    (41, frozenset({5, 9, 0})),     # F
    (43, frozenset({7, 11, 2})),    # G
]
# Key of C minor: Cm - Ab - Eb - Bb
MINOR_LOOP: list[Chord] = [
    (36, frozenset({0, 3, 7})),     # Cm
    (32, frozenset({8, 0, 3})),     # Ab
    (39, frozenset({3, 7, 10})),    # Eb
    (34, frozenset({10, 2, 5})),    # Bb
]
PROGRESSIONS = {
    "Pentatonic": MAJOR_LOOP,
    "Major": MAJOR_LOOP,
    "Minor": MINOR_LOOP,
}
DOMINANT: Chord = (43, frozenset({7, 11, 2}))   # G, played before the final tonic


def _loop(scale_name: str) -> list[Chord]:
    return PROGRESSIONS.get(scale_name, MAJOR_LOOP)


def chord_at(position: int, final_start: int, scale_name: str) -> Chord:
    """Chord that sounds at `position` (in ticks).

    Normal bars loop the progression, the last bar before the final note is
    the dominant, and from `final_start` on the chord is the tonic.
    """
    loop = _loop(scale_name)
    if position >= final_start:
        return loop[0]
    last_bar_start = (final_start - 1) // BAR_TICKS * BAR_TICKS
    if position >= last_bar_start:
        return DOMINANT
    return loop[(position // BAR_TICKS) % len(loop)]


def bass_plan(final_start: int, total_ticks: int, scale_name: str) -> list[tuple]:
    """List of (bass root note, duration in ticks) covering the whole piece."""
    plan = []
    position = 0
    while position < final_start:
        duration = min(BAR_TICKS, final_start - position)
        plan.append((chord_at(position, final_start, scale_name)[0], duration))
        position += duration
    plan.append((_loop(scale_name)[0][0], total_ticks - final_start))
    return plan