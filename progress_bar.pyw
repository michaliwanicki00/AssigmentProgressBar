"""Assignment Progress Tracker.

Tracks the Big Data Processing - Functional Programming assignment
(C:\\Users\\haryd\\BigDataAnalisys\\fp_template).

Tick the questions you have finished; each part's bar (and the overall
0-125 bar) fills by the point value of the questions you check. Your
ticks are remembered between runs.
"""

import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

DATA_FILE = Path(__file__).with_name("progress_bar_data.json")

BG = "#f4f4f5"
CARD = "#ffffff"
FG = "#18181b"
MUTED = "#71717a"
ACCENT = "#6366f1"
DONE = "#16a34a"

# Each part: key, title, source file(s), and its questions as (id, label, points).
# Point values come from the /** Qn (Xp) */ headers in the template .scala files.
PARTS = [
    {
        "key": "intro",
        "title": "Part 1 \u00b7 Intro",
        "folder": "src/main/scala/intro",
        "questions": [
            ("Q0", "Q0 \u00b7 fizzBuzz", 2),
            ("Q1", "Q1 \u00b7 hofs / lambdas", 1),
            ("Q2", "Q2 \u00b7 customAverage", 3),
            ("Q3", "Q3 \u00b7 firstDivByX", 2),
            ("Q4", "Q4 \u00b7 onlyEvenNumbers", 2),
            ("Q5", "Q5 \u00b7 twice", 2),
            ("Q6", "Q6 \u00b7 drunkWords", 2),
            ("Q7", "Q7 \u00b7 myForAll", 3),
            ("Q8", "Q8 \u00b7 lastElem", 3),
            ("Q9", "Q9 \u00b7 append", 4),
            ("Q10", "Q10 \u00b7 firstN", 2),
            ("Q11", "Q11 \u00b7 maxValue", 4),
            ("Q12", "Q12 \u00b7 intList", 3),
            ("Q13", "Q13 \u00b7 myFilter", 7),
        ],
    },
    {
        "key": "fp_functions",
        "title": "Part 2 \u00b7 FP Functions",
        "folder": "src/main/scala/fp_functions",
        "questions": [
            ("Q14", "Q14 \u00b7 map", 5),
            ("Q15", "Q15 \u00b7 filter", 5),
            ("Q16", "Q16 \u00b7 recFlat", 5),
            ("Q17", "Q17 \u00b7 foldL", 5),
            ("Q18", "Q18 \u00b7 foldR", 5),
            ("Q19", "Q19 \u00b7 zip", 5),
        ],
    },
    {
        "key": "fp_practice",
        "title": "Part 3 \u00b7 FP Practice",
        "folder": "src/main/scala/fp_practice",
        "questions": [
            ("Q20", "Q20 \u00b7 first10Above25", 4),
            ("Q21", "Q21 \u00b7 passingStudents", 5),
            ("Q22", "Q22 \u00b7 headSumsTail", 6),
        ],
    },
    {
        "key": "dataset",
        "title": "Part 4 \u00b7 Dataset",
        "folder": "src/main/scala/dataset",
        "questions": [
            ("Q23", "Q23 \u00b7 avgAdditions", 4),
            ("Q24", "Q24 \u00b7 jsTime", 4),
            ("Q25", "Q25 \u00b7 topCommitter", 5),
            ("Q26", "Q26 \u00b7 commitsPerRepo", 9),
            ("Q27", "Q27 \u00b7 topFileFormats", 9),
            ("Q28", "Q28 \u00b7 mostProductivePart", 9),
        ],
    },
]

PART_TOTAL = {p["key"]: sum(pts for _, _, pts in p["questions"]) for p in PARTS}
GRAND_TOTAL = sum(PART_TOTAL.values())
ALL_IDS = {qid for p in PARTS for qid, _, _ in p["questions"]}


def load():
    """Return the set of ticked question ids; tolerant of missing/corrupt/old files."""
    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        done = raw.get("done", [])
        return {qid for qid in done if qid in ALL_IDS}
    except Exception:
        return set()


def fmt(value):
    """Show 40 rather than 40.0, but keep 40.5."""
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


class App:
    def __init__(self, root):
        self.root = root
        root.title("Assignment Progress")
        root.configure(bg=BG)
        root.geometry("470x650")
        root.minsize(430, 420)

        done = load()
        self.vars = {}  # qid -> BooleanVar

        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=CARD)
        style.configure("Bg.TFrame", background=BG)
        style.configure("TLabel", background=CARD, foreground=FG, font=("Segoe UI", 10))
        style.configure("Head.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Total.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure(
            "TCheckbutton", background=CARD, foreground=FG, font=("Segoe UI", 10)
        )
        style.map("TCheckbutton", background=[("active", CARD)])
        style.configure("TButton", font=("Segoe UI", 10), padding=5)
        for name, col in (("Bar", ACCENT), ("Done", DONE)):
            style.configure(
                f"{name}.Horizontal.TProgressbar",
                troughcolor=BG, bordercolor=BG,
                background=col, lightcolor=col, darkcolor=col,
                thickness=20,
            )

        # --- scrolling container ------------------------------------------------
        wrap = tk.Frame(root, bg=BG)
        wrap.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(wrap, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=BG)
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width)
        )
        self.canvas.bind_all("<MouseWheel>", self._on_wheel)

        pad = dict(padx=14, pady=(0, 12))

        # --- total ------------------------------------------------------------
        total_card = tk.Frame(self.inner, bg=CARD, padx=14, pady=12)
        total_card.pack(fill="x", padx=14, pady=(14, 12))
        self.total_label = ttk.Label(total_card, text="", style="Total.TLabel")
        self.total_label.pack(anchor="w", pady=(0, 6))
        self.total_bar = ttk.Progressbar(
            total_card, style="Bar.Horizontal.TProgressbar",
            mode="determinate", maximum=100,
        )
        self.total_bar.pack(fill="x")

        # --- one block per part --------------------------------------------------
        self.part_widgets = {}
        for part in PARTS:
            card = tk.Frame(self.inner, bg=CARD, padx=14, pady=12)
            card.pack(fill="x", **pad)

            head = ttk.Label(card, text="", style="Head.TLabel")
            head.pack(anchor="w", pady=(0, 6))
            bar = ttk.Progressbar(
                card, style="Bar.Horizontal.TProgressbar",
                mode="determinate", maximum=100,
            )
            bar.pack(fill="x", pady=(0, 8))
            ttk.Label(
                card, text=part["folder"], foreground=MUTED, font=("Segoe UI", 8)
            ).pack(anchor="w", pady=(0, 4))

            for qid, label, pts in part["questions"]:
                var = tk.BooleanVar(value=qid in done)
                self.vars[qid] = var
                ttk.Checkbutton(
                    card, text=f"{label} ({pts}p)", variable=var,
                    command=self.recompute,
                ).pack(anchor="w")

            self.part_widgets[part["key"]] = (head, bar)

        # --- buttons ----------------------------------------------------------
        btns = tk.Frame(self.inner, bg=BG)
        btns.pack(fill="x", padx=14, pady=(0, 16))
        ttk.Button(btns, text="Check all", command=lambda: self.set_all(True)).pack(
            side="left"
        )
        ttk.Button(
            btns, text="Uncheck all", command=lambda: self.set_all(False)
        ).pack(side="left", padx=8)

        root.bind("<Escape>", lambda *_: self.close())
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.recompute()
        self.center()

    # ------------------------------------------------------------------ helpers
    def _on_wheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def set_all(self, value):
        if not value and not messagebox.askyesno(
            "Uncheck all", "Untick every question?"
        ):
            return
        for var in self.vars.values():
            var.set(value)
        self.recompute()

    def recompute(self):
        grand = 0
        for part in PARTS:
            earned = sum(
                pts for qid, _, pts in part["questions"] if self.vars[qid].get()
            )
            grand += earned
            total = PART_TOTAL[part["key"]]
            pct = earned / total * 100 if total else 0
            head, bar = self.part_widgets[part["key"]]
            done = earned >= total
            bar.configure(
                style="Done.Horizontal.TProgressbar"
                if done
                else "Bar.Horizontal.TProgressbar"
            )
            bar["value"] = pct
            tail = "   \u2713 done" if done else ""
            head.configure(
                text=f"{part['title']} \u2014 {fmt(earned)} / {total} \u00b7 {pct:.0f}%{tail}",
                foreground=DONE if done else FG,
            )

        pct = grand / GRAND_TOTAL * 100 if GRAND_TOTAL else 0
        done = grand >= GRAND_TOTAL
        self.total_bar.configure(
            style="Done.Horizontal.TProgressbar"
            if done
            else "Bar.Horizontal.TProgressbar"
        )
        self.total_bar["value"] = pct
        tail = "   \U0001f389 all done!" if done else ""
        self.total_label.configure(
            text=f"Assignment \u2014 {fmt(grand)} / {GRAND_TOTAL} \u00b7 {pct:.0f}%{tail}",
            foreground=DONE if done else FG,
        )
        self.save()

    def save(self):
        try:
            done = sorted(
                (qid for qid, var in self.vars.items() if var.get()),
                key=lambda q: int(q[1:]),
            )
            DATA_FILE.write_text(json.dumps({"done": done}), encoding="utf-8")
        except Exception:
            pass

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 3
        self.root.geometry(f"+{x}+{y}")

    def close(self):
        self.save()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
