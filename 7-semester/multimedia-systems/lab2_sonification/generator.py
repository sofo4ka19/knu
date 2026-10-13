import mido

from harmony import TICKS_PER_BEAT, bass_plan
from mapping import Note

# --- Constants ---
MELODY_CHANNEL = 0
BASS_CHANNEL = 1
GATE = 0.9              # a note sounds for 90% of its slot, the rest is a tiny gap
BASS_VELOCITY = 70
PAN_CC = 10             # MIDI controller number for panning
DEFAULT_TEMPO_BPM = 100

INSTRUMENTS = {
    "Piano": 0,
    "Vibraphone": 11,
    "Acoustic Guitar": 24,
    "Flute": 73,
    "Strings": 48,
}
DEFAULT_MELODY = "Piano"
BASS_PROGRAM = 32


def generate_midi(notes: list[Note], path: str, scale_name: str = "Pentatonic",
                  melody_instrument: str = DEFAULT_MELODY,
                  tempo_bpm: int = DEFAULT_TEMPO_BPM) -> float:
    """Write a MIDI file and return its length in seconds."""
    if not notes:
        raise ValueError("The note list is empty.")
    if melody_instrument not in INSTRUMENTS:
        raise ValueError(f"Unknown instrument: {melody_instrument}")

    mid = mido.MidiFile(type=1, ticks_per_beat=TICKS_PER_BEAT)
    melody_track, total_ticks = _build_melody(
        notes, INSTRUMENTS[melody_instrument], tempo_bpm)
    final_start = total_ticks - notes[-1].duration
    mid.tracks.append(melody_track)
    mid.tracks.append(_build_bass(final_start, total_ticks, scale_name))
    mid.save(path)
    return mid.length


def _build_melody(notes: list[Note], program: int, tempo_bpm: int):
    """Return the melody track and its total length in ticks."""
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name="Melody", time=0))
    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo_bpm), time=0))
    track.append(mido.Message("program_change", channel=MELODY_CHANNEL,
                              program=program, time=0))

    carry = 0                # ticks of silence before the next event
    total = 0
    for i, note in enumerate(notes):
        track.append(mido.Message("control_change", channel=MELODY_CHANNEL,
                                  control=PAN_CC, value=note.pan, time=carry))
        track.append(mido.Message("note_on", channel=MELODY_CHANNEL,
                                  note=note.pitch, velocity=note.velocity, time=0))
        is_last = i == len(notes) - 1
        # The final note rings for its full length, without a gap
        sounding = note.duration if is_last else int(note.duration * GATE)
        track.append(mido.Message("note_off", channel=MELODY_CHANNEL,
                                  note=note.pitch, velocity=0, time=sounding))
        carry = note.duration - sounding
        total += note.duration

    track.append(mido.MetaMessage("end_of_track", time=carry))
    return track, total


def _build_bass(final_start: int, total_ticks: int, scale_name: str) -> mido.MidiTrack:
    """Bass: one root note per bar following harmony.bass_plan()."""
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name="Bass", time=0))
    track.append(mido.Message("program_change", channel=BASS_CHANNEL,
                              program=BASS_PROGRAM, time=0))
    for root, duration in bass_plan(final_start, total_ticks, scale_name):
        track.append(mido.Message("note_on", channel=BASS_CHANNEL,
                                  note=root, velocity=BASS_VELOCITY, time=0))
        track.append(mido.Message("note_off", channel=BASS_CHANNEL,
                                  note=root, velocity=0, time=duration))
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track