from dataclasses import dataclass

import pandas as pd

from data_loader import (DEFAULT_MAX_NOTES, DataError, clean, downsample,
                         normalize, split_trend)

# --- Musical constants ---
TICKS_PER_BEAT = 480            # MIDI time resolution
BASE_NOTE = 48                  # C3, the lowest note of the melody
OCTAVES = 2                     # melody range in octaves
MAX_COLUMNS = 4                 # how many columns take part in the mapping

# Note durations in beats
DURATIONS_BEATS = [2.0, 1.0, 0.5, 0.25]

VELOCITY_MIN, VELOCITY_MAX = 40, 110
PAN_MIN, PAN_MAX = 10, 117      # avoid extreme left/right
TEMPO_MIN_BPM, TEMPO_MAX_BPM = 80, 140

# Scales as semitone offsets from the root note
SCALES = {
    "Pentatonic": [0, 2, 4, 7, 9],
    "Major":      [0, 2, 4, 5, 7, 9, 11],
    "Minor":      [0, 2, 3, 5, 7, 8, 10],
}
DEFAULT_SCALE = "Pentatonic"


@dataclass(frozen=True)
class Note:
    pitch: int            # 0..127
    duration: int         # in ticks
    velocity: int         # 0..127
    pan: int              # 0..127 (CC10)
    tempo_bpm: int        # tempo at the moment of this note


# ------------------------------------------------- single-value converters
def to_pitch(norm: float, scale_name: str = DEFAULT_SCALE,
             base: int = BASE_NOTE, octaves: int = OCTAVES) -> int:
    scale = SCALES[scale_name]
    steps = len(scale) * octaves
    index = round(norm * (steps - 1))
    pitch = base + 12 * (index // len(scale)) + scale[index % len(scale)]
    return max(0, min(127, pitch))


def to_duration(norm: float) -> int:
    index = round(norm * (len(DURATIONS_BEATS) - 1))
    return int(DURATIONS_BEATS[index] * TICKS_PER_BEAT)


def to_velocity(norm: float) -> int:
    return int(VELOCITY_MIN + norm * (VELOCITY_MAX - VELOCITY_MIN))


def to_pan(norm: float) -> int:
    return int(PAN_MIN + norm * (PAN_MAX - PAN_MIN))


def to_tempo(norm: float) -> int:
    return int(TEMPO_MIN_BPM + norm * (TEMPO_MAX_BPM - TEMPO_MIN_BPM))


# ------------------------------------------------------------ whole table
def build_notes(df: pd.DataFrame, scale_name: str = DEFAULT_SCALE,
                max_notes: int = DEFAULT_MAX_NOTES) -> list[Note]:
    if df.shape[1] < 2:
        raise DataError("At least two numeric columns are required.")
    if scale_name not in SCALES:
        raise DataError(f"Unknown scale: {scale_name}")

    data = downsample(df.iloc[:, :MAX_COLUMNS].apply(clean), max_notes)
    cols = [data[c] for c in data.columns]

    trend, fluctuation = split_trend(cols[0])
    pitch_n = normalize(fluctuation)
    tempo_n = normalize(trend)
    duration_n = normalize(cols[1])
    velocity_n = normalize(cols[2] if len(cols) > 2 else cols[1])
    pan_n = normalize(cols[3]) if len(cols) > 3 else None

    notes = []
    for i in range(len(data)):
        notes.append(Note(
            pitch=to_pitch(pitch_n.iloc[i], scale_name),
            duration=to_duration(duration_n.iloc[i]),
            velocity=to_velocity(velocity_n.iloc[i]),
            pan=to_pan(pan_n.iloc[i]) if pan_n is not None else 64,
            tempo_bpm=to_tempo(tempo_n.iloc[i]),
        ))
    return notes