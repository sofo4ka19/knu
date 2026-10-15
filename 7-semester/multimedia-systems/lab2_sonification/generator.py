"""generator.py: writes a MIDI file from a list of notes.

The file has two tracks:
    track 0: the melody (channel 0), with a constant tempo
    track 1: the bass (channel 1), one note per chord from theory.py
"""
import mido

from mapping import CADENCE_NOTES
from harmony import TICKS_PER_BEAT

MELODY_CHANNEL = 0
BASS_CHANNEL = 1
GATE = 0.9                      # a note sounds for 90% of its length, then a short pause
BASS_VELOCITY = 70
BASS_PROGRAM = 32               # acoustic bass
PAN_CONTROLLER = 10             # MIDI controller number for pan

DEFAULT_TEMPO_BPM = 100
TEMPO_RANGE = (50, 180)         # tempos accepted by the window and the command line

# General MIDI instrument numbers
INSTRUMENTS = {
    "Piano": 0,
    "Vibraphone": 11,
    "Acoustic Guitar": 24,
    "Flute": 73,
    "Strings": 48,
}
DEFAULT_INSTRUMENT = "Piano"


def generate_midi(notes, path, scale, instrument=DEFAULT_INSTRUMENT, tempo=DEFAULT_TEMPO_BPM):
    """Save the notes as a MIDI file and return its length in seconds."""
    midi = mido.MidiFile(type=1, ticks_per_beat=TICKS_PER_BEAT)
    melody_track, total_ticks = make_melody_track(notes, INSTRUMENTS[instrument], tempo)

    final_start = total_ticks - notes[-1].duration
    approach_start = sum(note.duration for note in notes[:-CADENCE_NOTES])
    plan = scale.bass_plan(final_start, total_ticks, approach_start)

    midi.tracks.append(melody_track)
    midi.tracks.append(make_bass_track(plan))
    midi.save(path)
    return midi.length


def make_melody_track(notes, program, tempo):
    """Return the melody track and its length in ticks."""
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name="Melody", time=0))
    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo), time=0))
    track.append(mido.Message("program_change", channel=MELODY_CHANNEL,
                              program=program, time=0))

    pause = 0                   # silence (in ticks) before the next note
    total_ticks = 0
    for i, note in enumerate(notes):
        track.append(mido.Message("control_change", channel=MELODY_CHANNEL,
                                  control=PAN_CONTROLLER, value=note.pan, time=pause))
        track.append(mido.Message("note_on", channel=MELODY_CHANNEL,
                                  note=note.pitch, velocity=note.velocity, time=0))
        if i == len(notes) - 1:
            sounding = note.duration            # the last note rings to the end
        else:
            sounding = int(note.duration * GATE)
        track.append(mido.Message("note_off", channel=MELODY_CHANNEL,
                                  note=note.pitch, velocity=0, time=sounding))
        pause = note.duration - sounding
        total_ticks += note.duration
    return track, total_ticks


def make_bass_track(plan):
    """Bass track: one long note for every item of the bass plan."""
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name="Bass", time=0))
    track.append(mido.Message("program_change", channel=BASS_CHANNEL,
                              program=BASS_PROGRAM, time=0))
    for bass_note, length in plan:
        track.append(mido.Message("note_on", channel=BASS_CHANNEL,
                                  note=bass_note, velocity=BASS_VELOCITY, time=0))
        track.append(mido.Message("note_off", channel=BASS_CHANNEL,
                                  note=bass_note, velocity=0, time=length))
    return track