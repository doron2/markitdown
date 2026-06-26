# Copyright 2024 doron2. Tkinter GUI wrapper for microsoft/markitdown (MIT License).
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, font, messagebox, scrolledtext, ttk

from markitdown import MarkItDown


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MarkItDown GUI")
        self.resizable(True, True)
        self.minsize(600, 400)

        self._input_files: list[Path] = []
        self._output_dir: Path | None = None
        self._queue: queue.Queue = queue.Queue()

        self._build_ui()
        self._poll_queue()

    # ------------------------------------------------------------------ UI --
    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # --- input files row ---
        frm_in = ttk.Frame(self)
        frm_in.pack(fill="x", **pad)
        ttk.Button(frm_in, text="Select files…", command=self._pick_files).pack(side="left")
        self._lbl_files = ttk.Label(frm_in, text="No files selected", foreground="grey")
        self._lbl_files.pack(side="left", padx=6)

        # --- output folder row ---
        frm_out = ttk.Frame(self)
        frm_out.pack(fill="x", **pad)
        ttk.Button(frm_out, text="Output folder…", command=self._pick_outdir).pack(side="left")
        self._lbl_outdir = ttk.Label(frm_out, text="Same folder as each input file (default)", foreground="grey")
        self._lbl_outdir.pack(side="left", padx=6)

        # --- convert button ---
        self._btn_convert = ttk.Button(self, text="Convert", command=self._start_conversion)
        self._btn_convert.pack(**pad)

        # --- status area ---
        ttk.Label(self, text="Status:").pack(anchor="w", padx=8)
        mono = font.Font(family="Courier", size=10)
        self._status = scrolledtext.ScrolledText(self, height=16, state="disabled", font=mono)
        self._status.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._status.tag_config("ok", foreground="green")
        self._status.tag_config("err", foreground="red")

    # ---------------------------------------------------------------- picks --
    def _pick_files(self):
        paths = filedialog.askopenfilenames(title="Select input files")
        if paths:
            self._input_files = [Path(p) for p in paths]
            self._lbl_files.config(
                text=f"{len(self._input_files)} file(s) selected", foreground="black"
            )

    def _pick_outdir(self):
        d = filedialog.askdirectory(title="Select output folder")
        if d:
            self._output_dir = Path(d)
            self._lbl_outdir.config(text=str(self._output_dir), foreground="black")

    # ----------------------------------------------------------- conversion --
    def _start_conversion(self):
        if not self._input_files:
            messagebox.showwarning("No files", "Please select at least one input file.")
            return

        self._btn_convert.config(state="disabled")
        self._clear_status()

        thread = threading.Thread(
            target=self._convert_all,
            args=(list(self._input_files), self._output_dir),
            daemon=True,
        )
        thread.start()

    def _convert_all(self, files: list[Path], out_dir: Path | None):
        md = MarkItDown()
        for path in files:
            dest_dir = out_dir if out_dir is not None else path.parent
            dest = dest_dir / (path.stem + ".md")
            try:
                result = md.convert(str(path))
                dest.write_text(result.text_content, encoding="utf-8")
                self._queue.put(("ok", f"✓  {path.name}  →  {dest}\n"))
            except Exception as exc:
                self._queue.put(("err", f"✗  {path.name}  —  {exc}\n"))

        self._queue.put(("done", None))

    # --------------------------------------------------------- queue/UI sync --
    def _poll_queue(self):
        try:
            while True:
                tag, msg = self._queue.get_nowait()
                if tag == "done":
                    self._btn_convert.config(state="normal")
                else:
                    self._append_status(msg, tag)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _append_status(self, text: str, tag: str):
        self._status.config(state="normal")
        self._status.insert("end", text, tag)
        self._status.see("end")
        self._status.config(state="disabled")

    def _clear_status(self):
        self._status.config(state="normal")
        self._status.delete("1.0", "end")
        self._status.config(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
