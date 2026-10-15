"""tkinter graphical interface of the sonification program."""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

from data_loader import DataError, load_csv
from generator import (DEFAULT_INSTRUMENT, DEFAULT_TEMPO_BPM, INSTRUMENTS,
                       TEMPO_RANGE, generate_midi)
from mapping import build_notes, pitch_per_point, point_start_ticks
from player import MidiPlayer, PlayerError
from harmony import DEFAULT_SCALE_NAME, SCALES, TICKS_PER_BEAT

# --- Constants ---
WINDOW_TITLE = "Data Sonification"
WINDOW_SIZE = "940x780"
WINDOW_MIN_SIZE = (800, 650)
DEFAULT_OUTPUT = "output.mid"
POLL_MS = 100            # how often the playback position is refreshed
PAD = 8
NONE = "(none)"

# (short name, label in the window, is the role required)
ROLES = [
    ("Melody", "Melody (pitch):", True),
    ("Rhythm", "Rhythm (note length):", True),
    ("Loudness", "Loudness (optional):", False),
    ("Pan", "Stereo pan (optional):", False),
]


class SonificationApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.source = None             # DataFrame read from the CSV file
        self.source_path = None
        self.columns = {}              # text shown in a list -> real column name
        self.used = []                 # [(role, column)] of the last generation
        self.midi_path = None          # path of the last generated file
        self.duration = 0.0            # its length in seconds
        self.plot_points = 0
        self.point_pitches = []        # pitch of the melody at every data point
        self.cursor_times = []         # seconds at which each data point starts
        self.cursor_xs = []            # the matching positions on the plot
        self.player = MidiPlayer()
        self.state = "stopped"          # "stopped", "playing" or "paused"
        self._poll_job = None           # id of the scheduled position update
        self.cursors = []              # vertical lines on the plots
        self.canvas = None

        root.title(WINDOW_TITLE)
        root.geometry(WINDOW_SIZE)
        root.minsize(*WINDOW_MIN_SIZE)
        self._create_variables()
        self._build_widgets()
        self._update_buttons()
        root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------ building
    def _create_variables(self):
        self.csv_var = tk.StringVar()
        self.out_var = tk.StringVar(value=os.path.abspath(DEFAULT_OUTPUT))
        self.scale_var = tk.StringVar(value=DEFAULT_SCALE_NAME)
        self.instrument_var = tk.StringVar(value=DEFAULT_INSTRUMENT)
        self.tempo_var = tk.DoubleVar(value=DEFAULT_TEMPO_BPM)
        self.tempo_text = tk.StringVar(value=f"{DEFAULT_TEMPO_BPM} BPM")
        self.role_vars = [tk.StringVar(value=NONE) for _ in ROLES]
        self.status_var = tk.StringVar(
            value="Choose a CSV file, check the columns and press Generate.")
        self.time_var = tk.StringVar(value="")

    def _build_widgets(self):
        outer = ttk.Frame(self.root, padding=PAD)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(4, weight=1)

        self._build_data_frame(outer).grid(row=0, column=0, sticky="ew")
        self._build_music_frame(outer).grid(row=1, column=0, sticky="ew", pady=PAD)
        self._build_output_frame(outer).grid(row=2, column=0, sticky="ew")
        self._build_buttons(outer).grid(row=3, column=0, sticky="ew", pady=PAD)

        self.plot_frame = ttk.LabelFrame(outer, text="Data used for the melody",
                                         padding=PAD)
        self.plot_frame.grid(row=4, column=0, sticky="nsew")

        status = ttk.Label(outer, textvariable=self.status_var, wraplength=800)
        status.grid(row=5, column=0, sticky="ew", pady=(PAD, 0))
        status.bind("<Configure>",
                    lambda e: status.configure(wraplength=max(200, e.width - 10)))

    def _build_data_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="1. Data", padding=PAD)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="CSV file:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.csv_var).grid(
            row=0, column=1, sticky="ew", padx=PAD)
        ttk.Button(frame, text="Browse...", command=self._browse_csv).grid(
            row=0, column=2)

        roles = ttk.Frame(frame)
        roles.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(PAD, 0))
        roles.columnconfigure(1, weight=1)
        roles.columnconfigure(3, weight=1)
        self.role_boxes = []
        for i, (_, label, _required) in enumerate(ROLES):
            row, col = divmod(i, 2)
            ttk.Label(roles, text=label).grid(
                row=row, column=col * 2, sticky="w", pady=2,
                padx=(0 if col == 0 else PAD * 2, PAD))
            box = ttk.Combobox(roles, textvariable=self.role_vars[i],
                               state="disabled", width=22)
            box.grid(row=row, column=col * 2 + 1, sticky="ew", pady=2)
            self.role_boxes.append(box)

        ttk.Label(frame, foreground="gray", wraplength=860,
                  text="Tip: columns with only a few distinct values (flags such as "
                       "0/1) give a monotonous melody, so they are not chosen "
                       "by default.").grid(row=2, column=0, columnspan=3,
                                           sticky="w", pady=(PAD, 0))
        return frame

    def _build_music_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="2. Music", padding=PAD)

        top = ttk.Frame(frame)
        top.pack(fill="x")
        ttk.Label(top, text="Scale:").pack(side="left")
        ttk.Combobox(top, textvariable=self.scale_var, values=list(SCALES),
                     state="readonly", width=12).pack(side="left", padx=(4, PAD * 2))
        ttk.Label(top, text="Instrument:").pack(side="left")
        ttk.Combobox(top, textvariable=self.instrument_var,
                     values=list(INSTRUMENTS), state="readonly",
                     width=16).pack(side="left", padx=(4, PAD * 2))

        bottom = ttk.Frame(frame)
        bottom.pack(fill="x", pady=(PAD, 0))
        ttk.Label(bottom, text="Tempo:").pack(side="left")
        ttk.Scale(bottom, from_=TEMPO_RANGE[0], to=TEMPO_RANGE[1],
                  variable=self.tempo_var, length=260,
                  command=lambda v: self.tempo_text.set(f"{float(v):.0f} BPM")
                  ).pack(side="left", padx=4)
        ttk.Label(bottom, textvariable=self.tempo_text, width=8).pack(side="left")
        return frame

    def _build_output_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="3. Output", padding=PAD)
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text="Save MIDI as:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.out_var).grid(
            row=0, column=1, sticky="ew", padx=PAD)
        ttk.Button(frame, text="Save as...", command=self._browse_output).grid(
            row=0, column=2)
        return frame

    def _build_buttons(self, parent):
        frame = ttk.Frame(parent)
        self.generate_btn = ttk.Button(frame, text="Generate", command=self._generate)
        self.play_btn = ttk.Button(frame, text="Play", command=self._play)
        self.pause_btn = ttk.Button(frame, text="Pause", command=self._pause)
        self.stop_btn = ttk.Button(frame, text="Stop", command=self._stop)
        for button in (self.generate_btn, self.play_btn, self.pause_btn, self.stop_btn):
            button.pack(side="left", padx=(0, PAD))
        ttk.Label(frame, textvariable=self.time_var).pack(side="left", padx=PAD)
        return frame

    # ------------------------------------------------------- file and data
    def _browse_csv(self):
        path = filedialog.askopenfilename(
            title="Choose a CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        self.csv_var.set(path)
        try:
            self._load_columns(path)
        except DataError as e:
            messagebox.showerror("Data error", str(e))

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save MIDI file", defaultextension=".mid",
            filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")])
        if path:
            self.out_var.set(path)

    def _load_columns(self, path: str):
        """Read the file and fill the column lists. Raises DataError."""
        df = load_csv(path)
        self.source, self.source_path = df, path
        self.columns = {str(c): c for c in df.columns}
        names = list(self.columns)
        suggested = names          # load_csv() already put flag columns last
        for i, box in enumerate(self.role_boxes):
            required = ROLES[i][2]
            box["values"] = names if required else [NONE] + names
            box.configure(state="readonly")
            self.role_vars[i].set(suggested[i] if i < len(suggested) else NONE)
        rows = df.attrs.get("source_rows", len(df))
        self.status_var.set(
            f"Loaded {rows} rows (averaged to {len(df)} points), "
            f"{len(names)} numeric columns. Check the columns and press Generate.")

    def _build_input(self):
        """Turn the chosen roles into a table for build_notes()."""
        chosen = [var.get() for var in self.role_vars]
        names = [n for n in chosen if n != NONE]
        if any(n not in self.columns for n in names) or \
                chosen[0] == NONE or chosen[1] == NONE:
            raise DataError("Choose columns for Melody and Rhythm.")
        if len(set(names)) != len(names):
            raise DataError("Each role needs a different column.")

        melody, rhythm, loudness, pan = chosen
        sequence = [melody, rhythm]
        if loudness != NONE:
            sequence.append(loudness)
        if pan != NONE:
            if loudness == NONE:
                sequence.append(rhythm)
            sequence.append(pan)

        table = pd.DataFrame({
            f"c{i}": self.source[self.columns[name]].to_numpy()
            for i, name in enumerate(sequence)
        })
        used = [(ROLES[i][0], chosen[i]) for i in range(len(ROLES)) if chosen[i] != NONE]
        return table, used

    # ------------------------------------------------------------- actions
    def _generate(self):
        csv_path = self.csv_var.get().strip()
        out_path = self.out_var.get().strip()
        if not csv_path:
            messagebox.showerror("No file", "Choose a CSV file first.")
            return
        if not out_path:
            messagebox.showerror("No file", "Choose where to save the MIDI file.")
            return

        self._stop()   # the old file may still be playing (and locked on Windows)
        scale = SCALES[self.scale_var.get()]
        try:
            if self.source is None or self.source_path != csv_path:
                self._load_columns(csv_path)
            table, used = self._build_input()
            tempo = int(round(self.tempo_var.get()))
            notes = build_notes(table, scale)
            seconds = generate_midi(notes, out_path, scale,
                                    self.instrument_var.get(), tempo)
        except DataError as e:
            messagebox.showerror("Data error", str(e))
            return
        except OSError as e:
            messagebox.showerror("File error", f"Could not write the MIDI file: {e}")
            return

        self.midi_path, self.duration, self.used = out_path, seconds, used
        self._prepare_cursor(notes, tempo)
        self.point_pitches = pitch_per_point(notes)
        roles = ", ".join(f"{role}: {name}" for role, name in used)
        self.status_var.set(f"Done: {len(notes)} notes, {seconds:.0f} s. "
                            f"{roles}. Saved to {out_path}")
        self.time_var.set("")
        self._draw_plot()
        self._update_buttons()

    def _play(self):
        """Play from the start, or continue from the place where it was paused."""
        if not self.midi_path:
            return
        try:
            if self.state == "paused":
                self.player.resume()
            else:
                self.player.play(self.midi_path)
        except PlayerError as e:
            messagebox.showerror("Playback error", str(e))
            return
        self.state = "playing"
        self._update_buttons()
        self._cancel_poll()
        self._poll()

    def _pause(self):
        if self.state != "playing":
            return
        try:
            self.player.pause()
        except PlayerError as e:
            messagebox.showerror("Playback error", str(e))
            return
        self.state = "paused"
        self._cancel_poll()
        self.time_var.set(f"{self.player.position():4.1f} / {self.duration:4.1f} s (paused)")
        self._update_buttons()

    def _stop(self):
        """Stop and rewind; the next Play starts from the beginning."""
        if self.state != "stopped":
            try:
                self.player.stop()
            except PlayerError:
                pass
            self._finish_playback()

    def _poll(self):
        """Refresh the time label and the plot cursor while music is playing."""
        if self.state != "playing":
            return
        if self.player.is_playing():
            position = self.player.position()
            self.time_var.set(f"{position:4.1f} / {self.duration:4.1f} s")
            self._move_cursor(position)
            self._poll_job = self.root.after(POLL_MS, self._poll)
        else:
            self._finish_playback()

    def _cancel_poll(self):
        if self._poll_job is not None:
            self.root.after_cancel(self._poll_job)
            self._poll_job = None

    def _finish_playback(self):
        self._cancel_poll()
        self.state = "stopped"
        self.time_var.set("")
        self._move_cursor(0)
        self._update_buttons()

    # ---------------------------------------------------------------- plot
    def _draw_plot(self):
        """One small chart per used column, drawn from the data the melody uses."""
        if self.source is None:
            return
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        real = [self.columns[name] for _, name in self.used]
        data = self.source[real]
        self.plot_points = len(data)
        self.plot_frame.configure(
            text=f"Data used for the melody (averaged to {self.plot_points} points). "
                 "Orange line: the notes of the melody")

        figure = Figure(figsize=(6, 3), dpi=100, constrained_layout=True)
        axes = figure.subplots(len(real), 1, sharex=True, squeeze=False)[:, 0]
        self.cursors = []
        for ax, (role, name), column in zip(axes, self.used, real):
            ax.plot(data[column].to_numpy(), linewidth=1.2)
            ax.set_ylabel(f"{role}\n{name}", fontsize=8)
            ax.tick_params(labelsize=8)
            ax.set_xlim(0, self.plot_points - 1)
            self.cursors.append(ax.axvline(0, color="black", linewidth=1.5))
            if role == "Melody":
                self._overlay_notes(ax)
        axes[-1].set_xlabel("Data point", fontsize=8)

        self.canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()

    def _prepare_cursor(self, notes, tempo_bpm: int):
        """Build the table "playback time -> position on the plot"."""
        ticks_per_second = tempo_bpm / 60 * TICKS_PER_BEAT
        starts = point_start_ticks(notes)
        total = sum(note.duration for note in notes)
        self.cursor_times = [t / ticks_per_second for t in starts] + [total / ticks_per_second]
        self.cursor_xs = list(range(len(starts))) + [len(starts) - 1]

    def _overlay_notes(self, ax):
        """Draw the pitch of the melody over the Melody chart (right-hand axis)."""
        count = min(len(self.point_pitches), self.plot_points)
        notes_ax = ax.twinx()
        notes_ax.step(range(count), self.point_pitches[:count], where="mid",
                      color="tab:orange", linewidth=1.4)
        names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        notes_ax.yaxis.set_major_formatter(FuncFormatter(
            lambda v, _: f"{names[int(round(v)) % 12]}{int(round(v)) // 12 - 1}"))
        notes_ax.tick_params(labelsize=8, colors="tab:orange")
        notes_ax.set_ylabel("Note", fontsize=8, color="tab:orange")

    def _move_cursor(self, seconds: float):
        """Move the cursor to the data point that is sounding now."""
        if not self.cursors or self.canvas is None or not self.cursor_times:
            return
        x = float(np.interp(seconds, self.cursor_times, self.cursor_xs))
        for line in self.cursors:
            line.set_xdata([x, x])
        self.canvas.draw_idle()

    # ------------------------------------------------------------- helpers
    def _update_buttons(self):
        """Play is available when there is a file and the music is not sounding."""
        can_play = self.midi_path is not None and self.state != "playing"
        self.play_btn.configure(text="Resume" if self.state == "paused" else "Play")
        self.play_btn.state(["!disabled"] if can_play else ["disabled"])
        self.pause_btn.state(["!disabled"] if self.state == "playing" else ["disabled"])
        self.stop_btn.state(["!disabled"] if self.state != "stopped" else ["disabled"])

    def _on_close(self):
        self._cancel_poll()
        try:
            self.player.stop()
        except PlayerError:
            pass
        self.root.destroy()


def run() -> None:
    """Open the main window."""
    root = tk.Tk()
    SonificationApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()