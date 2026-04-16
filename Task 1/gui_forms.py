# =========================================================
# Tkinter dialogs and forms used by the GUI
# Flexible lesson input dialog
# Lesson change dialog
# Student add/edit form
# =========================================================
from __future__ import annotations # Allow forward references in type hints (for Python 3.7+ compatibility)

import tkinter as tk # Standard Tkinter import for building the GUI.
from tkinter import messagebox, ttk # Standard Tkinter imports for building dialogs and forms in the GUI.

from constants import ALLOWED_GRADES, ALLOWED_LESSON_MINUTES, ALLOWED_PLACES, ALLOWED_WEEKDAYS # Allowed values for form dropdowns and validation
from validators import InputValidator # Centralized validation logic used by the forms to keep the UI code clean and focused on layout and user interaction.


class FlexibleLessonDialog(tk.Toplevel):
    # Dialog used to create or edit one flexible lesson.

    def __init__(self, parent, title: str = "Add Flexible Lesson", lesson: dict | None = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x250")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()
        # Center the dialog on the parent window.
        main_frame = ttk.Frame(self, padding=18)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Pre-fill the form if editing an existing lesson, otherwise use defaults.
        default_lesson = lesson or {"date": "", "start_time": "1300", "lesson_minutes": 45}
        self.date_entry = self._create_labeled_entry(main_frame, 0, "Date (YYYY-MM-DD):", default_lesson["date"])
        self.start_time_entry = self._create_labeled_entry(main_frame, 1, "Start time (HHMM):", default_lesson["start_time"])
        # Lesson minutes uses a dropdown since it's a fixed set of options.
        ttk.Label(main_frame, text="Lesson minutes:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.lesson_minutes_combo = ttk.Combobox(main_frame, values=[str(item) for item in ALLOWED_LESSON_MINUTES], state="readonly", width=27)
        self.lesson_minutes_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.lesson_minutes_combo.set(str(default_lesson["lesson_minutes"]))
        # Add a hint label for the expected input format.
        ttk.Label(main_frame, text="Example: 2026-02-18 / 1400 / 45").grid(row=3, column=0, columnspan=2, padx=10, pady=(6, 14), sticky="w")
        self._create_button_row(main_frame, 4, self.on_save, self.on_cancel)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def _create_labeled_entry(self, parent, row_index: int, label_text: str, default_value: str) -> ttk.Entry:
        # Create one label and entry pair.
        ttk.Label(parent, text=label_text).grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        entry_widget = ttk.Entry(parent, width=30)
        entry_widget.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
        entry_widget.insert(0, default_value)
        return entry_widget

    def _create_button_row(self, parent, row_index: int, save_command, cancel_command) -> None:
        # Create a save/cancel button row.
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row_index, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save", width=12, command=save_command).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="Cancel", width=12, command=cancel_command).pack(side=tk.LEFT, padx=8)

    def on_save(self) -> None:
        # Validate and close with result data.
        try:
            lesson_date = InputValidator.validate_date_text(self.date_entry.get().strip(), "Lesson date")
            start_time = InputValidator.validate_time_hhmm(self.start_time_entry.get().strip(), "Start time")
            lesson_minutes = InputValidator.validate_lesson_minutes(self.lesson_minutes_combo.get().strip())
            self.result = {"date": lesson_date, "start_time": start_time, "lesson_minutes": lesson_minutes}
            self.destroy()
        except Exception as error:
            messagebox.showerror("Input Error", str(error), parent=self)

    def on_cancel(self) -> None:
        # Close without saving.
        self.result = None
        self.destroy()


class ChangeLessonDialog(tk.Toplevel):
    # Dialog used to change one regular lesson.

    def __init__(self, parent, original_text: str, default_date: str, default_start_time: str):
        super().__init__(parent)
        self.title("Change Selected Lesson")
        self.geometry("470x240")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()
        
        main_frame = ttk.Frame(self, padding=18)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Display the original lesson details and pre-fill the form with the current date/time for easy editing.
        ttk.Label(main_frame, text="Original lesson:").grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        ttk.Label(main_frame, text=original_text, wraplength=280).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        # Add a hint label for the expected input format.
        ttk.Label(main_frame, text="New date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = ttk.Entry(main_frame, width=28)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.date_entry.insert(0, default_date)
        # Add a hint label for the expected input format.
        ttk.Label(main_frame, text="New start time (HHMM):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.start_time_entry = ttk.Entry(main_frame, width=28)
        self.start_time_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.start_time_entry.insert(0, default_start_time)
        # Add a hint label for the expected input format.
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(button_frame, text="Save", width=12, command=self.on_save).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="Cancel", width=12, command=self.on_cancel).pack(side=tk.LEFT, padx=8)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_save(self) -> None:
        # Validate and close with the new lesson date/time.
        try:
            new_date = InputValidator.validate_date_text(self.date_entry.get().strip(), "New lesson date")
            new_start_time = InputValidator.validate_time_hhmm(self.start_time_entry.get().strip(), "New start time")
            self.result = {"new_date": new_date, "new_start_time": new_start_time}
            self.destroy()
        except Exception as error:
            messagebox.showerror("Input Error", str(error), parent=self)

    def on_cancel(self) -> None:
        # Close without saving.
        self.result = None
        self.destroy()


class StudentForm(tk.Toplevel):
    # Add/edit student dialog shared by the GUI.

    def __init__(self, parent, title: str, student=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("700x860")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()
        # Pre-fill the form with the student data if provided, otherwise use defaults. Flexible lessons are only relevant when in flexible mode.
        self.custom_lessons = [dict(item) for item in getattr(student, "custom_lessons", [])] if getattr(student, "is_flexible", False) else []
        main_frame = ttk.Frame(self, padding=18)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Define default values for the form fields, using student data if available or sensible defaults otherwise.
        default_values = {
            "Name": getattr(student, "name", ""),
            "Birth": getattr(getattr(student, "birth_date", None), "isoformat", lambda: "2001-01-01")(),
            "Instrument": getattr(student, "instrument", "Trumpet"),
            "Grade": str(getattr(student, "grade", "8")),
            "Lesson minutes": str(getattr(student, "lesson_minutes", 45)),
            "Start time": getattr(student, "lesson_start_time", "1300"),
            "Fee (HKD)": str(getattr(student, "fee_hkd", 500)),
            "Lesson weekday": getattr(student, "lesson_weekday", "Mon"),
            "Place": getattr(student, "place", "Studio"),
        }
        # Build the form fields and keep references to the entry widgets for later validation and data retrieval.
        self.entry_widgets: dict[str, ttk.Entry | ttk.Combobox] = {}
        field_specs = [
            ("Name", "entry", default_values["Name"]),
            ("Birth", "entry", default_values["Birth"]),
            ("Instrument", "entry", default_values["Instrument"]),
            ("Grade", "grade", default_values["Grade"]),
            ("Lesson minutes", "minutes", default_values["Lesson minutes"]),
            ("Start time", "entry", default_values["Start time"]),
            ("Fee (HKD)", "entry", default_values["Fee (HKD)"]),
            ("Lesson weekday", "weekday", default_values["Lesson weekday"]),
            ("Place", "place", default_values["Place"]),
        ]
        # Create the form fields based on the specifications, using dropdowns for certain fields and entries for others.
        for row_index, (label_text, field_type, default_value) in enumerate(field_specs):
            ttk.Label(main_frame, text=label_text).grid(row=row_index, column=0, padx=10, pady=8, sticky="w")
            widget = self._build_field_widget(main_frame, row_index, field_type, default_value)
            self.entry_widgets[label_text] = widget
        # Add a checkbox to toggle between regular and flexible scheduling modes. The flexible lessons section is only shown when flexible mode is enabled.
        self.flexible_var = tk.BooleanVar(value=getattr(student, "is_flexible", False))
        self.flexible_check = ttk.Checkbutton(
            main_frame,
            text="Flexible mode ( non-regular)",
            variable=self.flexible_var,
            command=self.on_mode_changed,
        )
        self.flexible_check.grid(row=len(field_specs), column=0, columnspan=2, padx=10, pady=(10, 8), sticky="w")
        # Add a hint label to explain the difference between regular and flexible modes.
        self.mode_hint_var = tk.StringVar(value="")
        ttk.Label(main_frame, textvariable=self.mode_hint_var).grid(row=len(field_specs) + 1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="w")
        # The flexible lessons section is implemented as a listbox with add/edit/remove buttons. It is only enabled when flexible mode is selected.
        self.flex_frame = ttk.LabelFrame(main_frame, text="Flexible Lessons", padding=10)
        self.flex_frame.grid(row=len(field_specs) + 2, column=0, columnspan=2, padx=10, pady=8, sticky="ew")
        # The flexible lessons section is implemented as a listbox with add/edit/remove buttons. It is only enabled when flexible mode is selected.
        self.flex_listbox = tk.Listbox(self.flex_frame, height=6, width=72, exportselection=False, font=("Courier", 11))
        self.flex_listbox.pack(fill=tk.X, expand=False, pady=(0, 8))
        # Add buttons to manage the flexible lessons (add, edit, remove). These buttons open dialogs to input the lesson details.
        flex_button_frame = ttk.Frame(self.flex_frame)
        flex_button_frame.pack(fill=tk.X)
        for button_text, button_command in [
            ("Add Lesson", self.add_flexible_lesson),
            ("Edit Selected", self.edit_flexible_lesson),
            ("Remove Selected", self.remove_flexible_lesson),
        ]:
            ttk.Button(flex_button_frame, text=button_text, command=button_command).pack(side=tk.LEFT, padx=(0, 8))
        # Add the final save/cancel buttons for the entire student form.
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(field_specs) + 3, column=0, columnspan=2, pady=18)
        ttk.Button(button_frame, text="Save", width=12, command=self.on_save).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", width=12, command=self.on_cancel).pack(side=tk.LEFT, padx=10)

        self.refresh_flexible_list()
        self.on_mode_changed()
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def _build_field_widget(self, parent, row_index: int, field_type: str, default_value: str):
        # Build one form field widget.
        values_by_type = {
            "grade": ALLOWED_GRADES,
            "minutes": [str(item) for item in ALLOWED_LESSON_MINUTES],
            "weekday": ALLOWED_WEEKDAYS,
            "place": ALLOWED_PLACES,
        }
        if field_type in values_by_type:
            widget = ttk.Combobox(parent, values=values_by_type[field_type], state="readonly", width=34)
            widget.set(default_value)
        else:
            widget = ttk.Entry(parent, width=37)
            widget.insert(0, default_value)
        widget.grid(row=row_index, column=1, padx=10, pady=8, sticky="w")
        return widget

    def on_mode_changed(self) -> None:
        # Enable or disable regular/flexible widgets.
        is_flexible = self.flexible_var.get()
        regular_field_names = ["Lesson minutes", "Start time", "Lesson weekday"]
        if is_flexible:
            self.mode_hint_var.set("Flexible mode: weekly day/time fields are disabled. Please add custom lessons below.")
            for field_name in regular_field_names:
                self.entry_widgets[field_name].configure(state="disabled")
            self.flex_frame.grid()
            return

        self.mode_hint_var.set("Regular mode: fixed weekly lesson schedule.")
        for field_name in regular_field_names:
            widget_state = "readonly" if field_name in {"Lesson minutes", "Lesson weekday"} else "normal"
            self.entry_widgets[field_name].configure(state=widget_state)
        self.flex_frame.grid_remove()

    def refresh_flexible_list(self) -> None:
        """Refresh the flexible lesson listbox."""
        self.flex_listbox.delete(0, tk.END)
        if not self.custom_lessons:
            self.flex_listbox.insert(tk.END, "(No flexible lessons added)")
            return

        sorted_lessons = sorted(self.custom_lessons, key=lambda item: (item["date"], item["start_time"], int(item["lesson_minutes"])))
        self.custom_lessons = sorted_lessons
        for index, lesson_item in enumerate(sorted_lessons, start=1):
            lesson_date = lesson_item["date"]
            start_time = lesson_item["start_time"]
            lesson_minutes = int(lesson_item["lesson_minutes"])
            end_time = self._calc_end_time(start_time, lesson_minutes)
            weekday_name = ALLOWED_WEEKDAYS[InputValidator.parse_date(lesson_date, "Lesson date").weekday()]
            self.flex_listbox.insert(tk.END, f"Lesson {index}: {lesson_date} - {weekday_name} - {start_time}-{end_time} ({lesson_minutes}min)")

    def _calc_end_time(self, start_time: str, lesson_minutes: int) -> str:
        # Calculate end time from a HHMM start time.
        start_hour = int(start_time[:2])
        start_minute = int(start_time[2:])
        total_minutes = start_hour * 60 + start_minute + int(lesson_minutes)
        end_hour, end_minute = divmod(total_minutes, 60)
        return f"{end_hour % 24:02d}{end_minute:02d}"

    def add_flexible_lesson(self) -> None:
        # Add one flexible lesson entry to the form.
        dialog = FlexibleLessonDialog(self, "Add Flexible Lesson")
        self.wait_window(dialog)
        if not dialog.result:
            return
        if any(item["date"] == dialog.result["date"] and item["start_time"] == dialog.result["start_time"] for item in self.custom_lessons):
            messagebox.showerror("Error", "This flexible lesson already exists.", parent=self)
            return
        self.custom_lessons.append(dialog.result)
        self.refresh_flexible_list()

    def edit_flexible_lesson(self) -> None:
        # Edit the selected flexible lesson.
        selection = self.flex_listbox.curselection()
        if not selection or selection[0] >= len(self.custom_lessons):
            messagebox.showinfo("Info", "Please select one flexible lesson first.", parent=self)
            return

        selected_index = selection[0]
        dialog = FlexibleLessonDialog(self, "Edit Flexible Lesson", lesson=self.custom_lessons[selected_index])
        self.wait_window(dialog)
        if not dialog.result:
            return

        self.custom_lessons[selected_index] = dialog.result
        self.refresh_flexible_list()
        self.flex_listbox.selection_set(selected_index)

    def remove_flexible_lesson(self) -> None:
        # Remove the selected flexible lesson.
        selection = self.flex_listbox.curselection()
        if not selection or selection[0] >= len(self.custom_lessons):
            messagebox.showinfo("Info", "Please select one flexible lesson first.", parent=self)
            return

        if messagebox.askyesno("Confirm", "Remove selected flexible lesson?", parent=self):
            del self.custom_lessons[selection[0]]
            self.refresh_flexible_list()

    def on_save(self) -> None:
        # Validate the form and return a payload dictionary.
        try:
            name = InputValidator.validate_name(self.entry_widgets["Name"].get().strip())
            birth = InputValidator.validate_date_text(self.entry_widgets["Birth"].get().strip(), "Birth date")
            instrument = InputValidator.validate_instrument(self.entry_widgets["Instrument"].get().strip())
            grade = InputValidator.validate_grade(self.entry_widgets["Grade"].get().strip())
            fee_hkd = InputValidator.validate_fee_hkd(self.entry_widgets["Fee (HKD)"].get().strip())
            place = InputValidator.validate_place(self.entry_widgets["Place"].get().strip())
            is_flexible = self.flexible_var.get()

            if is_flexible:
                if not self.custom_lessons:
                    raise ValueError("Flexible mode requires at least one flexible lesson.")
                normalized_lessons = [InputValidator.validate_flexible_lesson(item) for item in self.custom_lessons]

                self.result = {
                    "plan_type": "flexible",
                    "name": name,
                    "birth": birth,
                    "instrument": instrument,
                    "grade": grade,
                    "lesson_minutes": 45,
                    "lesson_start_time": "1300",
                    "fee_hkd": fee_hkd,
                    "lesson_weekday": "Mon",
                    "place": place,
                    "custom_lessons": normalized_lessons,
                }
            else:
                lesson_minutes = InputValidator.validate_lesson_minutes(self.entry_widgets["Lesson minutes"].get().strip())
                lesson_start_time = InputValidator.validate_time_hhmm(self.entry_widgets["Start time"].get().strip(), "Start time")
                lesson_weekday = InputValidator.validate_weekday(self.entry_widgets["Lesson weekday"].get().strip())
                self.result = {
                    "plan_type": "regular",
                    "name": name,
                    "birth": birth,
                    "instrument": instrument,
                    "grade": grade,
                    "lesson_minutes": lesson_minutes,
                    "lesson_start_time": lesson_start_time,
                    "fee_hkd": fee_hkd,
                    "lesson_weekday": lesson_weekday,
                    "place": place,
                    "custom_lessons": [],
                }
            self.destroy()
        except Exception as error:
            messagebox.showerror("Input Error", str(error), parent=self)

    def on_cancel(self) -> None:
        # Close without saving.
        self.result = None
        self.destroy()
