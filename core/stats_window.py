import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
from collections import defaultdict, Counter
from core.stats_tracker import CSV_FILES, CSV_DIR, IDLE_THRESHOLD

BG      = "#0a0a1a"
PANEL   = "#12122a"
ACCENT  = "#b048e8"
ACCENT2 = "#77c402"
TEXT    = "#d1fffd"
GRID    = "#1e1e3a"
PLOT_BG = "#0d0d22"

PUZZLE_ORDER = [
    ("puzzle_1_tuner",   "Trion Tuner"),
    ("puzzle_2_seed",    "Plant Seed"),
    ("puzzle_3_entropy", "Liquid Entropy + Safe"),
    ("puzzle_4_safe",    "Charge Battery"),
    ("puzzle_5_battery", "Insert Drive"),
    ("puzzle_6_drive",   "Decrypt Drive"),
]

def _style_ax(ax):
    ax.set_facecolor(PLOT_BG)
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(ACCENT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linewidth=0.6)

def _embed(fig, parent):
    fig.patch.set_facecolor(PLOT_BG)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return canvas

def _no_data(ax, msg="No data recorded yet"):
    ax.text(0.5, 0.5, msg, transform=ax.transAxes,
            ha="center", va="center", color=TEXT, fontsize=10)

def _read_csv(feature):
    path = CSV_FILES.get(feature, "")
    if not os.path.isfile(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _rows_for_session(rows, session_id):
    return [r for r in rows if r.get("session_id") == session_id]

def _stint_totals_from_rows(rows):
    counts = defaultdict(int)
    dim_of = {}
    for r in rows:
        key = (r.get("session_id", "s"), r["stint_id"])
        counts[key] += 1
        dim_of[key]  = r["dimension"]
    result = {"past": [], "present": [], "future": []}
    for key, total in counts.items():
        d = dim_of[key]
        if d in result:
            result[d].append(total)
    return result

def _stint_totals_from_tuples(dim_rows):
    counts = defaultdict(int)
    for dim, sid in dim_rows:
        counts[(dim, sid)] += 1
    result = {"past": [], "present": [], "future": []}
    for (dim, _), total in counts.items():
        if dim in result:
            result[dim].append(total)
    return result

def _puzzle_totals_from_rows(rows):
    counts = defaultdict(int)
    for r in rows:
        stage = r.get("puzzle_stage", r.get("item_name", ""))
        if stage and stage != "puzzle_done":
            counts[(r["session_id"], stage)] += 1
    result = defaultdict(list)
    for (_, stage), cnt in counts.items():
        result[stage].append(cnt)
    return result

def _make_sub_notebook(parent):
    style_name = "Inner.TNotebook"
    style = ttk.Style()
    style.configure(f"{style_name}",        background=PANEL, borderwidth=0)
    style.configure(f"{style_name}.Tab",    background=GRID,  foreground=TEXT,
                    padding=[10, 4],         font=("Courier", 8, "bold"))
    style.map(f"{style_name}.Tab",
              background=[("selected", ACCENT2)],
              foreground=[("selected", BG)])
    nb = ttk.Notebook(parent, style=style_name)
    nb.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
    return nb

def _sub_frames(parent):
    nb = _make_sub_notebook(parent)
    f_this = tk.Frame(nb, bg=PANEL)
    f_all  = tk.Frame(nb, bg=PANEL)
    nb.add(f_this, text="  This Session  ")
    nb.add(f_all,  text="  All Sessions  ")
    return f_this, f_all

def _click_coords_graph(parent, coords, title):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.4))
    fig.suptitle(title, color=ACCENT, fontsize=10)
    if coords:
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        ax1.hist(xs, bins=np.arange(0, 850, 80), color=ACCENT, edgecolor=BG, linewidth=0.5)
        ax1.set_xlabel("Screen X"); ax1.set_ylabel("Click Count")
        ax1.set_title("Horizontal Distribution")
        ax2.hist(ys, bins=np.arange(0, 650, 60), color=ACCENT2, edgecolor=BG,
                 linewidth=0.5, orientation="horizontal")
        ax2.set_xlabel("Click Count"); ax2.set_ylabel("Screen Y")
        ax2.set_title("Vertical Distribution")
    else:
        for ax in (ax1, ax2): _no_data(ax)
    for ax in (ax1, ax2): _style_ax(ax)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    _embed(fig, parent)
    plt.close(fig)

def build_click_coords(parent, tracker):
    f_this, f_all = _sub_frames(parent)

    # This session
    this_coords = tracker.get_click_coords()
    _click_coords_graph(f_this, this_coords,
                        f"This Session  ({len(this_coords)} clicks)")

    # All sessions
    csv_rows  = _read_csv("click_coords")
    all_coords = [(int(row["click_x"]), int(row["click_y"])) for row in csv_rows] \
                 if csv_rows else this_coords
    _click_coords_graph(f_all, all_coords,
                        f"All Sessions  ({len(all_coords)} clicks)")

def _dim_boxplot(parent, stint_data, title):
    fig, ax = plt.subplots(figsize=(7, 3.8))
    dims   = ["past",        "present",        "future"]
    labels = ["Past (1986)", "Present (2026)", "Future (2066)"]
    colors = [ACCENT,         ACCENT2,          TEXT]
    data   = [stint_data[d] if stint_data[d] else [0] for d in dims]

    bp = ax.boxplot(data, patch_artist=True, medianprops={"color": BG, "linewidth": 2})
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color); patch.set_alpha(0.8)
    for element in ["whiskers", "caps", "fliers"]:
        for artist in bp[element]: artist.set_color(TEXT)

    ylim = ax.get_ylim()
    for i, d in enumerate(dims):
        ax.text(i + 1, ylim[0], f"n={len(stint_data[d])}",
                ha="center", color=GRID, fontsize=7)

    ax.set_xticks(range(1, 4))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Clicks per Stint")
    ax.set_title(title, color=ACCENT)
    _style_ax(ax); fig.tight_layout()
    _embed(fig, parent); plt.close(fig)

def build_clicks_per_dim(parent, tracker):
    f_this, f_all = _sub_frames(parent)

    # This session from in-memory dim rows
    this_stints = _stint_totals_from_tuples(tracker.get_dim_rows())
    _dim_boxplot(f_this, this_stints, "Clicks Per Dimension — This Session")

    # All sessions from CSV
    csv_rows = _read_csv("clicks_per_dim")
    all_stints = _stint_totals_from_rows(csv_rows) if csv_rows else this_stints
    _dim_boxplot(f_all, all_stints, "Clicks Per Dimension — All Sessions")

def _thinking_graph(parent, durations, indices, title):
    fig, ax = plt.subplots(figsize=(8, 3.4))
    if durations:
        ax.plot(indices, durations, color=ACCENT, linewidth=1.5,
                marker="o", markersize=4, markerfacecolor=ACCENT2)
        ax.fill_between(indices, durations, alpha=0.15, color=ACCENT)
        ax.axhline(IDLE_THRESHOLD, color=TEXT, linewidth=0.8, linestyle="--", alpha=0.5,
                   label=f"{IDLE_THRESHOLD}-sec threshold")
        ax.set_xlabel("Thinking Event #"); ax.set_ylabel("Idle Duration (s)")
        ax.legend(facecolor=PANEL, labelcolor=TEXT, fontsize=8)
    else:
        _no_data(ax, "No idle gaps > 3 seconds recorded")
    ax.set_title(title, color=ACCENT)
    _style_ax(ax); fig.tight_layout()
    _embed(fig, parent); plt.close(fig)

def build_thinking_time(parent, tracker):
    f_this, f_all = _sub_frames(parent)

    # This session
    this_times = tracker.get_thinking_times()
    _thinking_graph(f_this,
                    [t[0] for t in this_times],
                    [t[1] for t in this_times],
                    "Thinking Time — This Session")

    # All sessions
    csv_rows = _read_csv("thinking_time")
    if csv_rows:
        all_dur = [float(r["idle_duration_sec"]) for r in csv_rows]
        all_idx = list(range(len(all_dur)))
    else:
        all_dur = [t[0] for t in this_times]
        all_idx = [t[1] for t in this_times]
    _thinking_graph(f_all, all_dur, all_idx, "Thinking Time — All Sessions")

def _puzzle_table(parent, counts_this, counts_all, current_last):
    """
    counts_this: dict puzzle_stage -> int  (this session)
    counts_all:  dict puzzle_stage -> [int, ...]  (all sessions)
    current_last: puzzle_stage the player stopped at
    """
    outer = tk.Frame(parent, bg=PANEL)
    outer.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

    col_puzzle  = 24
    col_session = 10
    col_div     = 2
    col_stats   = [7, 7, 8, 8, 8]

    # Header
    hdr = tk.Frame(outer, bg=GRID)
    hdr.pack(fill=tk.X, padx=4)

    def _h(text, width, fg=ACCENT, bg=GRID):
        tk.Label(hdr, text=text, bg=bg, fg=fg,
                 font=("Courier", 9, "bold"), width=width,
                 anchor="center", padx=2, pady=6).pack(side=tk.LEFT)

    _h("Puzzle",       col_puzzle)
    _h("This Session", col_session, fg=ACCENT2)
    _h("|",            col_div,     fg=GRID, bg=GRID)
    for h, w in zip(["Min","Max","Mean","Median","Std Dev"], col_stats):
        _h(h, w)

    # Sub-header
    sub = tk.Frame(outer, bg="#0d0d22")
    sub.pack(fill=tk.X, padx=4)
    tk.Label(sub, text="", bg="#0d0d22",
             width=col_puzzle+col_session+col_div,
             font=("Courier", 7)).pack(side=tk.LEFT)
    tk.Label(sub, text="◄─── All Sessions ───►",
             bg="#0d0d22", fg=GRID, font=("Courier", 7, "italic"),
             width=sum(col_stats)).pack(side=tk.LEFT)

    # Data rows
    for i, (pid, label) in enumerate(PUZZLE_ORDER):
        this_val = counts_this.get(pid, 0)
        all_vals = counts_all.get(pid, [])
        is_last  = pid == current_last

        row_bg = "#1e0a2e" if is_last else (PANEL if i % 2 == 0 else "#16163a")
        row    = tk.Frame(outer, bg=row_bg)
        row.pack(fill=tk.X, padx=4)

        label_text = f"{i+1} · {label}" + ("  ◄" if is_last else "")
        tk.Label(row, text=label_text, bg=row_bg,
                 fg=ACCENT if is_last else TEXT,
                 font=("Courier", 9, "bold" if is_last else "normal"),
                 width=col_puzzle, anchor="w", padx=6, pady=5).pack(side=tk.LEFT)

        tk.Label(row,
                 text=str(this_val) if this_val else "n/a",
                 bg=row_bg,
                 fg=ACCENT2 if this_val else GRID,
                 font=("Courier", 9, "bold" if this_val else "normal"),
                 width=col_session, anchor="center", pady=5).pack(side=tk.LEFT)

        tk.Label(row, text="|", bg=row_bg, fg=GRID,
                 font=("Courier", 9), width=col_div,
                 anchor="center").pack(side=tk.LEFT)

        if all_vals:
            arr = np.array(all_vals, dtype=float)
            cells = [int(arr.min()), int(arr.max()),
                     f"{arr.mean():.1f}", f"{np.median(arr):.1f}", f"{arr.std():.1f}"]
            sfg = TEXT
        else:
            cells = ["n/a"]*5
            sfg   = GRID

        for val, w in zip(cells, col_stats):
            tk.Label(row, text=str(val), bg=row_bg, fg=sfg,
                     font=("Courier", 9), width=w,
                     anchor="center", pady=5).pack(side=tk.LEFT)

    tk.Label(outer,
             text="◄ = stopped here  |  n/a = not reached  |  Higher mean → harder",
             bg=PANEL, fg=GRID, font=("Courier", 8, "italic")
             ).pack(pady=(10, 4))

def build_puzzle_clicks(parent, tracker):
    f_this, f_all = _sub_frames(parent)

    # Current session counts
    current_rows   = tracker.get_puzzle_stage_rows()
    current_counts = defaultdict(int)
    current_last   = None
    for r in current_rows:
        stage = r.get("puzzle_stage", "")
        if stage and stage != "puzzle_done":
            current_counts[stage] += 1
            current_last = stage

    # All-sessions from CSV
    csv_rows = _read_csv("clicks_btw_puzzles")
    all_agg  = _puzzle_totals_from_rows(csv_rows) if csv_rows else defaultdict(list)

    # This session
    _puzzle_table(f_this, current_counts, defaultdict(list), current_last)

    # All sessions
    _puzzle_table(f_all, current_counts, all_agg, current_last)

def _zone_bar(parent, zones, counts, title):
    fig, ax = plt.subplots(figsize=(7, 3.8))
    x    = np.arange(len(zones))
    bars = ax.bar(x, counts, color=ACCENT, edgecolor=BG, linewidth=0.5, width=0.55)

    max_c = max(counts) if any(counts) else 1
    for bar, count in zip(bars, counts):
        t = count / max_c
        r = int(176*t + 40*(1-t)); g = int(72*t + 40*(1-t)); b = int(232*t + 80*(1-t))
        bar.set_facecolor(f"#{r:02x}{g:02x}{b:02x}")
        if count > 0:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.3,
                    str(count), ha="center", va="bottom", color=TEXT, fontsize=9)

    ax.set_xticks(x); ax.set_xticklabels(zones, fontsize=9)
    ax.set_ylabel("Entry Count")
    ax.set_title(title, color=ACCENT)
    _style_ax(ax); fig.tight_layout()
    _embed(fig, parent); plt.close(fig)

def build_zone_entries(parent, tracker):
    f_this, f_all = _sub_frames(parent)

    zones = [f"Zone {i}" for i in range(1, 7)]

    # This session
    ze_this  = tracker.get_zone_entries()
    cnt_this = [ze_this.get(z, 0) for z in zones]
    _zone_bar(f_this, zones, cnt_this, "Zone Entries — This Session")

    # All sessions
    csv_rows = _read_csv("zone_entries")
    if csv_rows:
        zc = Counter(r["zone"] for r in csv_rows)
        cnt_all = [zc.get(z, 0) for z in zones]
    else:
        cnt_all = cnt_this
    _zone_bar(f_all, zones, cnt_all, "Zone Entries — All Sessions")

# Main window
def show_stats(tracker):
    root = tk.Tk()
    root.title("THE TRION — Session Statistics")
    root.configure(bg=BG)
    root.geometry("920x620")
    root.resizable(True, True)

    all_rows   = _read_csv("click_coords")
    n_sessions = len(set(r["session_id"] for r in all_rows)) if all_rows else 1

    # Header
    header = tk.Frame(root, bg=PANEL, height=52)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    tk.Label(header, text="◈  THE TRION  —  SESSION STATS",
             bg=PANEL, fg=ACCENT, font=("Courier", 14, "bold")
             ).pack(side=tk.LEFT, padx=20, pady=12)
    tk.Label(header,
             text=f"session: {tracker.session_id}   |   total sessions: {n_sessions}",
             bg=PANEL, fg=GRID, font=("Courier", 8)
             ).pack(side=tk.RIGHT, padx=20)

    # Main notebook
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook",     background=BG,    borderwidth=0)
    style.configure("TNotebook.Tab", background=PANEL, foreground=TEXT,
                    padding=[14, 6], font=("Courier", 9, "bold"))
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", BG)])

    nb = ttk.Notebook(root)
    nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=(6, 4))

    for tab_label, builder in [
        ("📍 Click Map",     build_click_coords),
        ("⏱  Dimensions",   build_clicks_per_dim),
        ("💭 Thinking Time", build_thinking_time),
        ("🧩 Puzzle Clicks", build_puzzle_clicks),
        ("🗺  Zone Entries", build_zone_entries),
    ]:
        frame = tk.Frame(nb, bg=PANEL)
        nb.add(frame, text=tab_label)
        builder(frame, tracker)

    # Footer
    footer = tk.Frame(root, bg=BG)
    footer.pack(fill=tk.X, padx=10, pady=(0, 8))
    tk.Label(footer, text=f"CSVs: {os.path.abspath(CSV_DIR)}",
             bg=BG, fg=GRID, font=("Courier", 8)).pack(side=tk.LEFT)
    tk.Button(footer, text="CLOSE", bg=ACCENT, fg=BG,
              font=("Courier", 10, "bold"), relief=tk.FLAT,
              padx=20, pady=6, cursor="hand2",
              command=root.destroy).pack(side=tk.RIGHT)

    root.mainloop()
