# =========================================================
# Student CRUD service with schedule delegation
# ScheduleService (lesson logic)
# InvoiceService (billing)
# =========================================================
from __future__ import annotations # Allow forward references in type hints

from typing import Optional # For optional return types

from constants import DEFAULT_STUDENTS # Default student data used for seeding when no data file exists
from models import Student # Domain model for student data
from repository import StudentRepository # Abstract repository interface for data access
from schedule_service import ScheduleService # Service responsible for lesson scheduling logic
from validators import InputValidator # Centralized input validation logic for all student fields and lesson details


class StudentService:
    # High-level application service used by CLI and GUI.

    def __init__(self, repo: StudentRepository):
        self.repo = repo
        self.schedule_service = ScheduleService(repo)
        self.invoice_service = None

    def attach_invoice_service(self, invoice_service) -> None:
        # Attach the invoice service after initialization.
        self.invoice_service = invoice_service

    def list_students(self) -> list[Student]:
        # Return all students.
        return self.repo.list_students()

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        # Return one student by ID.
        return self.repo.get_by_id(InputValidator.validate_student_id(student_id))

    def ensure_default_student(self) -> None:
        # Seed the system with default students when the file is empty.
        if self.repo.list_students():
            return
        # Iterate over the predefined DEFAULT_STUDENTS data, build validated Student objects, and add them to the repository.
        for name, birth_date_text, instrument, grade, lesson_minutes, lesson_start_time, fee_hkd, lesson_weekday, place in DEFAULT_STUDENTS:
            student = self._build_student(
                student_id=self.repo.next_id(),
                name=name,
                birth_date_str=birth_date_text,
                instrument=instrument,
                grade=grade,
                lesson_minutes=lesson_minutes,
                lesson_start_time=lesson_start_time,
                fee_hkd=fee_hkd,
                lesson_weekday=lesson_weekday,
                place=place,
                plan_type="regular",
                custom_lessons=[],
                lesson_overrides={},
            )
            self.repo.add(student)

    def _build_student(
        self,
        student_id: int,
        name: str,
        birth_date_str: str,
        instrument: str,
        grade: int | str,
        lesson_minutes: int,
        lesson_start_time: str,
        fee_hkd: int,
        lesson_weekday: str,
        place: str,
        plan_type: str,
        custom_lessons: Optional[list[dict]] = None,
        lesson_overrides: Optional[dict] = None,
    ) -> Student:
        # Create a validated student object.
        normalized_student_id = InputValidator.validate_student_id(student_id)
        birth_date = InputValidator.parse_date(birth_date_str, "Birth date")
        normalized_name = InputValidator.validate_name(name)
        normalized_instrument = InputValidator.validate_instrument(instrument)
        normalized_grade = InputValidator.validate_grade(str(grade))
        normalized_place = InputValidator.validate_place(place)
        normalized_fee_hkd = InputValidator.validate_fee_hkd(fee_hkd)
        normalized_plan_type = InputValidator.validate_plan_type(plan_type)
        normalized_lesson_minutes = InputValidator.validate_lesson_minutes(lesson_minutes)
        normalized_lesson_start_time = InputValidator.validate_time_hhmm(lesson_start_time)
        normalized_lesson_weekday = InputValidator.validate_weekday(lesson_weekday)
        # For flexible students, validate the custom lessons and ignore any lesson overrides since they don't apply. For regular students, validate the lesson overrides and ignore any custom lessons.
        normalized_custom_lessons = []
        normalized_lesson_overrides = lesson_overrides or {}
        if normalized_plan_type == "flexible":
            normalized_custom_lessons = [
                InputValidator.validate_flexible_lesson(lesson_item, normalized_lesson_minutes)
                for lesson_item in (custom_lessons or [])
            ]
            normalized_lesson_overrides = {}
        # For regular students, we validate the lesson overrides and ignore any custom lessons since they don't apply.
        return Student(
            student_id=normalized_student_id,
            name=normalized_name,
            birth_date=birth_date,
            instrument=normalized_instrument,
            grade=normalized_grade,
            lesson_minutes=normalized_lesson_minutes,
            lesson_start_time=normalized_lesson_start_time,
            fee_hkd=normalized_fee_hkd,
            lesson_weekday=normalized_lesson_weekday,
            place=normalized_place,
            plan_type=normalized_plan_type,
            lesson_overrides=normalized_lesson_overrides,
            custom_lessons=normalized_custom_lessons,
        )

    def add_student(
        self,
        name: str,
        birth_date_str: str,
        instrument: str,
        grade: int | str,
        lesson_minutes: int,
        lesson_start_time: str,
        fee_hkd: int,
        lesson_weekday: str,
        place: str,
        plan_type: str = "regular",
        custom_lessons: Optional[list[dict]] = None,
    ) -> Student:
        # Create and persist a new student.
        student = self._build_student(
            student_id=self.repo.next_id(),
            name=name,
            birth_date_str=birth_date_str,
            instrument=instrument,
            grade=grade,
            lesson_minutes=lesson_minutes,
            lesson_start_time=lesson_start_time,
            fee_hkd=fee_hkd,
            lesson_weekday=lesson_weekday,
            place=place,
            plan_type=plan_type,
            custom_lessons=custom_lessons,
            lesson_overrides={},
        )
        self.schedule_service.validate_student_schedule(student)
        self.repo.add(student)
        return student

    def add_flexible_student(
        self,
        name: str,
        birth_date_str: str,
        instrument: str,
        grade: int | str,
        fee_hkd: int,
        place: str,
        custom_lessons: list[dict],
        default_lesson_minutes: int = 45,
        default_start_time: str = "1300",
        default_weekday: str = "Mon",
    ) -> Student:
        # Convenience method for flexible student creation.
        return self.add_student(
            name=name,
            birth_date_str=birth_date_str,
            instrument=instrument,
            grade=grade,
            lesson_minutes=default_lesson_minutes,
            lesson_start_time=default_start_time,
            fee_hkd=fee_hkd,
            lesson_weekday=default_weekday,
            place=place,
            plan_type="flexible",
            custom_lessons=custom_lessons,
        )

    def update_student(self, student: Student) -> None:
        # Validate and update an existing student.
        student.student_id = InputValidator.validate_student_id(student.student_id)
        student.name = InputValidator.validate_name(student.name)
        student.instrument = InputValidator.validate_instrument(student.instrument)
        student.grade = InputValidator.validate_grade(student.grade)
        student.fee_hkd = InputValidator.validate_fee_hkd(student.fee_hkd)
        student.place = InputValidator.validate_place(student.place)
        student.plan_type = InputValidator.validate_plan_type(student.plan_type)
        student.lesson_minutes = InputValidator.validate_lesson_minutes(student.lesson_minutes)
        student.lesson_start_time = InputValidator.validate_time_hhmm(student.lesson_start_time)
        student.lesson_weekday = InputValidator.validate_weekday(student.lesson_weekday)
        student.custom_lessons = [
            InputValidator.validate_flexible_lesson(lesson_item, student.lesson_minutes)
            for lesson_item in student.custom_lessons
        ]

        if student.is_flexible:
            student.lesson_overrides = {}
        else:
            student.custom_lessons = []

        self.schedule_service.validate_student_schedule(student)
        self.repo.update(student)

    def delete_student_by_id(self, student_id: int) -> None:
        # Delete a student by ID.
        self.repo.delete_by_id(InputValidator.validate_student_id(student_id))

    def find_by_name(self, keyword: str) -> list[Student]:
        # Search for students by a partial case-insensitive name.
        normalized_keyword = InputValidator.validate_non_empty_text(keyword, "Name keyword").lower()
        return [student for student in self.repo.list_students() if normalized_keyword in student.name.lower()]

    def lesson_occurrences_for_student_in_month(self, student_id: int, year: int, month: int) -> list[dict]:
        # Return detailed lesson occurrences for one student and month.
        return self.schedule_service.get_student_occurrences(student_id, year, month)

    def schedule_for_month(self, year: int, month: int) -> list[str]:
        # Return the monthly schedule text lines.
        return self.schedule_service.schedule_for_month(year, month)

    def daily_schedule_for_date(self, target_date: str) -> list[str]:
        # Return the daily schedule text lines.
        return self.schedule_service.daily_schedule_for_date(target_date)

    def monthly_income_statement(self, year: int, month: int) -> dict:
        # Return the monthly income statement data.
        return self.schedule_service.monthly_income_statement(year, month)

    def change_single_lesson(self, student_id: int, original_lesson_date: str, new_lesson_date: str, new_start_time: str) -> None:
        # Change one regular lesson occurrence.
        self.schedule_service.change_single_lesson(student_id, original_lesson_date, new_lesson_date, new_start_time)

    def cancel_single_lesson(self, student_id: int, original_lesson_date: str) -> None:
        # Cancel one regular lesson occurrence.
        self.schedule_service.cancel_single_lesson(student_id, original_lesson_date)

    def clear_single_lesson_override(self, student_id: int, original_lesson_date: str) -> None:
        # Clear one regular lesson override.
        self.schedule_service.clear_single_lesson_override(student_id, original_lesson_date)

    def add_flexible_lesson(self, student_id: int, lesson_date: str, start_time: str, lesson_minutes: int) -> None:
        # Add one lesson to a flexible student.
        self.schedule_service.add_flexible_lesson(student_id, lesson_date, start_time, lesson_minutes)

    def remove_flexible_lesson(self, student_id: int, lesson_date: str, start_time: str) -> None:
        # Remove one lesson from a flexible student.
        self.schedule_service.remove_flexible_lesson(student_id, lesson_date, start_time)
