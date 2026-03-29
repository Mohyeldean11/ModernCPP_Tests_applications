import json
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import customtkinter as ctk
import tkinter as tk
from tkinter import TclError, messagebox

try:
    from plyer import notification as desktop_notification
except Exception:
    desktop_notification = None


APP_NAME = "Weekly Checklist Pro"
DATA_DIR = Path("checklist_data")
DEFAULT_PROFILE = "General"
PRIORITY_VALUES = ["High", "Medium", "Low"]
SORT_VALUES = ["Manual", "Day", "Hours ↑", "Hours ↓", "Priority", "Status"]
POMODORO_PRESETS = {
    "Classic 25/5": (25 * 60, 5 * 60),
    "Deep Work 50/10": (50 * 60, 10 * 60),
    "Sprint 15/3": (15 * 60, 3 * 60),
}


@dataclass
class Task:
    id: str
    title: str
    hours: float
    day: str  # YYYY-MM-DD
    completed: bool = False
    completed_at: Optional[str] = None
    order: int = 0
    tag: str = ""
    priority: str = "Medium"


class TaskStore:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.base_dir / "_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _week_start(date_obj: datetime) -> datetime:
        return date_obj - timedelta(days=date_obj.weekday())

    def week_key(self, date_obj: datetime) -> str:
        ws = self._week_start(date_obj)
        return ws.strftime("%Y-%m-%d")

    def _read_json(self, path: Path, default):
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _write_json_atomic(self, path: Path, payload) -> None:
        temp = path.with_suffix(path.suffix + ".tmp")
        temp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temp.replace(path)

    def _backup_if_exists(self, path: Path) -> None:
        if not path.exists():
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.stem}_{timestamp}{path.suffix}"
        try:
            shutil.copy2(path, self.backup_dir / backup_name)
        except Exception:
            return

    def profile_dir(self, profile: str) -> Path:
        path = self.base_dir / profile
        path.mkdir(parents=True, exist_ok=True)
        return path

    def profile_file(self) -> Path:
        return self.base_dir / "profiles.json"

    def settings_file(self) -> Path:
        return self.base_dir / "settings.json"

    def load_settings(self) -> Dict[str, object]:
        default = {"rollover_enabled": False, "font_scale": 1.0}
        loaded = self._read_json(self.settings_file(), default)
        if not isinstance(loaded, dict):
            return default
        merged = dict(default)
        merged.update(loaded)
        return merged

    def save_settings(self, settings: Dict[str, object]) -> None:
        self._write_json_atomic(self.settings_file(), settings)

    def load_profiles(self) -> List[str]:
        p = self.profile_file()
        if not p.exists():
            self.save_profiles([DEFAULT_PROFILE])
            return [DEFAULT_PROFILE]
        try:
            profiles = self._read_json(p, [DEFAULT_PROFILE])
            if not profiles:
                return [DEFAULT_PROFILE]
            return sorted(set(str(x) for x in profiles))
        except Exception:
            return [DEFAULT_PROFILE]

    def save_profiles(self, profiles: List[str]) -> None:
        self._write_json_atomic(self.profile_file(), sorted(set(profiles)))

    def files_for_week(self, profile: str, week_key: str) -> Dict[str, Path]:
        pdir = self.profile_dir(profile)
        return {
            "todo": pdir / f"{week_key}_todo.json",
            "completed": pdir / f"{week_key}_completed.json",
        }

    def load_week(self, profile: str, week_key: str) -> List[Task]:
        files = self.files_for_week(profile, week_key)
        tasks: List[Task] = []
        for status in ["todo", "completed"]:
            file_path = files[status]
            if file_path.exists():
                try:
                    rows = self._read_json(file_path, [])
                    for row in rows:
                        if not isinstance(row, dict):
                            continue
                        t = Task(
                            id=str(row.get("id", f"legacy-{int(datetime.now().timestamp() * 1000)}")),
                            title=str(row.get("title", "Untitled task")),
                            hours=float(row.get("hours", 1.0)),
                            day=str(row.get("day", week_key)),
                            completed=bool(row.get("completed", False)),
                            completed_at=row.get("completed_at"),
                            order=int(row.get("order", 0)),
                            tag=str(row.get("tag", "")),
                            priority=str(row.get("priority", "Medium")),
                        )
                        if t.priority not in PRIORITY_VALUES:
                            t.priority = "Medium"
                        if status == "completed":
                            t.completed = True
                        tasks.append(t)
                except Exception:
                    continue
        # Deduplicate by id (completed state takes precedence)
        by_id: Dict[str, Task] = {}
        for task in tasks:
            prev = by_id.get(task.id)
            if prev is None or task.completed:
                by_id[task.id] = task

        ordered = sorted(by_id.values(), key=lambda x: (x.order, x.day, x.title.lower(), x.id))
        for idx, task in enumerate(ordered):
            try:
                task.hours = float(task.hours)
            except (TypeError, ValueError):
                task.hours = 0.0
            task.title = str(task.title)
            task.day = str(task.day)
            task.tag = str(task.tag or "")
            if task.priority not in PRIORITY_VALUES:
                task.priority = "Medium"
            task.order = idx
        return ordered

    def save_week(self, profile: str, week_key: str, tasks: List[Task]) -> None:
        files = self.files_for_week(profile, week_key)
        ordered = sorted(tasks, key=lambda x: x.order)
        todo = [asdict(t) for t in ordered if not t.completed]
        done = [asdict(t) for t in ordered if t.completed]
        self._backup_if_exists(files["todo"])
        self._backup_if_exists(files["completed"])
        self._write_json_atomic(files["todo"], todo)
        self._write_json_atomic(files["completed"], done)

    def load_all_weeks(self, profile: str) -> Dict[str, List[Task]]:
        pdir = self.profile_dir(profile)
        weeks: Dict[str, List[Task]] = {}
        for file_path in pdir.glob("*_todo.json"):
            week = file_path.name.replace("_todo.json", "")
            weeks[week] = self.load_week(profile, week)
        for file_path in pdir.glob("*_completed.json"):
            week = file_path.name.replace("_completed.json", "")
            if week not in weeks:
                weeks[week] = self.load_week(profile, week)
        return weeks

    def pomodoro_history_file(self, profile: str) -> Path:
        return self.profile_dir(profile) / "pomodoro_history.json"

    def load_pomodoro_history(self, profile: str) -> List[Dict[str, object]]:
        rows = self._read_json(self.pomodoro_history_file(profile), [])
        if not isinstance(rows, list):
            return []
        clean_rows: List[Dict[str, object]] = []
        for row in rows:
            if isinstance(row, dict):
                clean_rows.append(row)
        return clean_rows

    def save_pomodoro_history(self, profile: str, rows: List[Dict[str, object]]) -> None:
        self._backup_if_exists(self.pomodoro_history_file(profile))
        self._write_json_atomic(self.pomodoro_history_file(profile), rows)


class ChecklistApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1260x820")
        self.minsize(1060, 720)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.store = TaskStore(DATA_DIR)
        self.settings = self.store.load_settings()
        self.profiles = self.store.load_profiles()
        self.current_profile = ctk.StringVar(value=self.profiles[0])
        self.active_profile_name = self.current_profile.get()
        self.current_week_key = self.store.week_key(datetime.now())
        self.week_picker_var = ctk.StringVar(value=self.current_week_key)
        self.tasks: List[Task] = self.store.load_week(self.current_profile.get(), self.current_week_key)
        self.normalize_task_order()
        self.pomodoro_history: List[Dict[str, object]] = self.store.load_pomodoro_history(self.current_profile.get())
        self.current_pomodoro_session_id: Optional[str] = None

        self.timer_running = False
        self.timer_seconds = 0
        self.timer_mode = "stopwatch"  # stopwatch | pomodoro_focus | pomodoro_break
        self.pomodoro_preset = ctk.StringVar(value=list(POMODORO_PRESETS.keys())[0])
        self.active_pomodoro_preset = self.pomodoro_preset.get()
        self.is_fullscreen = False
        self.notifications_enabled = ctk.BooleanVar(value=True)
        self.rollover_enabled = ctk.BooleanVar(value=bool(self.settings.get("rollover_enabled", False)))

        self.search_var = ctk.StringVar(value="")
        self.filter_status_var = ctk.StringVar(value="All")
        self.filter_day_var = ctk.StringVar(value="All")
        self.filter_priority_var = ctk.StringVar(value="All")
        self.filter_tag_var = ctk.StringVar(value="")
        self.filter_hours_min_var = ctk.StringVar(value="")
        self.filter_hours_max_var = ctk.StringVar(value="")
        self.sort_var = ctk.StringVar(value=SORT_VALUES[0])

        self.dragging_task_id: Optional[str] = None
        self.task_card_refs: Dict[str, ctk.CTkFrame] = {}
        self.selected_task_id: Optional[str] = None
        self.mini_hover_window: Optional[ctk.CTkToplevel] = None
        self.mini_hover_widgets: Dict[str, object] = {}
        self.command_palette_window: Optional[ctk.CTkToplevel] = None
        self.calendar_picker_window: Optional[ctk.CTkToplevel] = None
        self.shortcuts_help_window: Optional[ctk.CTkToplevel] = None

        self.font_scale = float(self.settings.get("font_scale", 1.0))
        self.font_scale = max(0.85, min(1.35, self.font_scale))

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        ctk.set_widget_scaling(self.font_scale)
        ctk.set_window_scaling(self.font_scale)

        self._build_ui()
        self.update_week_context()
        self.bind_shortcuts()
        self.bind_all("<ButtonRelease-1>", self.finish_task_drag, add="+")
        self.render_tasks()
        self.update_clock()
        self.update_timer()
        self.refresh_progress()
        self.render_pomodoro_history()

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(self, corner_radius=16)
        self.topbar.grid(row=0, column=0, padx=14, pady=(12, 8), sticky="ew")
        self.topbar.grid_columnconfigure(10, weight=1)

        self.profile_menu = ctk.CTkOptionMenu(
            self.topbar,
            values=self.profiles,
            variable=self.current_profile,
            command=self.on_profile_change,
            width=180,
        )
        self.profile_menu.grid(row=0, column=0, padx=(12, 8), pady=12)

        self.new_profile_entry = ctk.CTkEntry(self.topbar, placeholder_text="New profile name", width=180)
        self.new_profile_entry.grid(row=0, column=1, padx=8, pady=12)

        self.add_profile_btn = ctk.CTkButton(self.topbar, text="Add Profile", command=self.add_profile, width=100)
        self.add_profile_btn.grid(row=0, column=2, padx=8, pady=12)

        self.theme_toggle = ctk.CTkSegmentedButton(
            self.topbar,
            values=["Dark", "Light"],
            command=self.on_theme_change,
            width=130,
        )
        self.theme_toggle.set("Dark")
        self.theme_toggle.grid(row=0, column=3, padx=8, pady=12)

        self.fullscreen_btn = ctk.CTkButton(self.topbar, text="Fullscreen", command=self.toggle_fullscreen, width=100)
        self.fullscreen_btn.grid(row=0, column=4, padx=8, pady=12)

        self.float_btn = ctk.CTkButton(self.topbar, text="Mini Hover", command=self.open_mini_hover, width=100)
        self.float_btn.grid(row=0, column=5, padx=8, pady=12)

        self.notify_switch = ctk.CTkSwitch(
            self.topbar,
            text="Notify",
            variable=self.notifications_enabled,
            onvalue=True,
            offvalue=False,
            width=90,
        )
        self.notify_switch.grid(row=0, column=6, padx=8, pady=12)

        self.rollover_switch = ctk.CTkSwitch(
            self.topbar,
            text="Rollover",
            variable=self.rollover_enabled,
            onvalue=True,
            offvalue=False,
            width=95,
            command=self.persist_settings,
        )
        self.rollover_switch.grid(row=0, column=7, padx=8, pady=12)

        self.font_minus_btn = ctk.CTkButton(self.topbar, text="A-", width=36, command=self.decrease_font_scale)
        self.font_minus_btn.grid(row=0, column=8, padx=(8, 4), pady=12)

        self.font_plus_btn = ctk.CTkButton(self.topbar, text="A+", width=36, command=self.increase_font_scale)
        self.font_plus_btn.grid(row=0, column=9, padx=(4, 8), pady=12)

        self.clock_lbl = ctk.CTkLabel(self.topbar, text="", font=("JetBrains Mono", 18, "bold"))
        self.clock_lbl.grid(row=0, column=10, padx=12, pady=12, sticky="e")

        week_nav = ctk.CTkFrame(self.topbar, corner_radius=12)
        week_nav.grid(row=1, column=0, columnspan=11, padx=10, pady=(0, 10), sticky="ew")
        week_nav.grid_columnconfigure(2, weight=1)

        ctk.CTkButton(week_nav, text="◀ Week", width=88, command=lambda: self.change_week(-1)).grid(
            row=0, column=0, padx=6, pady=8
        )
        ctk.CTkButton(week_nav, text="Today", width=70, command=self.go_to_current_week).grid(
            row=0, column=1, padx=6, pady=8
        )
        self.week_picker_entry = ctk.CTkEntry(
            week_nav, textvariable=self.week_picker_var, placeholder_text="YYYY-MM-DD (any day)", height=34
        )
        self.week_picker_entry.grid(row=0, column=2, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(week_nav, text="Pick", width=60, command=self.open_calendar_picker).grid(
            row=0, column=3, padx=6, pady=8
        )
        ctk.CTkButton(week_nav, text="Go", width=50, command=self.go_to_week_from_picker).grid(
            row=0, column=4, padx=6, pady=8
        )
        ctk.CTkButton(week_nav, text="Week ▶", width=88, command=lambda: self.change_week(1)).grid(
            row=0, column=5, padx=6, pady=8
        )
        ctk.CTkButton(week_nav, text="Palette", width=76, command=self.open_command_palette).grid(
            row=0, column=6, padx=6, pady=8
        )
        ctk.CTkButton(week_nav, text="Shortcuts", width=90, command=self.open_shortcuts_help).grid(
            row=0, column=7, padx=(2, 8), pady=8
        )

        self.body = ctk.CTkTabview(self, corner_radius=14)
        self.body.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")
        self.body.add("Tasks")
        self.body.add("Summary")
        self.body.add("Pomodoro")
        self.body.set("Tasks")

        self._build_tasks_tab(self.body.tab("Tasks"))
        self._build_summary_tab(self.body.tab("Summary"))
        self._build_pomodoro_tab(self.body.tab("Pomodoro"))

    def _build_tasks_tab(self, parent) -> None:
        parent.grid_columnconfigure(0, weight=2)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        composer = ctk.CTkFrame(parent, corner_radius=12)
        composer.grid(row=0, column=0, columnspan=2, padx=12, pady=12, sticky="ew")
        composer.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(composer, placeholder_text="Task title", height=40)
        self.task_entry.grid(row=0, column=0, padx=(10, 8), pady=10, sticky="ew")

        self.hours_entry = ctk.CTkEntry(composer, placeholder_text="Hours", width=110, height=40)
        self.hours_entry.grid(row=0, column=1, padx=8, pady=10)

        self.day_menu = ctk.CTkOptionMenu(composer, values=self.week_day_options(), width=165)
        self.day_menu.set(self.week_day_options()[datetime.now().weekday()])
        self.day_menu.grid(row=0, column=2, padx=8, pady=10)

        self.tag_entry = ctk.CTkEntry(composer, placeholder_text="Tag", width=120, height=40)
        self.tag_entry.grid(row=0, column=3, padx=8, pady=10)

        self.priority_menu = ctk.CTkOptionMenu(composer, values=PRIORITY_VALUES, width=120)
        self.priority_menu.set("Medium")
        self.priority_menu.grid(row=0, column=4, padx=8, pady=10)

        add_btn = ctk.CTkButton(composer, text="Add Task", command=self.add_task, height=40, width=110)
        add_btn.grid(row=0, column=5, padx=(8, 10), pady=10)

        ctk.CTkLabel(
            composer,
            text="Drag tasks by handle (⋮⋮). Use filters/search/sort below for fast workflow.",
            text_color=("#4b5563", "#9ca3af"),
        ).grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 8), sticky="w")

        filters = ctk.CTkFrame(parent, corner_radius=12)
        filters.grid(row=1, column=0, columnspan=2, padx=12, pady=(0, 12), sticky="ew")
        filters.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(filters, textvariable=self.search_var, placeholder_text="Keyword search", height=34)
        self.search_entry.grid(row=0, column=0, padx=(10, 6), pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda _e: self.render_tasks())

        self.filter_status_menu = ctk.CTkOptionMenu(
            filters,
            values=["All", "Todo", "Done"],
            variable=self.filter_status_var,
            command=lambda _v: self.render_tasks(),
            width=90,
        )
        self.filter_status_menu.grid(row=0, column=1, padx=6, pady=10)

        self.filter_day_menu = ctk.CTkOptionMenu(
            filters,
            values=["All"] + self.week_day_options(),
            variable=self.filter_day_var,
            command=lambda _v: self.render_tasks(),
            width=120,
        )
        self.filter_day_menu.grid(row=0, column=2, padx=6, pady=10)

        self.filter_priority_menu = ctk.CTkOptionMenu(
            filters,
            values=["All"] + PRIORITY_VALUES,
            variable=self.filter_priority_var,
            command=lambda _v: self.render_tasks(),
            width=95,
        )
        self.filter_priority_menu.grid(row=0, column=3, padx=6, pady=10)

        self.tag_filter_entry = ctk.CTkEntry(filters, textvariable=self.filter_tag_var, placeholder_text="Tag filter", width=100)
        self.tag_filter_entry.grid(row=0, column=4, padx=6, pady=10)
        self.tag_filter_entry.bind("<KeyRelease>", lambda _e: self.render_tasks())

        self.hours_min_entry = ctk.CTkEntry(
            filters,
            textvariable=self.filter_hours_min_var,
            placeholder_text="Min h",
            width=70,
        )
        self.hours_min_entry.grid(row=0, column=5, padx=6, pady=10)
        self.hours_min_entry.bind("<KeyRelease>", lambda _e: self.render_tasks())

        self.hours_max_entry = ctk.CTkEntry(
            filters,
            textvariable=self.filter_hours_max_var,
            placeholder_text="Max h",
            width=70,
        )
        self.hours_max_entry.grid(row=0, column=6, padx=6, pady=10)
        self.hours_max_entry.bind("<KeyRelease>", lambda _e: self.render_tasks())

        self.sort_menu = ctk.CTkOptionMenu(
            filters,
            values=SORT_VALUES,
            variable=self.sort_var,
            command=lambda _v: self.render_tasks(),
            width=100,
        )
        self.sort_menu.grid(row=0, column=7, padx=6, pady=10)

        ctk.CTkButton(filters, text="Clear", width=64, command=self.clear_filters).grid(row=0, column=8, padx=(6, 10), pady=10)

        self.task_list_frame = ctk.CTkScrollableFrame(parent, corner_radius=12)
        self.task_list_frame.grid(row=2, column=0, padx=(12, 8), pady=(0, 12), sticky="nsew")

        side_panel = ctk.CTkFrame(parent, corner_radius=12)
        side_panel.grid(row=2, column=1, padx=(8, 12), pady=(0, 12), sticky="nsew")
        side_panel.grid_columnconfigure(0, weight=1)

        self.week_label = ctk.CTkLabel(side_panel, text=f"Week of {self.current_week_key}", font=("Segoe UI", 16, "bold"))
        self.week_label.grid(row=0, column=0, padx=10, pady=(12, 6), sticky="w")

        self.week_progress = ctk.CTkProgressBar(side_panel, height=18)
        self.week_progress.grid(row=1, column=0, padx=10, pady=8, sticky="ew")
        self.week_progress.set(0)

        self.week_pct_label = ctk.CTkLabel(side_panel, text="Weekly completion: 0%")
        self.week_pct_label.grid(row=2, column=0, padx=10, pady=4, sticky="w")

        self.daily_label = ctk.CTkLabel(side_panel, text="Daily completion", font=("Segoe UI", 14, "bold"))
        self.daily_label.grid(row=3, column=0, padx=10, pady=(12, 4), sticky="w")

        self.daily_rows_frame = ctk.CTkFrame(side_panel, fg_color="transparent")
        self.daily_rows_frame.grid(row=4, column=0, padx=10, pady=(0, 8), sticky="ew")
        self.daily_rows_frame.grid_columnconfigure(0, weight=1)
        self.daily_rows: List[ctk.CTkLabel] = []
        for i in range(7):
            lbl = ctk.CTkLabel(self.daily_rows_frame, text="--: 0%", anchor="w")
            lbl.grid(row=i, column=0, pady=2, sticky="ew")
            self.daily_rows.append(lbl)

        ctk.CTkButton(
            side_panel,
            text="Rollover Unfinished → Next Week",
            command=self.rollover_to_next_week_manual,
        ).grid(row=5, column=0, padx=10, pady=(4, 8), sticky="ew")

        timer_frame = ctk.CTkFrame(side_panel, corner_radius=10)
        timer_frame.grid(row=6, column=0, padx=10, pady=(10, 12), sticky="ew")
        timer_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(timer_frame, text="Timer + Pomodoro", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, padx=8, pady=(10, 6), sticky="w"
        )
        self.timer_mode_label = ctk.CTkLabel(timer_frame, text="Mode: Stopwatch", text_color=("#4b5563", "#9ca3af"))
        self.timer_mode_label.grid(row=1, column=0, columnspan=3, padx=8, pady=(0, 4), sticky="w")

        self.timer_lbl = ctk.CTkLabel(timer_frame, text="00:00:00", font=("JetBrains Mono", 24, "bold"))
        self.timer_lbl.grid(row=2, column=0, columnspan=3, padx=8, pady=8)

        self.pomodoro_menu = ctk.CTkOptionMenu(
            timer_frame,
            values=list(POMODORO_PRESETS.keys()),
            variable=self.pomodoro_preset,
            command=self.on_pomodoro_preset_change,
        )
        self.pomodoro_menu.grid(row=3, column=0, columnspan=2, padx=(5, 4), pady=(2, 6), sticky="ew")
        ctk.CTkButton(timer_frame, text="Start Pomo", command=self.start_pomodoro).grid(
            row=3, column=2, padx=(4, 5), pady=(2, 6), sticky="ew"
        )

        ctk.CTkButton(timer_frame, text="Start Clock", command=self.start_timer).grid(
            row=4, column=0, padx=5, pady=(4, 10), sticky="ew"
        )
        ctk.CTkButton(timer_frame, text="Pause", command=self.pause_timer).grid(
            row=4, column=1, padx=5, pady=(4, 10), sticky="ew"
        )
        ctk.CTkButton(timer_frame, text="Reset", command=self.reset_timer).grid(
            row=4, column=2, padx=5, pady=(4, 10), sticky="ew"
        )

    def _build_summary_tab(self, parent) -> None:
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(parent, corner_radius=12)
        header.grid(row=0, column=0, padx=12, pady=12, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header, text="Weekly Summary", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, padx=10, pady=12, sticky="w"
        )
        ctk.CTkButton(header, text="Refresh", command=self.render_summary, width=120).grid(
            row=0, column=2, padx=10, pady=12, sticky="e"
        )

        self.heatmap_panel = ctk.CTkFrame(parent, corner_radius=12)
        self.heatmap_panel.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="ew")
        self.heatmap_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.heatmap_panel, text="Calendar Heatmap (last 12 weeks)", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, padx=10, pady=(10, 4), sticky="w"
        )

        self.heatmap_hint = ctk.CTkLabel(self.heatmap_panel, text="Hover a day square to see details.")
        self.heatmap_hint.grid(row=1, column=0, padx=10, pady=(0, 6), sticky="w")

        self.heatmap_grid = ctk.CTkFrame(self.heatmap_panel, corner_radius=10)
        self.heatmap_grid.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.analytics_panel = ctk.CTkFrame(parent, corner_radius=12)
        self.analytics_panel.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="ew")
        self.analytics_panel.grid_columnconfigure(0, weight=1)
        self.analytics_title = ctk.CTkLabel(
            self.analytics_panel,
            text="Analytics: Streaks + Weekly Trend",
            font=("Segoe UI", 14, "bold"),
        )
        self.analytics_title.grid(row=0, column=0, padx=10, pady=(10, 4), sticky="w")
        self.analytics_stats = ctk.CTkLabel(self.analytics_panel, text="Streak: 0 days")
        self.analytics_stats.grid(row=1, column=0, padx=10, pady=(0, 6), sticky="w")
        self.trend_canvas = tk.Canvas(self.analytics_panel, height=180, highlightthickness=0)
        self.trend_canvas.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.summary_text = ctk.CTkTextbox(parent, corner_radius=12)
        self.summary_text.grid(row=3, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.summary_text.insert("1.0", "Summary will appear here.")
        self.summary_text.configure(state="disabled")

    def _build_pomodoro_tab(self, parent) -> None:
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(parent, corner_radius=12)
        header.grid(row=0, column=0, padx=12, pady=12, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(header, text="Pomodoro History", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, padx=10, pady=12, sticky="w"
        )
        ctk.CTkButton(header, text="Refresh", width=110, command=self.render_pomodoro_history).grid(
            row=0, column=2, padx=10, pady=12, sticky="e"
        )

        self.pomo_stats_label = ctk.CTkLabel(parent, text="No sessions yet.", anchor="w")
        self.pomo_stats_label.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="ew")

        charts = ctk.CTkFrame(parent, corner_radius=12)
        charts.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="ew")
        charts.grid_columnconfigure((0, 1), weight=1)

        self.pomo_day_text = ctk.CTkTextbox(charts, height=150, corner_radius=10)
        self.pomo_day_text.grid(row=0, column=0, padx=(10, 6), pady=10, sticky="ew")
        self.pomo_day_text.insert("1.0", "Daily focus minutes")
        self.pomo_day_text.configure(state="disabled")

        self.pomo_week_text = ctk.CTkTextbox(charts, height=150, corner_radius=10)
        self.pomo_week_text.grid(row=0, column=1, padx=(6, 10), pady=10, sticky="ew")
        self.pomo_week_text.insert("1.0", "Weekly focus minutes")
        self.pomo_week_text.configure(state="disabled")

        self.pomo_recent_text = ctk.CTkTextbox(parent, corner_radius=12)
        self.pomo_recent_text.grid(row=3, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.pomo_recent_text.insert("1.0", "Recent Pomodoro sessions will appear here.")
        self.pomo_recent_text.configure(state="disabled")

    def on_theme_change(self, mode: str) -> None:
        ctk.set_appearance_mode(mode)
        self.render_summary()
        self.render_pomodoro_history()

    def persist_settings(self) -> None:
        self.store.save_settings(
            {
                "rollover_enabled": bool(self.rollover_enabled.get()),
                "font_scale": float(self.font_scale),
            }
        )

    def set_font_scale(self, value: float) -> None:
        self.font_scale = max(0.85, min(1.35, value))
        ctk.set_widget_scaling(self.font_scale)
        ctk.set_window_scaling(self.font_scale)
        self.persist_settings()

    def increase_font_scale(self) -> None:
        self.set_font_scale(self.font_scale + 0.05)

    def decrease_font_scale(self) -> None:
        self.set_font_scale(self.font_scale - 0.05)

    def reset_font_scale(self) -> None:
        self.set_font_scale(1.0)

    def bind_shortcuts(self) -> None:
        self.bind_all("<Control-n>", self.shortcut_focus_task, add="+")
        self.bind_all("<Control-f>", self.shortcut_focus_search, add="+")
        self.bind_all("<Control-s>", self.shortcut_save, add="+")
        self.bind_all("<Control-Left>", lambda _e: self.change_week(-1), add="+")
        self.bind_all("<Control-Right>", lambda _e: self.change_week(1), add="+")
        self.bind_all("<Control-equal>", lambda _e: self.increase_font_scale(), add="+")
        self.bind_all("<Control-plus>", lambda _e: self.increase_font_scale(), add="+")
        self.bind_all("<Control-minus>", lambda _e: self.decrease_font_scale(), add="+")
        self.bind_all("<Control-0>", lambda _e: self.reset_font_scale(), add="+")
        self.bind_all("<Control-Shift-P>", lambda _e: self.open_command_palette(), add="+")
        self.bind_all("<Control-Shift-p>", lambda _e: self.open_command_palette(), add="+")
        self.bind_all("<Control-Return>", lambda _e: self.add_task(), add="+")
        self.bind_all("<Delete>", self.shortcut_delete_selected, add="+")
        self.bind_all("<space>", self.shortcut_toggle_selected, add="+")
        self.bind_all("<KeyPress-question>", self.shortcut_toggle_shortcuts_help, add="+")
        self.bind_all("<F1>", self.shortcut_toggle_shortcuts_help, add="+")

    def shortcut_focus_task(self, _event=None):
        self.task_entry.focus_set()
        return "break"

    def shortcut_focus_search(self, _event=None):
        self.search_entry.focus_set()
        return "break"

    def shortcut_save(self, _event=None):
        self.save_all()
        self.send_notification("Saved", "Checklist saved.")
        return "break"

    def shortcut_delete_selected(self, _event=None):
        if self.selected_task_id:
            self.delete_task(self.selected_task_id)
        return "break"

    def shortcut_toggle_selected(self, _event=None):
        widget = self.focus_get()
        if widget and widget.winfo_class().lower().find("entry") >= 0:
            return
        if self.selected_task_id:
            self.toggle_task(self.selected_task_id)
            return "break"

    def is_text_input_focused(self) -> bool:
        widget = self.focus_get()
        if widget is None:
            return False
        klass = widget.winfo_class().lower()
        return any(token in klass for token in ("entry", "text", "spinbox", "combobox"))

    def shortcut_toggle_shortcuts_help(self, _event=None):
        if self.is_text_input_focused():
            return
        self.open_shortcuts_help(toggle=True)
        return "break"

    def clear_filters(self) -> None:
        self.search_var.set("")
        self.filter_status_var.set("All")
        self.filter_day_var.set("All")
        self.filter_priority_var.set("All")
        self.filter_tag_var.set("")
        self.filter_hours_min_var.set("")
        self.filter_hours_max_var.set("")
        self.sort_var.set(SORT_VALUES[0])
        self.render_tasks()

    def week_start(self, week_key: str) -> datetime:
        return datetime.strptime(week_key, "%Y-%m-%d")

    def is_future_week(self, target_week_key: str) -> bool:
        return self.week_start(target_week_key) > self.week_start(self.current_week_key)

    def update_week_context(self) -> None:
        self.week_picker_var.set(self.current_week_key)
        self.week_label.configure(text=f"Week of {self.current_week_key}")

        days = self.week_day_options()
        self.day_menu.configure(values=days)
        if self.day_menu.get() not in days:
            self.day_menu.set(days[0])

        self.filter_day_menu.configure(values=["All"] + days)
        if self.filter_day_var.get() not in (["All"] + days):
            self.filter_day_var.set("All")

    def go_to_current_week(self) -> None:
        self.change_to_week(self.store.week_key(datetime.now()), allow_rollover=False)

    def go_to_week_from_picker(self) -> None:
        raw = self.week_picker_var.get().strip()
        try:
            dt = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Use YYYY-MM-DD format (e.g., 2026-02-08).")
            return
        self.change_to_week(self.store.week_key(dt), allow_rollover=False)

    def change_week(self, delta_weeks: int) -> None:
        current = self.week_start(self.current_week_key)
        target = self.store.week_key(current + timedelta(days=7 * delta_weeks))
        self.change_to_week(target, allow_rollover=(delta_weeks > 0))

    def rollover_tasks(self, source_tasks: List[Task], target_week_key: str) -> None:
        profile = self.current_profile.get()
        target_tasks = self.store.load_week(profile, target_week_key)
        source_start = self.week_start(self.current_week_key)
        target_start = self.week_start(target_week_key)

        existing_signatures = {
            (t.title.strip().lower(), round(t.hours, 3), t.day, t.tag.strip().lower(), t.priority) for t in target_tasks
        }

        added = 0
        next_order = max((t.order for t in target_tasks), default=-1) + 1
        for idx, task in enumerate(source_tasks):
            if task.completed:
                continue
            try:
                day_obj = datetime.strptime(task.day, "%Y-%m-%d")
                day_offset = max(0, min(6, (day_obj - source_start).days))
            except ValueError:
                day_offset = idx % 7
            new_day = (target_start + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            signature = (task.title.strip().lower(), round(task.hours, 3), new_day, task.tag.strip().lower(), task.priority)
            if signature in existing_signatures:
                continue
            target_tasks.append(
                Task(
                    id=f"task-{int(datetime.now().timestamp() * 1000)}-{idx}",
                    title=task.title,
                    hours=task.hours,
                    day=new_day,
                    completed=False,
                    completed_at=None,
                    order=next_order,
                    tag=task.tag,
                    priority=task.priority,
                )
            )
            next_order += 1
            added += 1

        if added:
            self.store.save_week(profile, target_week_key, target_tasks)

    def rollover_to_next_week_manual(self) -> None:
        source_tasks = [Task(**asdict(t)) for t in self.tasks]
        target = self.store.week_key(self.week_start(self.current_week_key) + timedelta(days=7))
        self.rollover_tasks(source_tasks, target)
        self.send_notification("Rollover complete", f"Unfinished tasks were copied to week {target}.")

    def change_to_week(self, target_week_key: str, allow_rollover: bool) -> None:
        if target_week_key == self.current_week_key:
            self.update_week_context()
            return

        source_tasks = [Task(**asdict(t)) for t in self.tasks]
        previous_week = self.current_week_key
        self.save_all()

        if allow_rollover and self.rollover_enabled.get() and self.week_start(target_week_key) > self.week_start(previous_week):
            self.rollover_tasks(source_tasks, target_week_key)

        self.current_week_key = target_week_key
        self.tasks = self.store.load_week(self.active_profile_name, self.current_week_key)
        self.normalize_task_order()
        self.selected_task_id = None
        self.current_pomodoro_session_id = None
        self.update_week_context()
        self.render_tasks()
        self.refresh_progress()

    def open_calendar_picker(self) -> None:
        if self.calendar_picker_window is not None and self.calendar_picker_window.winfo_exists():
            self.calendar_picker_window.lift()
            return

        picker = ctk.CTkToplevel(self)
        picker.title("Pick Date")
        picker.geometry("320x220")
        picker.resizable(False, False)
        self.calendar_picker_window = picker

        current = datetime.now()
        try:
            current = datetime.strptime(self.week_picker_var.get(), "%Y-%m-%d")
        except ValueError:
            pass

        years = [str(current.year + i) for i in range(-2, 3)]
        months = [f"{m:02d}" for m in range(1, 13)]
        days = [f"{d:02d}" for d in range(1, 32)]

        year_var = ctk.StringVar(value=str(current.year))
        month_var = ctk.StringVar(value=f"{current.month:02d}")
        day_var = ctk.StringVar(value=f"{current.day:02d}")

        ctk.CTkLabel(picker, text="Calendar Picker", font=("Segoe UI", 16, "bold")).pack(pady=(14, 10))
        grid = ctk.CTkFrame(picker)
        grid.pack(fill="x", padx=14, pady=6)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkOptionMenu(grid, values=years, variable=year_var).grid(row=0, column=0, padx=4, pady=8, sticky="ew")
        ctk.CTkOptionMenu(grid, values=months, variable=month_var).grid(row=0, column=1, padx=4, pady=8, sticky="ew")
        ctk.CTkOptionMenu(grid, values=days, variable=day_var).grid(row=0, column=2, padx=4, pady=8, sticky="ew")

        def apply_date():
            try:
                picked = datetime.strptime(f"{year_var.get()}-{month_var.get()}-{day_var.get()}", "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date", "Selected date is not valid.")
                return
            self.week_picker_var.set(picked.strftime("%Y-%m-%d"))
            self.go_to_week_from_picker()
            self.calendar_picker_window = None
            picker.destroy()

        btns = ctk.CTkFrame(picker, fg_color="transparent")
        btns.pack(fill="x", padx=14, pady=(10, 8))
        btns.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(btns, text="Use Date", command=apply_date).grid(row=0, column=0, padx=4, pady=6, sticky="ew")
        ctk.CTkButton(
            btns,
            text="Cancel",
            command=lambda: (setattr(self, "calendar_picker_window", None), picker.destroy()),
        ).grid(row=0, column=1, padx=4, pady=6, sticky="ew")

        picker.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, "calendar_picker_window", None), picker.destroy()))

    def open_command_palette(self) -> None:
        if self.command_palette_window is not None and self.command_palette_window.winfo_exists():
            self.command_palette_window.lift()
            return

        palette = ctk.CTkToplevel(self)
        palette.title("Command Palette")
        palette.geometry("520x420")
        palette.resizable(False, False)
        self.command_palette_window = palette

        query_var = ctk.StringVar(value="")
        ctk.CTkLabel(palette, text="Command Palette (Ctrl+Shift+P)", font=("Segoe UI", 16, "bold")).pack(
            padx=12, pady=(12, 8), anchor="w"
        )
        entry = ctk.CTkEntry(
            palette,
            textvariable=query_var,
            placeholder_text="Type a command or quick add: task:Title|2|Tag|High|2026-02-08",
            height=36,
        )
        entry.pack(fill="x", padx=12, pady=(0, 10))

        list_frame = ctk.CTkScrollableFrame(palette, corner_radius=10)
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        commands = [
            ("Next Week", lambda: self.change_week(1)),
            ("Previous Week", lambda: self.change_week(-1)),
            ("Go To Current Week", self.go_to_current_week),
            ("Start Pomodoro", self.start_pomodoro),
            ("Pause Timer", self.pause_timer),
            ("Open Summary Tab", lambda: self.body.set("Summary")),
            ("Open Pomodoro Tab", lambda: self.body.set("Pomodoro")),
            ("Open Tasks Tab", lambda: self.body.set("Tasks")),
            ("Save Now", self.save_all),
            ("Increase Font Scale", self.increase_font_scale),
            ("Decrease Font Scale", self.decrease_font_scale),
            ("Reset Font Scale", self.reset_font_scale),
            ("Toggle Mini Hover", self.open_mini_hover),
            ("Show Shortcuts Help", self.open_shortcuts_help),
            ("Roll Over To Next Week", self.rollover_to_next_week_manual),
        ]

        def run_command(action):
            action()
            self.command_palette_window = None
            palette.destroy()

        def refresh_commands(*_args):
            for child in list_frame.winfo_children():
                child.destroy()
            query = query_var.get().strip().lower()

            if query.startswith("task:"):
                ctk.CTkLabel(
                    list_frame,
                    text="Quick Add Format: task:Title|Hours|Tag|Priority|YYYY-MM-DD",
                    text_color=("#4b5563", "#9ca3af"),
                ).pack(anchor="w", padx=8, pady=(8, 4))
                ctk.CTkButton(list_frame, text=f"Run '{query_var.get()}'", command=lambda: self.run_palette_quick_add(query_var.get(), palette)).pack(
                    fill="x", padx=8, pady=6
                )
                return

            shown = 0
            for name, action in commands:
                if query and query not in name.lower():
                    continue
                ctk.CTkButton(list_frame, text=name, anchor="w", command=lambda act=action: run_command(act)).pack(
                    fill="x", padx=8, pady=4
                )
                shown += 1
            if shown == 0:
                ctk.CTkLabel(list_frame, text="No command matches.", text_color=("#6b7280", "#9ca3af")).pack(
                    anchor="w", padx=8, pady=8
                )

        query_var.trace_add("write", refresh_commands)
        refresh_commands()
        entry.focus_set()
        palette.bind("<Escape>", lambda _e: (setattr(self, "command_palette_window", None), palette.destroy()))
        palette.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, "command_palette_window", None), palette.destroy()))

    def close_shortcuts_help(self) -> None:
        if self.shortcuts_help_window is not None and self.shortcuts_help_window.winfo_exists():
            self.shortcuts_help_window.destroy()
        self.shortcuts_help_window = None

    def open_shortcuts_help(self, toggle: bool = False) -> None:
        if self.shortcuts_help_window is not None and self.shortcuts_help_window.winfo_exists():
            if toggle:
                self.close_shortcuts_help()
                return
            self.shortcuts_help_window.lift()
            self.shortcuts_help_window.focus_force()
            return

        overlay = ctk.CTkToplevel(self)
        overlay.title("Shortcuts Help")
        overlay.geometry("560x500")
        overlay.minsize(500, 400)
        self.shortcuts_help_window = overlay

        root = ctk.CTkFrame(overlay, corner_radius=14)
        root.pack(fill="both", expand=True, padx=10, pady=10)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        head = ctk.CTkFrame(root, corner_radius=12)
        head.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="ew")
        head.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(head, text="Keyboard Shortcuts", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, padx=12, pady=(10, 2), sticky="w"
        )
        ctk.CTkLabel(
            head,
            text="Press ? (or F1) to toggle this panel.",
            text_color=("#4b5563", "#9ca3af"),
        ).grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")
        ctk.CTkButton(head, text="Close", width=72, command=self.close_shortcuts_help).grid(
            row=0, column=1, rowspan=2, padx=10, pady=8, sticky="e"
        )

        scroll = ctk.CTkScrollableFrame(root, corner_radius=12)
        scroll.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        sections = [
            (
                "Global",
                [
                    ("?", "Toggle shortcuts help"),
                    ("Ctrl+Shift+P", "Open command palette"),
                    ("Ctrl+S", "Save all data now"),
                    ("Esc", "Close open popup windows"),
                ],
            ),
            (
                "Tasks",
                [
                    ("Ctrl+N", "Focus new task input"),
                    ("Ctrl+Enter", "Add task"),
                    ("Ctrl+F", "Focus search"),
                    ("Space", "Toggle selected task"),
                    ("Delete", "Delete selected task"),
                    ("Drag handle (⋮⋮)", "Reorder tasks manually"),
                ],
            ),
            (
                "Week Navigation",
                [
                    ("Ctrl+Left", "Previous week"),
                    ("Ctrl+Right", "Next week"),
                    ("Today button", "Jump to current week"),
                    ("Pick button", "Open calendar picker"),
                ],
            ),
            (
                "Accessibility",
                [
                    ("Ctrl++", "Increase UI scale"),
                    ("Ctrl+-", "Decrease UI scale"),
                    ("Ctrl+0", "Reset UI scale"),
                ],
            ),
            (
                "Timers",
                [
                    ("Palette: Start Pomodoro", "Start focus timer quickly"),
                    ("Palette: Pause Timer", "Pause active timer"),
                    ("Mini Hover", "Keep timer and progress on top"),
                ],
            ),
        ]

        for section, rows in sections:
            card = ctk.CTkFrame(scroll, corner_radius=10)
            card.pack(fill="x", padx=8, pady=6)
            ctk.CTkLabel(card, text=section, font=("Segoe UI", 14, "bold")).pack(
                anchor="w", padx=10, pady=(8, 4)
            )
            for combo, desc in rows:
                row = ctk.CTkFrame(card, fg_color="transparent")
                row.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(row, text=combo, width=200, anchor="w", font=("JetBrains Mono", 12)).pack(
                    side="left"
                )
                ctk.CTkLabel(row, text=desc, anchor="w", text_color=("#4b5563", "#9ca3af")).pack(
                    side="left", fill="x", expand=True
                )

        overlay.bind("<Escape>", lambda _e: self.close_shortcuts_help())
        overlay.protocol("WM_DELETE_WINDOW", self.close_shortcuts_help)

    def run_palette_quick_add(self, raw: str, palette_window) -> None:
        try:
            payload = raw.split(":", 1)[1]
            parts = [x.strip() for x in payload.split("|")]
            title = parts[0]
            if not title:
                raise ValueError("missing title")
            hours = float(parts[1]) if len(parts) > 1 and parts[1] else 1.0
            tag = parts[2] if len(parts) > 2 else ""
            priority = parts[3] if len(parts) > 3 and parts[3] in PRIORITY_VALUES else "Medium"
            day = parts[4] if len(parts) > 4 else self.parse_selected_day()
            day_obj = datetime.strptime(day, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Quick Add Error", "Use: task:Title|Hours|Tag|Priority|YYYY-MM-DD")
            return

        target_week = self.store.week_key(day_obj)
        if target_week != self.current_week_key:
            self.change_to_week(target_week, allow_rollover=False)
        self.create_task(title=title, hours=hours, day=day, tag=tag, priority=priority)
        self.command_palette_window = None
        palette_window.destroy()

    def week_day_options(self) -> List[str]:
        ws = datetime.strptime(self.current_week_key, "%Y-%m-%d")
        return [(ws + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    def parse_selected_day(self) -> str:
        return self.day_menu.get()

    def normalize_task_order(self) -> None:
        def safe_order(task: Task) -> int:
            try:
                return int(task.order)
            except (TypeError, ValueError):
                return 10**9

        ordered = sorted(self.tasks, key=lambda x: (safe_order(x), x.day, x.completed, x.title.lower(), x.id))
        for idx, task in enumerate(ordered):
            task.order = idx
        self.tasks = ordered

    def ordered_tasks(self) -> List[Task]:
        return sorted(self.tasks, key=lambda x: x.order)

    def add_profile(self) -> None:
        name = self.new_profile_entry.get().strip()
        if not name:
            return
        if name in self.profiles:
            self.current_profile.set(name)
            self.on_profile_change(name)
            return
        self.store.save_week(self.active_profile_name, self.current_week_key, self.tasks)
        self.store.save_pomodoro_history(self.active_profile_name, self.pomodoro_history)
        self.profiles.append(name)
        self.store.save_profiles(self.profiles)
        self.profile_menu.configure(values=self.profiles)
        self.current_profile.set(name)
        self.active_profile_name = name
        self.new_profile_entry.delete(0, "end")
        self.tasks = self.store.load_week(name, self.current_week_key)
        self.pomodoro_history = self.store.load_pomodoro_history(name)
        self.current_pomodoro_session_id = None
        self.normalize_task_order()
        self.update_week_context()
        self.render_tasks()
        self.refresh_progress()

    def on_profile_change(self, profile: str) -> None:
        if profile != self.active_profile_name:
            self.store.save_week(self.active_profile_name, self.current_week_key, self.tasks)
            self.store.save_pomodoro_history(self.active_profile_name, self.pomodoro_history)
            self.persist_settings()
            self.active_profile_name = profile
        self.tasks = self.store.load_week(profile, self.current_week_key)
        self.pomodoro_history = self.store.load_pomodoro_history(profile)
        self.current_pomodoro_session_id = None
        self.normalize_task_order()
        self.selected_task_id = None
        self.update_week_context()
        self.render_tasks()
        self.refresh_progress()

    def create_task(self, title: str, hours: float, day: str, tag: str, priority: str) -> None:
        if priority not in PRIORITY_VALUES:
            priority = "Medium"
        next_order = max((t.order for t in self.tasks), default=-1) + 1
        self.tasks.append(
            Task(
                id=f"task-{int(datetime.now().timestamp() * 1000)}",
                title=title.strip(),
                hours=float(hours),
                day=day,
                completed=False,
                completed_at=None,
                order=next_order,
                tag=tag.strip(),
                priority=priority,
            )
        )
        self.selected_task_id = self.tasks[-1].id
        self.render_tasks()
        self.refresh_progress()
        self.save_all()

    def add_task(self) -> None:
        title = self.task_entry.get().strip()
        hours_raw = self.hours_entry.get().strip()
        day = self.parse_selected_day()
        tag = self.tag_entry.get().strip()
        priority = self.priority_menu.get()
        if not title:
            return
        try:
            hours = float(hours_raw)
            if hours <= 0:
                raise ValueError
        except Exception:
            self.hours_entry.delete(0, "end")
            self.hours_entry.insert(0, "1")
            return

        self.create_task(title=title, hours=hours, day=day, tag=tag, priority=priority)
        self.task_entry.delete(0, "end")
        self.hours_entry.delete(0, "end")
        self.tag_entry.delete(0, "end")

    def toggle_task(self, task_id: str) -> None:
        completed_title: Optional[str] = None
        for t in self.tasks:
            if t.id == task_id:
                t.completed = not t.completed
                t.completed_at = datetime.now().isoformat() if t.completed else None
                if t.completed:
                    completed_title = t.title
                break
        self.render_tasks()
        self.refresh_progress()
        self.save_all()
        if completed_title:
            self.send_notification("Task Completed", f"{completed_title} marked as finished.")

    def delete_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if self.selected_task_id == task_id:
            self.selected_task_id = None
        self.normalize_task_order()
        self.render_tasks()
        self.refresh_progress()
        self.save_all()

    def start_task_drag(self, _event, task_id: str) -> None:
        if not self.can_reorder_manually():
            return
        self.dragging_task_id = task_id
        card = self.task_card_refs.get(task_id)
        if card is not None:
            card.configure(border_width=2, border_color=("#2563eb", "#60a5fa"))

    def finish_task_drag(self, event) -> None:
        if not self.dragging_task_id:
            return
        source_id = self.dragging_task_id
        self.dragging_task_id = None
        self.reorder_task_by_drop(source_id, event.y_root)

    def reorder_task_by_drop(self, task_id: str, drop_root_y: int) -> None:
        if not self.can_reorder_manually():
            self.render_tasks()
            return
        ordered = self.ordered_tasks()
        if len(ordered) < 2:
            self.render_tasks()
            return

        try:
            source_index = next(i for i, t in enumerate(ordered) if t.id == task_id)
        except StopIteration:
            self.render_tasks()
            return

        self.update_idletasks()
        target_index = source_index
        min_distance = float("inf")

        for idx, task in enumerate(ordered):
            card = self.task_card_refs.get(task.id)
            if card is None:
                continue
            center_y = card.winfo_rooty() + (card.winfo_height() / 2)
            distance = abs(center_y - drop_root_y)
            if distance < min_distance:
                min_distance = distance
                target_index = idx

        if target_index != source_index:
            moved = ordered.pop(source_index)
            ordered.insert(target_index, moved)
            for idx, task in enumerate(ordered):
                task.order = idx
            self.tasks = ordered
            self.save_all()

        self.render_tasks()

    def can_reorder_manually(self) -> bool:
        if self.sort_var.get() != "Manual":
            return False
        if self.search_var.get().strip():
            return False
        if self.filter_status_var.get() != "All":
            return False
        if self.filter_day_var.get() != "All":
            return False
        if self.filter_priority_var.get() != "All":
            return False
        if self.filter_tag_var.get().strip():
            return False
        if self.filter_hours_min_var.get().strip() or self.filter_hours_max_var.get().strip():
            return False
        return True

    def priority_rank(self, priority: str) -> int:
        return {"High": 0, "Medium": 1, "Low": 2}.get(priority, 1)

    def filtered_sorted_tasks(self) -> List[Task]:
        tasks = list(self.ordered_tasks())
        keyword = self.search_var.get().strip().lower()
        status = self.filter_status_var.get()
        day = self.filter_day_var.get()
        priority = self.filter_priority_var.get()
        tag = self.filter_tag_var.get().strip().lower()
        min_raw = self.filter_hours_min_var.get().strip()
        max_raw = self.filter_hours_max_var.get().strip()

        min_hours: Optional[float] = None
        max_hours: Optional[float] = None
        try:
            if min_raw:
                min_hours = float(min_raw)
        except ValueError:
            min_hours = None
        try:
            if max_raw:
                max_hours = float(max_raw)
        except ValueError:
            max_hours = None

        def include(task: Task) -> bool:
            if status == "Todo" and task.completed:
                return False
            if status == "Done" and not task.completed:
                return False
            if day != "All" and task.day != day:
                return False
            if priority != "All" and task.priority != priority:
                return False
            if min_hours is not None and task.hours < min_hours:
                return False
            if max_hours is not None and task.hours > max_hours:
                return False
            if tag and tag not in task.tag.lower():
                return False
            if keyword:
                haystack = f"{task.title} {task.tag} {task.priority} {task.day}".lower()
                if keyword not in haystack:
                    return False
            return True

        filtered = [task for task in tasks if include(task)]
        sort_mode = self.sort_var.get()
        if sort_mode == "Day":
            filtered.sort(key=lambda x: (x.day, x.order))
        elif sort_mode == "Hours ↑":
            filtered.sort(key=lambda x: (x.hours, x.order))
        elif sort_mode == "Hours ↓":
            filtered.sort(key=lambda x: (-x.hours, x.order))
        elif sort_mode == "Priority":
            filtered.sort(key=lambda x: (self.priority_rank(x.priority), x.order))
        elif sort_mode == "Status":
            filtered.sort(key=lambda x: (x.completed, x.order))
        return filtered

    def select_task(self, task_id: str) -> None:
        self.selected_task_id = task_id
        self.render_tasks()

    def render_tasks(self) -> None:
        for child in self.task_list_frame.winfo_children():
            child.destroy()
        self.task_card_refs = {}

        filtered_tasks = self.filtered_sorted_tasks()
        if not filtered_tasks:
            ctk.CTkLabel(
                self.task_list_frame,
                text="No matching tasks. Adjust filters or add a new task.",
                text_color=("#4b5563", "#9ca3af"),
            ).pack(anchor="w", padx=8, pady=8)
            return

        for task in filtered_tasks:
            card = ctk.CTkFrame(self.task_list_frame, corner_radius=12)
            card.pack(fill="x", padx=6, pady=6)
            card.grid_columnconfigure(2, weight=1)
            self.task_card_refs[task.id] = card

            drag_handle = ctk.CTkLabel(
                card,
                text="⋮⋮",
                width=22,
                font=("JetBrains Mono", 18, "bold"),
                text_color=("#374151", "#9ca3af"),
            )
            drag_handle.grid(row=0, column=0, padx=(10, 4), pady=10, sticky="ns")
            drag_handle.bind("<ButtonPress-1>", lambda e, tid=task.id: self.start_task_drag(e, tid))

            check = ctk.CTkCheckBox(card, text="", width=24, command=lambda tid=task.id: self.toggle_task(tid))
            check.grid(row=0, column=1, padx=(2, 6), pady=10)
            if task.completed:
                check.select()
            else:
                check.deselect()

            title_font = ("Segoe UI", 15, "normal")
            color = ("#111827", "#f3f4f6")
            if task.completed:
                title_font = ("Segoe UI", 15, "overstrike")
                color = ("#6b7280", "#9ca3af")

            if self.selected_task_id == task.id:
                card.configure(border_width=2, border_color=("#10b981", "#34d399"))
            else:
                card.configure(border_width=0)

            text_wrap = ctk.CTkFrame(card, fg_color="transparent")
            text_wrap.grid(row=0, column=2, padx=6, pady=8, sticky="ew")
            text_wrap.grid_columnconfigure(0, weight=1)

            title_lbl = ctk.CTkLabel(text_wrap, text=task.title, anchor="w", font=title_font, text_color=color)
            title_lbl.grid(row=0, column=0, sticky="ew")
            title_lbl.bind("<Button-1>", lambda _e, tid=task.id: self.select_task(tid))

            meta_lbl = ctk.CTkLabel(
                text_wrap,
                text=f"{task.hours:g}h • {task.day} • {task.priority} • {task.tag or 'No tag'}",
                anchor="w",
                text_color=("#6b7280", "#9ca3af"),
            )
            meta_lbl.grid(row=1, column=0, sticky="ew")
            meta_lbl.bind("<Button-1>", lambda _e, tid=task.id: self.select_task(tid))
            card.bind("<Button-1>", lambda _e, tid=task.id: self.select_task(tid))

            del_btn = ctk.CTkButton(card, text="Delete", width=80, command=lambda tid=task.id: self.delete_task(tid))
            del_btn.grid(row=0, column=3, padx=(6, 10), pady=10)

    def refresh_progress(self) -> None:
        total_hours = sum(t.hours for t in self.tasks)
        done_hours = sum(t.hours for t in self.tasks if t.completed)
        pct = (done_hours / total_hours * 100) if total_hours else 0
        self.week_progress.set(pct / 100)
        self.week_pct_label.configure(text=f"Weekly completion: {pct:.1f}% ({done_hours:.1f}h/{total_hours:.1f}h)")

        days = self.week_day_options()
        for i, day in enumerate(days):
            day_total = sum(t.hours for t in self.tasks if t.day == day)
            day_done = sum(t.hours for t in self.tasks if t.day == day and t.completed)
            day_pct = (day_done / day_total * 100) if day_total else 0
            if i < len(self.daily_rows):
                self.daily_rows[i].configure(text=f"{day}: {day_pct:.1f}%")

        self.render_summary()
        self.render_pomodoro_history()
        self.refresh_mini_hover()

    def day_completion_pct(self, tasks: List[Task], day: str) -> float:
        day_total = sum(t.hours for t in tasks if t.day == day)
        day_done = sum(t.hours for t in tasks if t.day == day and t.completed)
        return (day_done / day_total * 100) if day_total else 0

    def heatmap_color(self, pct: float):
        light_palette = ["#e5e7eb", "#bfdbfe", "#93c5fd", "#60a5fa", "#2563eb"]
        dark_palette = ["#1f2937", "#1e3a8a", "#1d4ed8", "#2563eb", "#60a5fa"]
        palette = dark_palette if ctk.get_appearance_mode().lower() == "dark" else light_palette
        if pct <= 0:
            idx = 0
        elif pct < 25:
            idx = 1
        elif pct < 50:
            idx = 2
        elif pct < 75:
            idx = 3
        else:
            idx = 4
        return palette[idx]

    def render_heatmap(self, weeks: Dict[str, List[Task]]) -> None:
        for child in self.heatmap_grid.winfo_children():
            child.destroy()

        if not weeks:
            ctk.CTkLabel(self.heatmap_grid, text="No data yet for heatmap.").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            return

        week_keys = sorted(weeks.keys())[-12:]
        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        ctk.CTkLabel(self.heatmap_grid, text="", width=44).grid(row=0, column=0, padx=(8, 4), pady=(6, 2), sticky="w")
        for col, week_key in enumerate(week_keys, start=1):
            try:
                week_start = datetime.strptime(week_key, "%Y-%m-%d")
                week_label = week_start.strftime("%m/%d")
            except ValueError:
                week_start = None
                week_label = week_key[-5:]
            ctk.CTkLabel(self.heatmap_grid, text=week_label, text_color=("#6b7280", "#9ca3af")).grid(
                row=0, column=col, padx=3, pady=(6, 2)
            )

            for row, day_name in enumerate(day_labels, start=1):
                if col == 1:
                    ctk.CTkLabel(self.heatmap_grid, text=day_name, text_color=("#6b7280", "#9ca3af")).grid(
                        row=row, column=0, padx=(8, 4), pady=3, sticky="w"
                    )
                day_str = (
                    (week_start + timedelta(days=row - 1)).strftime("%Y-%m-%d")
                    if week_start is not None
                    else day_name
                )
                pct = self.day_completion_pct(weeks[week_key], day_str)
                cell = ctk.CTkLabel(
                    self.heatmap_grid,
                    text="",
                    width=20,
                    height=20,
                    fg_color=self.heatmap_color(pct),
                    corner_radius=4,
                )
                cell.grid(row=row, column=col, padx=3, pady=3)
                cell.bind(
                    "<Enter>",
                    lambda _e, day=day_str, percent=pct: self.heatmap_hint.configure(
                        text=f"{day}: {percent:.1f}% completed"
                    ),
                )

        ctk.CTkLabel(
            self.heatmap_grid,
            text="Legend: 0%, 1-24%, 25-49%, 50-74%, 75-100%",
            text_color=("#6b7280", "#9ca3af"),
        ).grid(row=8, column=0, columnspan=len(week_keys) + 1, padx=8, pady=(6, 8), sticky="w")

    def render_analytics(self, weeks: Dict[str, List[Task]]) -> None:
        day_done: Dict[str, float] = {}
        for tasks in weeks.values():
            for task in tasks:
                if task.completed:
                    day_done[task.day] = day_done.get(task.day, 0.0) + task.hours

        streak = 0
        cursor = datetime.now()
        while day_done.get(cursor.strftime("%Y-%m-%d"), 0) > 0:
            streak += 1
            cursor -= timedelta(days=1)

        points: List[Dict[str, object]] = []
        for wk in sorted(weeks.keys())[-8:]:
            tasks = weeks[wk]
            total = sum(t.hours for t in tasks)
            done = sum(t.hours for t in tasks if t.completed)
            pct = (done / total * 100) if total else 0
            points.append({"week": wk, "total": total, "done": done, "pct": pct})

        if points:
            latest = points[-1]
            self.analytics_stats.configure(
                text=(
                    f"Streak: {streak} day(s) • Latest week: {latest['done']:.1f}h/"
                    f"{latest['total']:.1f}h ({latest['pct']:.1f}%)"
                )
            )
        else:
            self.analytics_stats.configure(text=f"Streak: {streak} day(s) • No weekly trend data")

        canvas = self.trend_canvas
        canvas.delete("all")
        width = max(420, canvas.winfo_width() or 420)
        height = max(180, canvas.winfo_height() or 180)
        canvas.configure(
            bg="#0f172a" if ctk.get_appearance_mode().lower() == "dark" else "#f8fafc",
            highlightbackground="#334155" if ctk.get_appearance_mode().lower() == "dark" else "#cbd5e1",
        )
        if not points:
            canvas.create_text(width / 2, height / 2, text="No trend data yet", fill="#94a3b8")
            return

        left = 36
        bottom = height - 26
        max_total = max(float(p["total"]) for p in points) or 1.0
        slot = (width - left - 16) / max(len(points), 1)
        bar_w = max(12, int(slot * 0.5))
        pct_points = []

        for idx, point in enumerate(points):
            x = left + (idx * slot) + 6
            total_h = int((float(point["total"]) / max_total) * (height - 56))
            done_h = int((float(point["done"]) / max_total) * (height - 56))
            y_total = bottom - total_h
            y_done = bottom - done_h

            canvas.create_rectangle(x, y_total, x + bar_w, bottom, outline="#64748b", width=1)
            canvas.create_rectangle(x + 2, y_done, x + bar_w - 2, bottom, fill="#2563eb", outline="")
            canvas.create_text(x + (bar_w / 2), bottom + 10, text=str(point["week"])[5:], fill="#94a3b8", font=("Segoe UI", 8))

            pct_y = bottom - (float(point["pct"]) / 100.0) * (height - 56)
            pct_points.append((x + (bar_w / 2), pct_y))

        if len(pct_points) > 1:
            flat = []
            for px, py in pct_points:
                flat.extend([px, py])
            canvas.create_line(*flat, fill="#10b981", width=2, smooth=True)

        canvas.create_text(
            left + 8,
            12,
            text="Blue: completed/planned hours bars • Green: completion %",
            anchor="w",
            fill="#94a3b8",
            font=("Segoe UI", 8),
        )

    def render_summary(self) -> None:
        weeks = self.store.load_all_weeks(self.active_profile_name)
        weeks[self.current_week_key] = [Task(**asdict(t)) for t in self.ordered_tasks()]
        self.render_heatmap(weeks)
        self.render_analytics(weeks)

        lines = [f"Profile: {self.current_profile.get()}", ""]
        if not weeks:
            lines.append("No weekly data available yet.")
        else:
            for wk in sorted(weeks.keys(), reverse=True):
                tasks = weeks[wk]
                total = sum(t.hours for t in tasks)
                done = sum(t.hours for t in tasks if t.completed)
                pct = (done / total * 100) if total else 0
                done_count = len([t for t in tasks if t.completed])
                lines.append(f"Week {wk} -> {pct:.1f}% complete | {done:.1f}h/{total:.1f}h | tasks {done_count}/{len(tasks)}")

        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", "\n".join(lines))
        self.summary_text.configure(state="disabled")

    def render_pomodoro_history(self) -> None:
        started = len(self.pomodoro_history)
        completed = len([x for x in self.pomodoro_history if bool(x.get("completed"))])
        success = (completed / started * 100) if started else 0

        day_totals: Dict[str, int] = {}
        week_totals: Dict[str, int] = {}
        for row in self.pomodoro_history:
            if not bool(row.get("completed")):
                continue
            day = str(row.get("date", ""))
            week = str(row.get("week_key", ""))
            minutes = int(row.get("focus_minutes", 0))
            day_totals[day] = day_totals.get(day, 0) + minutes
            week_totals[week] = week_totals.get(week, 0) + minutes

        current_week_minutes = week_totals.get(self.current_week_key, 0)
        self.pomo_stats_label.configure(
            text=(
                f"Sessions started: {started} • completed: {completed} • success: {success:.1f}%"
                f" • focus this week: {current_week_minutes} min"
            )
        )

        day_lines = ["Daily focus minutes (last 14 days):", ""]
        for i in range(13, -1, -1):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            mins = day_totals.get(day, 0)
            bars = "█" * min(24, max(0, mins // 10))
            day_lines.append(f"{day}: {mins:>3}m {bars}")
        self.pomo_day_text.configure(state="normal")
        self.pomo_day_text.delete("1.0", "end")
        self.pomo_day_text.insert("1.0", "\n".join(day_lines))
        self.pomo_day_text.configure(state="disabled")

        week_lines = ["Weekly focus minutes (last 12 weeks):", ""]
        for wk in sorted(week_totals.keys())[-12:]:
            mins = week_totals.get(wk, 0)
            bars = "█" * min(24, max(0, mins // 20))
            week_lines.append(f"{wk}: {mins:>4}m {bars}")
        if len(week_lines) == 2:
            week_lines.append("No completed sessions yet.")
        self.pomo_week_text.configure(state="normal")
        self.pomo_week_text.delete("1.0", "end")
        self.pomo_week_text.insert("1.0", "\n".join(week_lines))
        self.pomo_week_text.configure(state="disabled")

        recent_lines = ["Recent Pomodoro Sessions:", ""]
        for row in sorted(self.pomodoro_history, key=lambda x: str(x.get("started_at", "")), reverse=True)[:25]:
            marker = "✓" if bool(row.get("completed")) else "•"
            recent_lines.append(
                f"{marker} {row.get('started_at', '')[:19]} | {row.get('focus_minutes', 0)}m | {row.get('preset', '')}"
            )
        if len(recent_lines) == 2:
            recent_lines.append("No sessions recorded yet.")
        self.pomo_recent_text.configure(state="normal")
        self.pomo_recent_text.delete("1.0", "end")
        self.pomo_recent_text.insert("1.0", "\n".join(recent_lines))
        self.pomo_recent_text.configure(state="disabled")

    def send_notification(self, title: str, message: str) -> None:
        if not self.notifications_enabled.get():
            return
        if desktop_notification is not None:
            try:
                desktop_notification.notify(title=title, message=message, app_name=APP_NAME, timeout=5)
                return
            except Exception:
                pass
        try:
            self.bell()
        except TclError:
            pass

    def save_all(self) -> None:
        self.store.save_week(self.active_profile_name, self.current_week_key, self.tasks)
        self.store.save_pomodoro_history(self.active_profile_name, self.pomodoro_history)
        self.persist_settings()

    def on_close(self) -> None:
        if self.mini_hover_window is not None and self.mini_hover_window.winfo_exists():
            self.mini_hover_window.destroy()
        if self.command_palette_window is not None and self.command_palette_window.winfo_exists():
            self.command_palette_window.destroy()
        if self.calendar_picker_window is not None and self.calendar_picker_window.winfo_exists():
            self.calendar_picker_window.destroy()
        if self.shortcuts_help_window is not None and self.shortcuts_help_window.winfo_exists():
            self.shortcuts_help_window.destroy()
        self.save_all()
        self.destroy()

    def update_clock(self) -> None:
        self.clock_lbl.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.refresh_mini_hover()
        self.after(1000, self.update_clock)

    def format_timer(self, seconds: int) -> str:
        seconds = max(0, int(seconds))
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def begin_pomodoro_session(self) -> None:
        focus_seconds, _ = POMODORO_PRESETS[self.active_pomodoro_preset]
        focus_minutes = int(focus_seconds // 60)
        session_id = f"pomo-{int(datetime.now().timestamp() * 1000)}"
        self.current_pomodoro_session_id = session_id
        self.pomodoro_history.append(
            {
                "id": session_id,
                "started_at": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "week_key": self.current_week_key,
                "preset": self.active_pomodoro_preset,
                "focus_minutes": focus_minutes,
                "completed": False,
            }
        )
        self.store.save_pomodoro_history(self.active_profile_name, self.pomodoro_history)
        self.render_pomodoro_history()

    def complete_pomodoro_session(self) -> None:
        if not self.current_pomodoro_session_id:
            return
        for row in reversed(self.pomodoro_history):
            if str(row.get("id")) == self.current_pomodoro_session_id and not bool(row.get("completed")):
                row["completed"] = True
                row["completed_at"] = datetime.now().isoformat()
                break
        self.current_pomodoro_session_id = None
        self.store.save_pomodoro_history(self.active_profile_name, self.pomodoro_history)
        self.render_pomodoro_history()

    def abandon_pomodoro_session(self) -> None:
        self.current_pomodoro_session_id = None

    def on_pomodoro_preset_change(self, _preset: str) -> None:
        if self.timer_mode in {"pomodoro_focus", "pomodoro_break"} and not self.timer_running:
            self.start_pomodoro(reset=True)

    def start_pomodoro(self, reset: bool = False) -> None:
        self.active_pomodoro_preset = self.pomodoro_preset.get()
        focus_seconds, _break_seconds = POMODORO_PRESETS[self.active_pomodoro_preset]
        if reset or self.timer_mode not in {"pomodoro_focus", "pomodoro_break"}:
            self.timer_seconds = focus_seconds
            self.timer_mode = "pomodoro_focus"
            self.begin_pomodoro_session()
        elif self.timer_mode == "pomodoro_focus" and not self.current_pomodoro_session_id:
            self.begin_pomodoro_session()
        self.timer_running = True
        self.timer_mode_label.configure(text=f"Mode: {self.active_pomodoro_preset} | Focus")
        self.timer_lbl.configure(text=self.format_timer(self.timer_seconds))
        self.refresh_mini_hover()

    def start_timer(self) -> None:
        if self.timer_mode in {"pomodoro_focus", "pomodoro_break"}:
            self.abandon_pomodoro_session()
        if self.timer_mode != "stopwatch":
            self.timer_mode = "stopwatch"
            self.timer_seconds = 0
        self.timer_running = True
        self.timer_mode_label.configure(text="Mode: Stopwatch")
        self.timer_lbl.configure(text=self.format_timer(self.timer_seconds))
        self.refresh_mini_hover()

    def pause_timer(self) -> None:
        self.timer_running = False
        self.refresh_mini_hover()

    def reset_timer(self) -> None:
        self.timer_running = False
        if self.timer_mode in {"pomodoro_focus", "pomodoro_break"}:
            self.abandon_pomodoro_session()
        self.timer_mode = "stopwatch"
        self.timer_seconds = 0
        self.timer_mode_label.configure(text="Mode: Stopwatch")
        self.timer_lbl.configure(text="00:00:00")
        self.refresh_mini_hover()

    def on_pomodoro_tick(self) -> None:
        focus_seconds, break_seconds = POMODORO_PRESETS[self.active_pomodoro_preset]
        if self.timer_mode == "pomodoro_focus":
            if self.timer_seconds <= 0:
                self.complete_pomodoro_session()
                self.timer_mode = "pomodoro_break"
                self.timer_seconds = break_seconds
                self.timer_mode_label.configure(text=f"Mode: {self.active_pomodoro_preset} | Break")
                self.send_notification("Focus Complete", f"Take a {break_seconds // 60}-minute break.")
        elif self.timer_mode == "pomodoro_break":
            if self.timer_seconds <= 0:
                self.timer_mode = "pomodoro_focus"
                self.timer_seconds = focus_seconds
                self.begin_pomodoro_session()
                self.timer_mode_label.configure(text=f"Mode: {self.active_pomodoro_preset} | Focus")
                self.send_notification("Break Complete", f"Next {focus_seconds // 60}-minute focus session started.")

    def update_timer(self) -> None:
        if self.timer_running:
            if self.timer_mode == "stopwatch":
                self.timer_seconds += 1
            else:
                self.timer_seconds -= 1
                self.on_pomodoro_tick()
            self.timer_lbl.configure(text=self.format_timer(self.timer_seconds))
        self.refresh_mini_hover()
        self.after(1000, self.update_timer)

    def toggle_fullscreen(self) -> None:
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.fullscreen_btn.configure(text="Exit Fullscreen" if self.is_fullscreen else "Fullscreen")

    def mini_mode_text(self) -> str:
        if self.timer_mode == "stopwatch":
            return "Stopwatch"
        phase = "Focus" if self.timer_mode == "pomodoro_focus" else "Break"
        return f"{self.active_pomodoro_preset} | {phase}"

    def weekly_completion_pct(self) -> float:
        total = sum(t.hours for t in self.tasks)
        done = sum(t.hours for t in self.tasks if t.completed)
        return (done / total * 100) if total else 0

    def today_completion_pct(self) -> float:
        today = datetime.now().strftime("%Y-%m-%d")
        day_total = sum(t.hours for t in self.tasks if t.day == today)
        day_done = sum(t.hours for t in self.tasks if t.day == today and t.completed)
        return (day_done / day_total * 100) if day_total else 0

    def refresh_mini_hover(self) -> None:
        mini = self.mini_hover_window
        if mini is None or not mini.winfo_exists():
            return

        widgets = self.mini_hover_widgets
        try:
            widgets["clock"].configure(text=datetime.now().strftime("%H:%M:%S"))
            widgets["profile"].configure(text=f"{self.current_profile.get()} | Week {self.current_week_key}")

            week_pct = self.weekly_completion_pct()
            today_pct = self.today_completion_pct()
            widgets["progress_text"].configure(text=f"Week {week_pct:.1f}%  •  Today {today_pct:.1f}%")
            widgets["progress"].set(week_pct / 100)

            timer_text = self.format_timer(self.timer_seconds)
            widgets["timer"].configure(text=f"{self.mini_mode_text()}  •  {timer_text}")

            pending = next((t for t in self.ordered_tasks() if not t.completed), None)
            if pending is None:
                widgets["next_task"].configure(text="Next: All tasks completed")
            else:
                widgets["next_task"].configure(text=f"Next: {pending.title[:42]}")
        except (TclError, KeyError):
            return

    def close_mini_hover(self, restore_main: bool = True) -> None:
        mini = self.mini_hover_window
        if mini is not None and mini.winfo_exists():
            mini.destroy()
        self.mini_hover_window = None
        self.mini_hover_widgets = {}
        if restore_main:
            self.deiconify()
            self.lift()

    def toggle_mini_topmost(self) -> None:
        mini = self.mini_hover_window
        if mini is None or not mini.winfo_exists():
            return
        pin_var = self.mini_hover_widgets.get("pin_var")
        if isinstance(pin_var, ctk.BooleanVar):
            mini.attributes("-topmost", bool(pin_var.get()))

    def mini_start_move(self, event) -> None:
        mini = self.mini_hover_window
        if mini is None or not mini.winfo_exists():
            return
        mini._drag_offset_x = event.x_root - mini.winfo_x()
        mini._drag_offset_y = event.y_root - mini.winfo_y()

    def mini_do_move(self, event) -> None:
        mini = self.mini_hover_window
        if mini is None or not mini.winfo_exists():
            return
        dx = getattr(mini, "_drag_offset_x", 0)
        dy = getattr(mini, "_drag_offset_y", 0)
        new_x = max(0, event.x_root - dx)
        new_y = max(0, event.y_root - dy)
        mini.geometry(f"+{new_x}+{new_y}")

    def mini_snap_edges(self, _event=None) -> None:
        mini = self.mini_hover_window
        if mini is None or not mini.winfo_exists():
            return

        mini.update_idletasks()
        x = mini.winfo_x()
        y = mini.winfo_y()
        w = mini.winfo_width()
        h = mini.winfo_height()
        sw = mini.winfo_screenwidth()
        sh = mini.winfo_screenheight()
        margin = 24
        bottom_offset = 48

        if abs(x - 0) <= margin:
            x = 0
        elif abs((x + w) - sw) <= margin:
            x = max(0, sw - w)

        if abs(y - 0) <= margin:
            y = 0
        elif abs((y + h) - (sh - bottom_offset)) <= margin:
            y = max(0, sh - h - bottom_offset)

        mini.geometry(f"+{x}+{y}")

    def restore_from_mini(self) -> None:
        self.close_mini_hover(restore_main=True)

    def open_mini_hover(self) -> None:
        if self.mini_hover_window is not None and self.mini_hover_window.winfo_exists():
            self.mini_hover_window.lift()
            self.mini_hover_window.focus_force()
            self.iconify()
            self.refresh_mini_hover()
            return

        mini = ctk.CTkToplevel(self)
        width, height = 360, 210
        x = max(0, mini.winfo_screenwidth() - width - 26)
        y = 32
        mini.geometry(f"{width}x{height}+{x}+{y}")
        mini.overrideredirect(True)
        mini.attributes("-topmost", True)
        mini.bind("<Escape>", lambda _e: self.restore_from_mini())
        self.mini_hover_window = mini

        frame = ctk.CTkFrame(mini, corner_radius=18)
        frame.pack(fill="both", expand=True, padx=6, pady=6)
        frame.grid_columnconfigure(0, weight=1)

        title_bar = ctk.CTkFrame(frame, corner_radius=12)
        title_bar.grid(row=0, column=0, padx=10, pady=(10, 6), sticky="ew")
        title_bar.grid_columnconfigure(0, weight=1)
        title_bar.bind("<ButtonPress-1>", self.mini_start_move)
        title_bar.bind("<B1-Motion>", self.mini_do_move)
        title_bar.bind("<ButtonRelease-1>", self.mini_snap_edges)
        title_bar.bind("<Double-Button-1>", lambda _e: self.restore_from_mini())

        title = ctk.CTkLabel(title_bar, text="Focus Hover", font=("Segoe UI", 14, "bold"))
        title.grid(row=0, column=0, padx=10, pady=8, sticky="w")
        title.bind("<ButtonPress-1>", self.mini_start_move)
        title.bind("<B1-Motion>", self.mini_do_move)
        title.bind("<ButtonRelease-1>", self.mini_snap_edges)

        pin_var = ctk.BooleanVar(value=True)
        pin_switch = ctk.CTkSwitch(
            title_bar,
            text="Pin",
            variable=pin_var,
            onvalue=True,
            offvalue=False,
            width=60,
            command=self.toggle_mini_topmost,
        )
        pin_switch.grid(row=0, column=1, padx=(6, 4), pady=8, sticky="e")

        close_btn = ctk.CTkButton(
            title_bar,
            text="×",
            width=28,
            height=28,
            command=self.restore_from_mini,
        )
        close_btn.grid(row=0, column=2, padx=(2, 8), pady=8, sticky="e")

        info = ctk.CTkLabel(frame, text="", anchor="w")
        info.grid(row=1, column=0, padx=12, pady=(0, 2), sticky="ew")

        clock = ctk.CTkLabel(frame, text="", font=("JetBrains Mono", 18, "bold"), anchor="w")
        clock.grid(row=2, column=0, padx=12, pady=2, sticky="ew")

        timer = ctk.CTkLabel(frame, text="", anchor="w", text_color=("#4b5563", "#9ca3af"))
        timer.grid(row=3, column=0, padx=12, pady=(2, 4), sticky="ew")

        progress = ctk.CTkProgressBar(frame, height=12)
        progress.grid(row=4, column=0, padx=12, pady=(2, 2), sticky="ew")
        progress.set(0)

        progress_text = ctk.CTkLabel(frame, text="", anchor="w")
        progress_text.grid(row=5, column=0, padx=12, pady=(2, 0), sticky="ew")

        next_task = ctk.CTkLabel(frame, text="", anchor="w", text_color=("#6b7280", "#9ca3af"))
        next_task.grid(row=6, column=0, padx=12, pady=(2, 0), sticky="ew")

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.grid(row=7, column=0, padx=10, pady=(8, 10), sticky="ew")
        btns.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(btns, text="Start", height=30, command=self.start_timer).grid(row=0, column=0, padx=3, pady=2, sticky="ew")
        ctk.CTkButton(btns, text="Pause", height=30, command=self.pause_timer).grid(row=0, column=1, padx=3, pady=2, sticky="ew")
        ctk.CTkButton(btns, text="Pomo", height=30, command=self.start_pomodoro).grid(row=0, column=2, padx=3, pady=2, sticky="ew")
        ctk.CTkButton(btns, text="Open", height=30, command=self.restore_from_mini).grid(row=0, column=3, padx=3, pady=2, sticky="ew")

        self.mini_hover_widgets = {
            "clock": clock,
            "profile": info,
            "timer": timer,
            "progress": progress,
            "progress_text": progress_text,
            "next_task": next_task,
            "pin_var": pin_var,
        }
        self.refresh_mini_hover()
        mini.protocol("WM_DELETE_WINDOW", self.restore_from_mini)
        mini.lift()

        self.iconify()


if __name__ == "__main__":
    app = ChecklistApp()
    app.mainloop()
