# Data Sonification

A program that turns numeric data from a CSV file into a MIDI composition.
Every numeric column influences the music, and the rules are relative to the
data itself, so the program works with any CSV file, not with one fixed data set.


## Features

- Reads any CSV file (delimiter and decimal comma are detected automatically),
  keeps the numeric columns and reports clear errors for unusable files.
- Builds a two-track MIDI file: a melody driven by the data and a bass line.
- Three scales (pentatonic, major, minor), five melody instruments, adjustable tempo.
- The melody follows the values of the first column: the higher the value, the
  higher the note.
- Graphical interface (tkinter): choose which column drives which part of the
  music, play the result and see the data used, one chart per column, with a
  cursor that follows the music.

## Requirements

- Python 3.9 or newer (tkinter must be available; it ships with Python on Windows).
- Packages: `pip install -r requirements.txt` (pandas, numpy, mido, pygame, matplotlib).

## Usage

```
python main.py
```

1. Press **Browse...** and choose a CSV file.
2. Check the four column lists (Melody, Rhythm, Loudness, Stereo pan). The
   program fills them with suggested columns; change them if you like. Melody
   and Rhythm are required, the other two are optional.
3. Choose the scale, the instrument and the tempo.
4. Press **Generate**: the MIDI file is written to the chosen path.
5. Press **Play** to listen. **Pause** stops the music in place, and the same button
   (now called **Resume**) continues from that place. **Stop** rewinds to the
   beginning. The black line on the charts shows the current position.

### Input data

A CSV file with at least **two numeric columns** and at least 8 rows. Text and
date columns are ignored; empty cells are filled by interpolation; constant
columns are dropped. If the file has more than 96 rows, rows are averaged in
blocks, so the table has at most 96 rows (one row = one note of the melody).
All of this is done once, in `load_csv()`, and the rest of the program only
receives the ready table.

In the window you choose the columns yourself; each role needs a different
column, so at least two different indicators always influence the music. By
default, columns with only a few distinct values (flags such as 0/1) are
offered last, because they give a monotonous melody.

## How data becomes sound

All values are first converted to **relative ranks (0..1)** within their column,
so units and absolute values do not matter and a single outlier cannot flatten
the melody.

Column 1 to 4 below are the columns chosen for Melody, Rhythm, Loudness and Pan.

| Column | What is taken from the data | MIDI parameter |
|---|---|---|
| 1 | rank of the smoothed value | pitch: high value = high note. Per note the melody moves at most 4 scale steps (3 for pentatonic) toward the wanted pitch; a leap (a move of more than one step) lands on a chord tone |
| 1 | very large change (top 20%) | rhythmic figure: triplet or fast run |
| 1 | direction and size of the last changes | the way the melody ends (see below) |
| 2 | smoothed value | note duration: 2, 1 or 1/2 beat (higher value = shorter note) |
| 2 | value | velocity (if there is no third column) |
| 3 | value | velocity |
| 4 | value | pan (CC10, left / right position) |

With exactly two columns, each of them still affects at least one MIDI parameter.
If Pan is chosen but Loudness is not, the Rhythm column also drives the velocity.
The tempo is a constant setting and does not depend on the data.

### Musical rules

These rules make the result sound like music instead of random notes. Most of them
do not depend on the data; the way the melody ends does:

- The melody starts on the tonic (C) and always ends on the tonic, held for one
  full bar (the only note with a fixed length). The two notes before it depend on
  how the data end: rising data come to the tonic from below, falling data from
  above; small changes give a step-by-step approach, large changes a leap (table
  below). The bass plays the dominant (G) from the start of the approach and then
  the tonic.
- On strong beats (1 and 3) the melody moves to a tone of the chord played by the bass.
- A leap (a move of more than one scale step) lands on a chord tone, so it never ends on a note that clashes with the bass.
- Rhythm is aligned to the beat: short notes come in pairs, long notes start on beats 1 or 3.
- Rhythmic figures appear only on weak beats and at least 6 notes apart.
- The bass loops C - Am - F - G (Cm - Ab - Eb - Bb in minor).

The ending in major (the last note is always C; minor and pentatonic use the notes of their own scale):

| End of the data | Changes | Last three notes |
|---|---|---|
| falling | small | E - D - C |
| falling | large | G - D - C |
| rising | small | A - B - C |
| rising | large | G - B - C |

"Large" means that the mean rank of the last four changes is above 0.5.

## How the program is organized

The data goes through three steps, and each step is one module:

```
CSV file --load_csv()--> table --build_notes()--> list of notes --generate_midi()--> MIDI file
(data_loader.py)         (mapping.py)                             (generator.py)
```

```
main.py          starts the program (opens the window)
ui.py            the window: choose columns, play, plot of the data
data_loader.py   reads the CSV file and prepares the table (fills gaps, averages to <= 96 rows)
mapping.py       the rules that turn the table into notes
harmony.py       music theory: time grid, scales and chords (used by mapping.py and generator.py)
generator.py     writes the MIDI file (a melody track and a bass track)
player.py        plays the MIDI file (play, pause, resume, stop)
sample_data/     synthetic example files (smooth, noisy, with outliers)
```

## Notes and limitations

- Playback uses the system MIDI synthesizer through pygame. It works on Windows;
  on macOS and Linux it may fail without a SoundFont. In that case open the
  generated `.mid` file in any MIDI player (for example VLC with a SoundFont,
  or MuseScore).
- On the Melody chart the orange line shows the notes the melody actually plays,
  so you can compare the data with the music.
- The charts show the data after averaging to at most 96 points, exactly the
  data the melody is built from. The cursor follows the real timing: every
  note remembers the data point it was made from, so the cursor is at the
  point that is sounding now (it depends on the accuracy of the playback
  position reported by the system).
- The key is fixed (C major / C minor).