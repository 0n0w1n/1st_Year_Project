"""
Module for tracking and logging game statistics to CSV files.
"""
import csv
import os
import time
import uuid
from datetime import datetime

CSV_DIR = "data/stats"
IDLE_THRESHOLD = 3.0  # seconds of inactivity before counting as "thinking time"
CSV_FILES = {
    "click_coords":       os.path.join(CSV_DIR, "click_coords.csv"),
    "clicks_per_dim":     os.path.join(CSV_DIR, "clicks_per_dim.csv"),
    "thinking_time":      os.path.join(CSV_DIR, "thinking_time.csv"),
    "clicks_btw_puzzles": os.path.join(CSV_DIR, "clicks_btw_puzzles.csv"),
    "zone_entries":       os.path.join(CSV_DIR, "zone_entries.csv"),
}

HEADERS = {
    # 1 row per click
    "click_coords":       ["session_id", "timestamp", "click_x", "click_y", "zone", "dimension"],
    # 1 row per click
    "clicks_per_dim":     ["session_id", "timestamp", "dimension", "stint_id"],
    # 1 row per idle gap > 3 s
    "thinking_time":      ["session_id", "timestamp", "idle_duration_sec", "zone", "dimension"],
    # 1 row per click
    "clicks_btw_puzzles": ["session_id", "timestamp", "item_name", "puzzle_stage", "zone", "dimension"],
    # 1 row per zone entry
    "zone_entries":       ["session_id", "timestamp", "zone", "dimension", "total_entries_so_far"],
}


class StatsTracker:
    """
    Tracks player behavior including clicks, dimension changes, idle time, and zone entries.
    """
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:4]
        self._rows = {key: [] for key in CSV_FILES}

        # Feature 2: stint tracking
        self._current_dim = "present"
        self._stint_id    = 0       # increments each time dimension changes

        # Feature 3: idle time
        self._last_click_time = time.time()

        # Feature 5: zone totals
        self._zone_totals = {i: 0 for i in range(1, 7)}

        # Puzzle guard
        self._solved_puzzles = set()
        self._current_puzzle_id    = None
        self._current_puzzle_label = None

    def _ts(self):
        """Generates a formatted string of the current timestamp."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _row(self, feature, **fields):
        """
        Internal helper to append a data row to the in-memory storage.
        feature (str): The key corresponding to the CSV_FILES category.
        **fields: Arbitrary keyword arguments representing CSV columns.
        """
        row = {"session_id": self.session_id, "timestamp": self._ts()}
        row.update(fields)
        self._rows[feature].append(row)

    def record_click(self, pos, zone, dimension, item_name, puzzle_stage="unknown"):
        """One row per left click — the core collection method."""
        x, y = pos
        now  = time.time()

        # Feature 1: coordinates
        self._row("click_coords",
                  click_x=x, click_y=y,
                  zone=f"Zone {zone}", dimension=dimension)

        # Feature 2: dimension + stint_id (stint_id increments on dimension change)
        if dimension != self._current_dim:
            self._current_dim  = dimension
            self._stint_id    += 1
        self._row("clicks_per_dim",
                  dimension=dimension,
                  stint_id=self._stint_id)

        # Feature 3: thinking time only when idle > 3 s
        idle = now - self._last_click_time
        if idle > IDLE_THRESHOLD:
            self._row("thinking_time",
                      idle_duration_sec=round(idle, 2),
                      zone=f"Zone {zone}", dimension=dimension)
        self._last_click_time = now

        # Feature 4: store item clicked and which puzzle was active
        self._row("clicks_btw_puzzles",
                  item_name=item_name,
                  puzzle_stage=puzzle_stage,
                  zone=f"Zone {zone}", dimension=dimension)

    def record_zone_entry(self, zone_number, dimension):
        """
        Logs when a player enters a new zone
        """
        self._zone_totals[zone_number] = self._zone_totals.get(zone_number, 0) + 1
        self._row("zone_entries",
                  zone=f"Zone {zone_number}",
                  dimension=dimension,
                  total_entries_so_far=self._zone_totals[zone_number])

    def set_active_puzzle(self, puzzle_id, puzzle_label):
        """Sets the current puzzle context for tracking."""
        self._current_puzzle_id    = puzzle_id
        self._current_puzzle_label = puzzle_label

    def record_puzzle_solved(self, puzzle_id, _puzzle_label):
        """Adds a puzzle ID to the solved set to prevent duplicate logging."""
        if puzzle_id in self._solved_puzzles:
            return
        self._solved_puzzles.add(puzzle_id)

    def finalise(self):
        """Writes all recorded session data from memory to physical CSV files."""
        os.makedirs(CSV_DIR, exist_ok=True)
        for feature, filepath in CSV_FILES.items():
            rows = self._rows[feature]
            if not rows:
                continue
            headers  = HEADERS[feature]
            new_file = not os.path.isfile(filepath)
            with open(filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
                if new_file:
                    writer.writeheader()
                writer.writerows(rows)
        print(f"[StatsTracker] Session '{self.session_id}' saved to {CSV_DIR}/")

    # Read-back helpers for stats_window
    def get_click_coords(self):
        """Returns a list of x, y coordinate tuples for the current session."""
        return [(int(r["click_x"]), int(r["click_y"])) for r in self._rows["click_coords"]]

    def get_dim_rows(self):
        """Returns list of (dimension, stint_id) per click."""
        return [(r["dimension"], r["stint_id"]) for r in self._rows["clicks_per_dim"]]

    def get_thinking_times(self):
        """Returns a list of (duration, index) for each idle event."""
        return [(float(r["idle_duration_sec"]), i)
                for i, r in enumerate(self._rows["thinking_time"])]

    def get_puzzle_stage_rows(self):
        """Returns list of (item_name, puzzle_stage) dicts for current session."""
        return [{"item_name": r["item_name"], "puzzle_stage": r["puzzle_stage"],
                 "session_id": r["session_id"]}
                for r in self._rows["clicks_btw_puzzles"]]

    def get_zone_entries(self):
        """Returns a dictionary summarizing total entries per zone."""
        result = {f"Zone {i}": 0 for i in range(1, 7)}
        for r in self._rows["zone_entries"]:
            z = r["zone"]
            if z in result:
                result[z] += 1
        return result
