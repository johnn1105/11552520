# =========================================================
# CLI Application for Music Lesson Management System
# Login system
# CRUD operations for students
# Support for regular and flexible lesson modes
# Monthly schedule display
# Invoice generation (PDF)
# =========================================================
from __future__ import annotations  # Allow forward references in type hints
from bootstrap import create_student_service  # Factory function to build full system
from constants import DEFAULT_ACCOUNT, DEFAULT_MONTH_TEXT, DEFAULT_PASSWORD # Shared constants
from validators import InputValidator  # Centralised validation logic

class CLIApp:
    # Simple CLI interface for managing music students
    def __init__(self, student_service):
        # Inject the student service 
        self.student_service = student_service

    def login(self) -> bool:
        # Handle CLI login.
        print("========= Login System =========")
        account_text = input(f"Account (default {DEFAULT_ACCOUNT}): ").strip() or DEFAULT_ACCOUNT
        password_text = input(f"Password (default {DEFAULT_PASSWORD}): ").strip() or DEFAULT_PASSWORD
        is_success = account_text == DEFAULT_ACCOUNT and password_text == DEFAULT_PASSWORD
        print("Login success.\n" if is_success else "Login failed.\n")
        return is_success

    def print_students(self) -> None:
        # Print all students to the terminal.
        students = self.student_service.list_students()
        if not students:
            print("(No students)")
            return

        print("=== My Students ===")
        for student in students:
            start_time = "-" if student.is_flexible else student.lesson_start_time
            lesson_minutes = "-" if student.is_flexible else f"{student.lesson_minutes}min"
            lesson_weekday = "-" if student.is_flexible else student.lesson_weekday
            print(
                f"ID={student.student_id} | Name={student.name} | Birth={student.birth_date} | "
                f"Instrument={student.instrument} | Grade={student.grade} | Mode={student.mode_label} | "
                f"Start={start_time} | Time={lesson_minutes} | Fee=HKD{student.fee_hkd} | "
                f"Lesson={lesson_weekday} | Place={student.place}"
            )

    def _collect_flexible_lessons(self) -> list[dict]:
        # Collect flexible lessons from the terminal.
        lesson_count = InputValidator.validate_positive_integer(
            input("How many flexible lessons to add now? ").strip(),
            "Lesson count",
        )
        return [
            InputValidator.validate_flexible_lesson(
                {
                    "date": input(f"Flexible lesson {index + 1} date (YYYY-MM-DD): ").strip(),
                    "start_time": input(f"Flexible lesson {index + 1} start time (HHMM): ").strip(),
                    "lesson_minutes": input(f"Flexible lesson {index + 1} minutes: ").strip(),
                }
            )
            for index in range(lesson_count)
        ]

    def add_student(self) -> None:
        # Add a regular or flexible student from terminal input.
        print("=== Add Student ===")
        print("1) Regular student")
        print("2) Flexible student")

        mode_choice = input("Choose mode: ").strip()
        if mode_choice not in {"1", "2"}:
            print("Invalid choice.")
            return
        # Common fields
        name = InputValidator.validate_name(input("Name: ").strip())
        birth_date_str = InputValidator.validate_date_text(input("Birth (YYYY-MM-DD): ").strip(), "Birth date")
        instrument = InputValidator.validate_instrument(input("Instrument: ").strip())
        grade = InputValidator.validate_grade(input("Grade (e.g. 8 / ATCL): ").strip())
        fee_hkd = InputValidator.validate_fee_hkd(input("Fee HKD per lesson (e.g. 500): ").strip())
        place = InputValidator.validate_place(input("Place (Studio/Home): ").strip())
        
        # Regular student fields
        if mode_choice == "1":
            lesson_minutes = InputValidator.validate_lesson_minutes(input("Lesson time minutes (30 / 45 / 60 / 90): ").strip())
            lesson_start_time = InputValidator.validate_time_hhmm(input("Lesson start time (HHMM, e.g. 1300): ").strip())
            lesson_weekday = InputValidator.validate_weekday(input("Lesson per week (Mon/Tue/...): ").strip())
            student = self.student_service.add_student(
                name=name,
                birth_date_str=birth_date_str,
                instrument=instrument,
                grade=grade,
                lesson_minutes=lesson_minutes,
                lesson_start_time=lesson_start_time,
                fee_hkd=fee_hkd,
                lesson_weekday=lesson_weekday,
                place=place,
                plan_type="regular",
            )
            print(f"Added regular student: {student.display_name()}")
            return
        
        # Flexible student fields
        custom_lessons = self._collect_flexible_lessons()
        student = self.student_service.add_flexible_student(
            name=name,
            birth_date_str=birth_date_str,
            instrument=instrument,
            grade=grade,
            fee_hkd=fee_hkd,
            place=place,
            custom_lessons=custom_lessons,
        )
        print(f"Added flexible student: {student.display_name()}")

    def edit_student(self) -> None:
        # Edit a student through CLI input.
        print("=== Edit Student ===")
        student_id = InputValidator.validate_student_id(input("Student ID: ").strip())
        student = self.student_service.get_student_by_id(student_id)
        if not student:
            print("Student not found.")
            return

        student.name = input(f"Name ({student.name}): ").strip() or student.name
        birth_text = input(f"Birth ({student.birth_date.isoformat()}): ").strip() or student.birth_date.isoformat()
        student.birth_date = InputValidator.parse_date(birth_text, "Birth date")
        student.instrument = InputValidator.validate_instrument(input(f"Instrument ({student.instrument}): ").strip() or student.instrument)
        student.grade = InputValidator.validate_grade(input(f"Grade ({student.grade}): ").strip() or student.grade)
        student.fee_hkd = InputValidator.validate_fee_hkd(input(f"Fee HKD ({student.fee_hkd}): ").strip() or student.fee_hkd)
        student.place = InputValidator.validate_place(input(f"Place ({student.place}): ").strip() or student.place)

        if student.is_flexible:
            print("Flexible student detected. Fixed weekly fields will stay as defaults.")
        else:
            student.lesson_minutes = InputValidator.validate_lesson_minutes(input(f"Lesson minutes ({student.lesson_minutes}): ").strip() or student.lesson_minutes)
            student.lesson_start_time = InputValidator.validate_time_hhmm(input(f"Lesson start time ({student.lesson_start_time}): ").strip() or student.lesson_start_time)
            student.lesson_weekday = InputValidator.validate_weekday(input(f"Lesson weekday ({student.lesson_weekday}): ").strip() or student.lesson_weekday)

        self.student_service.update_student(student)
        print("Updated.")

    def delete_student(self) -> None:
        # Delete a student by ID or name search.
        print("=== Delete Student ===")
        mode_choice = input("Delete by (1) ID or (2) Name? ").strip()
        if mode_choice == "1":
            student_id = InputValidator.validate_student_id(input("Student ID: ").strip())
            self.student_service.delete_student_by_id(student_id)
            print("Deleted (if existed).")
            return

        if mode_choice == "2":
            keyword = input("Name keyword: ").strip()
            matches = self.student_service.find_by_name(keyword)
            if not matches:
                print("No match.")
                return

            print("Matched students:")
            for student in matches:
                print(f"- {student.display_name()}")
            student_id = InputValidator.validate_student_id(input("Enter the ID to delete: ").strip())
            self.student_service.delete_student_by_id(student_id)
            print("Deleted (if existed).")
            return

        print("Invalid choice.")

    def show_schedule(self) -> None:
        # Print the monthly schedule.
        month_text = input(f"Enter month (YYYY-MM), default {DEFAULT_MONTH_TEXT}: ").strip() or DEFAULT_MONTH_TEXT
        year, month = InputValidator.parse_month_text(month_text)
        schedule_lines = self.student_service.schedule_for_month(year, month)
        print("(No schedule)" if not schedule_lines else "\n".join(schedule_lines))

    def generate_invoice(self) -> None:
        # Generate a PDF invoice for one student.
        month_text = input(f"Enter month (YYYY-MM), default {DEFAULT_MONTH_TEXT}: ").strip() or DEFAULT_MONTH_TEXT
        year, month = InputValidator.parse_month_text(month_text)
        student_id = InputValidator.validate_student_id(input("Student ID: ").strip())
        invoice = self.student_service.invoice_service.build_invoice(student_id, year, month)
        path = self.student_service.invoice_service.export_invoice_pdf(invoice)
        print(f"Invoice generated: {path}")

    def add_flexible_lesson(self) -> None:
        """Add one flexible lesson through CLI."""
        student_id = InputValidator.validate_student_id(input("Student ID: ").strip())
        lesson_date = input("Date (YYYY-MM-DD): ").strip()
        start_time = input("Start time (HHMM): ").strip()
        lesson_minutes = InputValidator.validate_lesson_minutes(input("Lesson minutes: ").strip())
        self.student_service.add_flexible_lesson(student_id, lesson_date, start_time, lesson_minutes)
        print("Flexible lesson added.")

    def remove_flexible_lesson(self) -> None:
        """Remove one flexible lesson through CLI."""
        student_id = InputValidator.validate_student_id(input("Student ID: ").strip())
        lesson_date = input("Date (YYYY-MM-DD): ").strip()
        start_time = input("Start time (HHMM): ").strip()
        self.student_service.remove_flexible_lesson(student_id, lesson_date, start_time)
        print("Flexible lesson removed.")

    def run_menu(self) -> None:
        # Show the interactive menu until the user exits.
        action_map = {
            "1": self.print_students,
            "2": self.add_student,
            "3": self.edit_student,
            "4": self.delete_student,
            "5": self.show_schedule,
            "6": self.generate_invoice,
            "7": self.add_flexible_lesson,
            "8": self.remove_flexible_lesson,
        }

        while True:
            print("\n=== Music Teacher Management ===")
            print("1) View my students")
            print("2) Add student (regular / flexible)")
            print("3) Edit student")
            print("4) Delete student")
            print("5) Show my schedule (one month)")
            print("6) Generate invoice (PDF)")
            print("7) Add flexible lesson")
            print("8) Remove flexible lesson")
            print("0) Exit")

            menu_choice = input("Choose: ").strip()
            if menu_choice == "0":
                print("Bye!!!")
                break

            action = action_map.get(menu_choice)
            if not action:
                print("Invalid choice.")
                continue

            try:
                action()
            except Exception as error:
                print(f"[Error] {error}")


def run_cli_app() -> None:
    # Application entry point for CLI mode.
    student_service = create_student_service()
    # Ensure default students exist 
    student_service.ensure_default_student()
    app = CLIApp(student_service)
    if not app.login():
        return
    #tO GUI
    launch_gui = input("Open GUI now? (y/n): ").strip().lower()
    if launch_gui == "y":
        from gui import run_gui_app
        run_gui_app(student_service)
    # Otherwise, stay in CLI mode
    app.run_menu()
