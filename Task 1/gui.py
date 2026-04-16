# =========================================================
# Tkinter application for the music lesson system.
# =========================================================
from __future__ import annotations # Allow forward references in type hints

import tkinter as tk # Standard GUI library
from tkinter import messagebox, ttk # For dialogs and themed widgets

from constants import DEFAULT_MONTH_TEXT # Default month text for the month entry field
from gui_forms import ChangeLessonDialog, StudentForm # Custom dialog forms for changing lessons and adding/editing students
from validators import InputValidator # Centralized input validation logic


class App(tk.Tk):
    # Main GUI application window.

    def __init__(self, student_service):
        super().__init__()
        self.service = student_service
        self.title("Music Teacher Management System")
        self.geometry("1600x900")
        self.minsize(1200, 820)
        self.current_occurrences: list[dict] = []
        self.columns = ["id", "name", "instrument", "grade", "mode", "weekday", "start", "minutes", "fee", "place"]
        self.sort_states = {column_name: False for column_name in self.columns}
        self.weekday_order = {name: index for index, name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])}
        self.grade_order = {grade: index for index, grade in enumerate(["1", "2", "3", "4", "5", "6", "7", "8", "ATCL", "LTCL", "FTCL"])}
        self._build_layout()
        self.refresh()
        self.show_schedule()
        self.after(200, self._show_open_message)  # show popup after GUI loads
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _show_open_message(self) -> None:
        # Show the welcome message after the window opens.
        messagebox.showinfo(
            "Welcome",
            "Music Teacher Management System opened successfully."
        )
    def _build_layout(self) -> None:
        # Build all GUI widgets.
        top_frame = ttk.Frame(self, padding=12)
        top_frame.pack(fill=tk.X)
        # Month selection
        ttk.Label(top_frame, text="Month (YYYY-MM):").pack(side=tk.LEFT)
        self.month_var = tk.StringVar(value=DEFAULT_MONTH_TEXT)
        month_entry = ttk.Entry(top_frame, textvariable=self.month_var, width=12)
        month_entry.pack(side=tk.LEFT, padx=(8, 12))
        month_entry.bind("<KeyRelease>", self.on_month_changed)
        # Action buttons
        ttk.Button(top_frame, text="Refresh", command=self.refresh_all).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="Edit Student", command=self.edit_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="Delete Student", command=self.delete_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="Generate Invoice", command=self.generate_invoice).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="Export Income Statement", command=self.export_monthly_income_statement).pack(side=tk.LEFT, padx=4)
        # Search bar
        middle_frame = ttk.Frame(self, padding=(12, 0, 12, 0))
        middle_frame.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(middle_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame = ttk.Frame(middle_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12, 0))
        # Build the student table on the left and the schedule panel on the right
        self._build_student_table(left_frame)
        self._build_schedule_panel(right_frame)
        self._build_selected_student_panel()

    def _build_student_table(self, parent) -> None:
        # Create the student table area.
        self.tree = ttk.Treeview(parent, columns=self.columns, show="headings", height=16)
        heading_names = {
            "id": "ID",
            "name": "Name",
            "instrument": "Instrument",
            "grade": "Grade",
            "mode": "Mode",
            "weekday": "Lesson Day",
            "start": "Start Time",
            "minutes": "Minutes",
            "fee": "Fee(HKD)",
            "place": "Place",
        }
        widths = {"id": 60, "name": 150, "instrument": 120, "grade": 90, "mode": 90, "weekday": 100, "start": 100, "minutes": 80, "fee": 100, "place": 100}
        # Configure columns and headings with sorting commands
        for column_name in self.columns:
            self.tree.heading(column_name, text=heading_names[column_name], command=lambda current_column=column_name: self.sort_treeview(current_column))
            self.tree.column(column_name, width=widths[column_name], anchor="center")
        # Add vertical scrollbar
        tree_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self.on_student_selected)

    def _build_schedule_panel(self, parent) -> None:
        # Create the monthly schedule and daily search panel.
        ttk.Label(parent, text="Monthly Schedule").pack(anchor="w", pady=(0, 6))
        self.schedule_box = tk.Text(parent, width=52, height=24)
        self.schedule_box.pack(fill=tk.BOTH, expand=True)
        # Daily search
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill=tk.X, pady=(12, 0))
        ttk.Label(date_frame, text="Date (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value="2026-02-01")
        ttk.Entry(date_frame, textvariable=self.date_var, width=14).pack(side=tk.LEFT, padx=8)
        ttk.Button(date_frame, text="Show Students On Date", command=self.show_students_on_date).pack(side=tk.LEFT)
    
    def _build_selected_student_panel(self) -> None:
        # Create the bottom panel for selected student lesson preview.
        bottom_frame = ttk.Frame(self, padding=12)
        bottom_frame.pack(fill=tk.BOTH, expand=False)
        # Selected student description
        self.selected_student_var = tk.StringVar(value="Select one student from the table above.")
        ttk.Label(bottom_frame, textvariable=self.selected_student_var).pack(anchor="w")
        # Lesson listbox for the selected student and month
        self.lesson_listbox = tk.Listbox(bottom_frame, height=8, exportselection=False, font=("Courier", 11))
        self.lesson_listbox.pack(fill=tk.X, expand=False, pady=(8, 6))
        self.lesson_listbox.bind("<<ListboxSelect>>", self.on_lesson_selected)
        # Selected lesson description and action buttons
        self.selected_lesson_var = tk.StringVar(value="Select one lesson below, then click Change / Cancel.")
        ttk.Label(bottom_frame, textvariable=self.selected_lesson_var).pack(anchor="w")
        # Action buttons for changing/cancelling/clearing the selected lesson
        action_frame = ttk.Frame(bottom_frame)
        action_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(action_frame, text="Change Selected Lesson", command=self.change_selected_lesson).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(action_frame, text="Cancel Selected Lesson", command=self.cancel_selected_lesson).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(action_frame, text="Clear Selected Override", command=self.clear_selected_lesson_override).pack(side=tk.LEFT)

    def on_close(self) -> None:
        # Close the GUI and return to CLI.
        if messagebox.askokcancel("Exit", "Return to CLI menu?"):
            self.destroy()

    def refresh_all(self) -> None:
        # Refresh both student and schedule areas.
        self.refresh()
        self.show_schedule()

    def _parse_month_input(self) -> tuple[int, int]:
        # Parse the month entry from the GUI.
        return InputValidator.parse_month_text(self.month_var.get().strip())

    def _selected_student_id(self):
        # Return the selected student ID from the table.
        selection = self.tree.selection()
        if not selection:
            return None
        return int(self.tree.item(selection[0], "values")[0])

    def _sort_key(self, column_name: str, value):
        # Return a sort key for treeview values.
        if column_name in {"id", "minutes", "fee", "start"}:
            try:
                return int(value)
            except ValueError:
                return 0
        if column_name == "weekday":
            return self.weekday_order.get(value, 999)
        if column_name == "grade":
            return self.grade_order.get(str(value), 999)
        return str(value).lower()

    def sort_treeview(self, column_name: str) -> None:
        # Sort the student table by the selected column.
        items = [(self.tree.set(item_id, column_name), item_id) for item_id in self.tree.get_children("")]
        reverse_order = self.sort_states[column_name]
        items.sort(key=lambda item: self._sort_key(column_name, item[0]), reverse=reverse_order)
        for index, (_, item_id) in enumerate(items):
            self.tree.move(item_id, "", index)
        self.sort_states[column_name] = not reverse_order

    def refresh(self) -> None:
        # Reload the student table.
        selected_student_id = self._selected_student_id()
        for item_id in self.tree.get_children():
            self.tree.delete(item_id)
        # Rebuild the treeview with updated student data.
        selected_item_id = None
        for student in self.service.list_students():
            item_id = self.tree.insert(
                "",
                tk.END,
                values=(
                    student.student_id,
                    student.name,
                    student.instrument,
                    student.grade,
                    student.mode_label,
                    "-" if student.is_flexible else student.lesson_weekday,
                    "-" if student.is_flexible else student.lesson_start_time,
                    "-" if student.is_flexible else student.lesson_minutes,
                    student.fee_hkd,
                    student.place,
                ),
            )
            if selected_student_id == student.student_id:
                selected_item_id = item_id
        # Restore selection if possible after refresh
        if selected_item_id:
            self.tree.selection_set(selected_item_id)
            self.tree.focus(selected_item_id)
            self.update_selected_student_preview()
        else:
            self.clear_selected_student_preview()

    def clear_selected_student_preview(self) -> None:
        # Reset the selected student preview area.
        self.current_occurrences = []
        self.selected_student_var.set("Select one student from the table above.")
        self.lesson_listbox.delete(0, tk.END)
        self.lesson_listbox.insert(tk.END, "(No student selected)")
        self.selected_lesson_var.set("Select one lesson below, then click Change / Cancel.")

    def update_selected_student_preview(self) -> None:
        # Update the selected student lesson preview.
        student_id = self._selected_student_id()
        self.lesson_listbox.delete(0, tk.END)
        self.current_occurrences = []
        if student_id is None:
            self.clear_selected_student_preview()
            return
        # Get the student and their lesson occurrences for the selected month, then update the preview area.
        student = self.service.get_student_by_id(student_id)
        if not student:
            self.selected_student_var.set("Student not found.")
            self.lesson_listbox.insert(tk.END, "(Student not found)")
            return
        # Get the student's lesson occurrences for the selected month.
        try:
            year, month = self._parse_month_input()
            self.current_occurrences = self.service.lesson_occurrences_for_student_in_month(student_id, year, month)
            month_text = f"{year:04d}-{month:02d}"
            self.selected_student_var.set(f"{student.name} | {student.instrument} | {student.mode_label} | {month_text} | {len(self.current_occurrences)} lesson(s)")
            if not self.current_occurrences:
                self.lesson_listbox.insert(tk.END, "(No lesson in this month)")
            else:
                for index, occurrence in enumerate(self.current_occurrences, start=1):
                    self.lesson_listbox.insert(tk.END, f"Lesson {index}: {occurrence['display_text']}")
            self.selected_lesson_var.set(
                "Flexible student selected. Change / Cancel / Clear are only for regular mode."
                if student.is_flexible
                else "Select one lesson below, then click Change / Cancel."
            )
        except Exception as error:
            self.selected_student_var.set(f"{student.name} | invalid month input")
            self.lesson_listbox.insert(tk.END, f"[Error] {error}")
            self.selected_lesson_var.set("Select one lesson below, then click Change / Cancel.")

    def on_student_selected(self, event=None) -> None:
        # Handle student selection.
        self.update_selected_student_preview()

    def on_month_changed(self, event=None) -> None:
        # Refresh preview when the month input changes.
        try:
            self._parse_month_input()
        except Exception:
            return
        if self._selected_student_id() is not None:
            self.update_selected_student_preview()

    def _get_selected_lesson_info(self) -> dict | None:
        # Return the selected occurrence dictionary.
        selection = self.lesson_listbox.curselection()
        if not selection:
            return None
        selected_index = selection[0]
        if selected_index >= len(self.current_occurrences):
            return None
        return self.current_occurrences[selected_index]

    def on_lesson_selected(self, event=None) -> None:
        # Update the selected lesson description text.
        lesson_info = self._get_selected_lesson_info()
        if not lesson_info:
            self.selected_lesson_var.set("Select one lesson below, then click Change / Cancel.")
            return
        self.selected_lesson_var.set(f"Selected original lesson date: {lesson_info['original_date']}")

    def change_selected_lesson(self) -> None:
        # Change one selected regular lesson.
        student_id = self._selected_student_id()
        occurrence = self._get_selected_lesson_info()
        if student_id is None or not occurrence:
            messagebox.showinfo("Info", "Please select one lesson first.")
            return
        # Verify that the student is regular mode before allowing changes.
        student = self.service.get_student_by_id(student_id)
        if not student or student.is_flexible:
            messagebox.showinfo("Info", "This action is only available for regular students.")
            return
        # Open the change lesson dialog with the current lesson info pre-filled, and update the lesson if the user confirms.
        dialog = ChangeLessonDialog(self, occurrence["display_text"], occurrence["date"], occurrence["start_time"])
        self.wait_window(dialog)
        if not dialog.result:
            return

        try:
            self.service.change_single_lesson(student_id, occurrence["original_date"], dialog.result["new_date"], dialog.result["new_start_time"])
            self.refresh_all()
            self.update_selected_student_preview()
            messagebox.showinfo("Done", "Selected lesson updated successfully.")
        except Exception as error:
            messagebox.showerror("Warning", str(error))

    def cancel_selected_lesson(self) -> None:
        # Cancel one selected regular lesson.
        student_id = self._selected_student_id()
        occurrence = self._get_selected_lesson_info()
        if student_id is None or not occurrence:
            messagebox.showinfo("Info", "Please select one lesson first.")
            return
        # Verify that the student is regular mode before allowing cancellation.
        student = self.service.get_student_by_id(student_id)
        if not student or student.is_flexible:
            messagebox.showinfo("Info", "This action is only available for regular students.")
            return
        # Confirm the cancellation action with the user before proceeding.
        if not messagebox.askyesno("Confirm", f"Cancel lesson on {occurrence['original_date']}?"):
            return
        # Call the service to cancel the lesson, then refresh the preview and schedule.
        try:
            self.service.cancel_single_lesson(student_id, occurrence["original_date"])
            self.refresh_all()
            self.update_selected_student_preview()
            messagebox.showinfo("Done", "Selected lesson cancelled successfully.")
        except Exception as error:
            messagebox.showerror("Warning", str(error))

    def clear_selected_lesson_override(self) -> None:
        # Clear one regular lesson override.
        student_id = self._selected_student_id()
        occurrence = self._get_selected_lesson_info()
        if student_id is None or not occurrence:
            messagebox.showinfo("Info", "Please select one lesson first.")
            return
        # Verify that the student is regular mode before allowing override clearing.
        student = self.service.get_student_by_id(student_id)
        if not student or student.is_flexible:
            messagebox.showinfo("Info", "This action is only available for regular students.")
            return
        #
        try:
            self.service.clear_single_lesson_override(student_id, occurrence["original_date"])
            self.refresh_all()
            self.update_selected_student_preview()
            messagebox.showinfo("Done", "Selected override cleared successfully.")
        except Exception as error:
            messagebox.showerror("Warning", str(error))

    def add_student(self) -> None:
        # Open the add student form.
        form = StudentForm(self, "Add Student")
        self.wait_window(form)
        if not form.result:
            return

        try:
            data = form.result
            if data["plan_type"] == "regular":
                self.service.add_student(
                    name=data["name"],
                    birth_date_str=data["birth"],
                    instrument=data["instrument"],
                    grade=data["grade"],
                    lesson_minutes=data["lesson_minutes"],
                    lesson_start_time=data["lesson_start_time"],
                    fee_hkd=data["fee_hkd"],
                    lesson_weekday=data["lesson_weekday"],
                    place=data["place"],
                    plan_type="regular",
                )
            else:
                self.service.add_flexible_student(
                    name=data["name"],
                    birth_date_str=data["birth"],
                    instrument=data["instrument"],
                    grade=data["grade"],
                    fee_hkd=data["fee_hkd"],
                    place=data["place"],
                    custom_lessons=data["custom_lessons"],
                    default_lesson_minutes=data["lesson_minutes"],
                    default_start_time=data["lesson_start_time"],
                    default_weekday=data["lesson_weekday"],
                )
            self.refresh_all()
            messagebox.showinfo("Done", "Student added successfully.")
        except Exception as error:
            messagebox.showerror("Warning", str(error))

    def edit_student(self) -> None:
        # Open the edit student form.
        student_id = self._selected_student_id()
        if student_id is None:
            messagebox.showinfo("Info", "Please select a student first.")
            return
        # Get the student data and pre-fill the form, then update the student if the user confirms.
        student = self.service.get_student_by_id(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return
        # Get the student's lesson occurrences for the selected month.
        form = StudentForm(self, "Edit Student", student=student)
        self.wait_window(form)
        if not form.result:
            return

        try:
            data = form.result
            student.name = data["name"]
            student.birth_date = InputValidator.parse_date(data["birth"], "Birth date")
            student.instrument = data["instrument"]
            student.grade = data["grade"]
            student.fee_hkd = InputValidator.validate_fee_hkd(data["fee_hkd"])
            student.place = data["place"]
            student.plan_type = data["plan_type"]
            student.lesson_minutes = InputValidator.validate_lesson_minutes(data["lesson_minutes"])
            student.lesson_start_time = data["lesson_start_time"]
            student.lesson_weekday = data["lesson_weekday"]
            student.custom_lessons = list(data["custom_lessons"])
            if student.plan_type == "regular":
                student.custom_lessons = []
            else:
                student.lesson_overrides = {}
            self.service.update_student(student)
            self.refresh_all()
            messagebox.showinfo("Done", "Student updated successfully.")
        except Exception as error:
            messagebox.showerror("Warning", str(error))

    def delete_student(self) -> None:
        # Delete the selected student.
        student_id = self._selected_student_id()
        if student_id is None:
            messagebox.showinfo("Info", "Please select a student first.")
            return
        if messagebox.askyesno("Confirm", f"Delete student ID={student_id}?"):
            self.service.delete_student_by_id(student_id)
            self.refresh_all()
            messagebox.showinfo("Done", "Student deleted successfully.")

    def show_schedule(self) -> None:
        # Show the monthly schedule in the right-side text area.
        self.schedule_box.delete("1.0", tk.END)
        try:
            year, month = self._parse_month_input()
            schedule_items = self.service.schedule_for_month(year, month)
            self.schedule_box.insert(tk.END, "(No schedule)\n" if not schedule_items else "\n".join(schedule_items) + "\n")
        except Exception as error:
            self.schedule_box.insert(tk.END, f"[Error] {error}\n")

    def show_students_on_date(self) -> None:
        # Show all students scheduled on the requested date.
        self.schedule_box.delete("1.0", tk.END)
        try:
            target_date = self.date_var.get().strip()
            InputValidator.validate_date_text(target_date, "Target date")
            items = self.service.daily_schedule_for_date(target_date)
            self.schedule_box.insert(tk.END, f"Students on {target_date}\n")
            self.schedule_box.insert(tk.END, "=" * 40 + "\n")
            self.schedule_box.insert(tk.END, "(No lesson)\n" if not items else "\n".join(items) + "\n")
        except Exception as error:
            self.schedule_box.insert(tk.END, f"[Error] {error}\n")

    def generate_invoice(self) -> None:
        # Generate an invoice for the selected student and month.
        student_id = self._selected_student_id()
        if student_id is None:
            messagebox.showinfo("Info", "Please select a student first.")
            return
        try:
            year, month = self._parse_month_input()
            invoice = self.service.invoice_service.build_invoice(student_id, year, month)
            path = self.service.invoice_service.export_invoice_pdf(invoice)
            messagebox.showinfo("Done", f"Invoice generated:\n{path}")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def export_monthly_income_statement(self) -> None:
        # Generate the monthly income statement PDF.
        try:
            year, month = self._parse_month_input()
            statement = self.service.monthly_income_statement(year, month)
            path = self.service.invoice_service.export_monthly_income_pdf(statement)
            messagebox.showinfo("Done", f"Monthly income statement generated:\n{path}")
        except Exception as error:
            messagebox.showerror("Error", str(error))


def run_gui_app(student_service) -> None:
    # Open the GUI and block until it closes.
    app = App(student_service)
    app.mainloop()
