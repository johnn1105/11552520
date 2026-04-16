# =========================================================
# Scheduling, occurrence generation, and conflict handling
# Lesson occurrence generation
# Conflict detection (time overlap)
# Lesson rescheduling and cancellation
# Monthly and daily schedule generation
# =========================================================
from __future__ import annotations

from datetime import date, timedelta # For date handling and calculating lesson occurrences
from typing import Optional # For optional parameters in method signatures

from constants import WEEKDAY_MAP, WEEKDAY_NAME_BY_INDEX # Mapping of weekday names to indices and vice versa
from lesson_plans import FlexibleLessonPlan, LessonPlan, RegularLessonPlan  # Lesson plan strategies for regular and flexible students
from models import LessonOccurrence, Student # Data models for students and lesson occurrences
from repository import StudentRepository # Abstract repository interface for student data access
from validators import InputValidator # Centralized input validation logic


class ScheduleService:
    """Service responsible for lesson schedules and lesson overrides."""

    def __init__(self, repo: StudentRepository):
        # Initialize the service with a student repository for data access.
        self.repo = repo

    def parse_date(self, date_text: str) -> date:
        # Parse a date string into a date object.
        return InputValidator.parse_date(date_text, "Date")

    def time_to_minutes(self, time_text: str) -> int:
        # Convert HHMM to minutes since midnight.
        return int(time_text[:2]) * 60 + int(time_text[2:])

    def calc_end_time(self, start_time: str, lesson_minutes: int) -> str:
        # Calculate the end time from start time and duration.
        end_total_minutes = self.time_to_minutes(start_time) + int(lesson_minutes)
        end_hour, end_minute = divmod(end_total_minutes, 60)
        return f"{end_hour % 24:02d}{end_minute:02d}"
    
    def build_occurrence(
        self,
        student: Student,
        original_date: str,
        actual_date: str,
        start_time: str,
        lesson_minutes: int,
        cancelled: bool,
        is_override: bool,
    ) -> LessonOccurrence:
        # Create a lesson occurrence object.
        actual_date_object = self.parse_date(actual_date)
        end_time = self.calc_end_time(start_time, lesson_minutes)
        weekday_name = WEEKDAY_NAME_BY_INDEX[actual_date_object.weekday()]
        return LessonOccurrence(
            original_date=original_date,
            date=actual_date,
            weekday=weekday_name,
            start_time=start_time,
            end_time=end_time,
            lesson_minutes=int(lesson_minutes),
            cancelled=bool(cancelled),
            is_override=bool(is_override),
        )

    def get_plan(self, student: Student) -> LessonPlan:
        # Return the appropriate lesson plan strategy for a student.
        return FlexibleLessonPlan() if student.is_flexible else RegularLessonPlan()

    def lesson_dates_in_month(self, year: int, month: int, weekday: str) -> list[str]:
        # Return all regular lesson dates in the target month.
        weekday_index = WEEKDAY_MAP[weekday]
        first_day = date(year, month, 1)
        offset_days = (weekday_index - first_day.weekday()) % 7
        first_lesson_date = first_day + timedelta(days=offset_days)

        lesson_dates: list[str] = []
        current_date = first_lesson_date
        while current_date.month == month:
            lesson_dates.append(current_date.isoformat())
            current_date += timedelta(days=7)
        return lesson_dates

    def get_student_occurrences(self, student_id: int, year: int, month: int) -> list[dict]:
        # Return occurrence dictionaries for the target student and month.
        student = self.repo.get_by_id(InputValidator.validate_student_id(student_id))
        if not student:
            raise ValueError("Student not found.")
        return [occurrence.to_dict() for occurrence in self.get_plan(student).get_occurrences(self, student, year, month)]

    def _check_regular_conflict(
        self,
        lesson_weekday: str,
        lesson_start_time: str,
        lesson_minutes: int,
        ignore_student_id: Optional[int] = None,
    ) -> Optional[str]:
        # Check weekly regular timetable overlap.
        new_start_minutes = self.time_to_minutes(lesson_start_time)
        new_end_minutes = new_start_minutes + int(lesson_minutes)
        # Iterate through all students to find any time overlap on the same weekday, ignoring the specified student ID.
        for student in self.repo.list_students():
            if ignore_student_id is not None and student.student_id == ignore_student_id:
                continue
            if student.is_flexible or student.lesson_weekday != lesson_weekday:
                continue
            # Calculate the time range for the existing lesson and check for overlap with the new lesson time.        
            old_start_minutes = self.time_to_minutes(student.lesson_start_time)
            old_end_minutes = old_start_minutes + int(student.lesson_minutes)
            if new_start_minutes < old_end_minutes and old_start_minutes < new_end_minutes:
                end_time = self.calc_end_time(student.lesson_start_time, student.lesson_minutes)
                return (
                    "Time overlap detected.\n\n"
                    f"Existing student: {student.name}\n"
                    f"Day: {student.lesson_weekday}\n"
                    f"Time: {student.lesson_start_time}-{end_time} ({student.lesson_minutes}min)"
                )
        return None

    def check_single_lesson_conflict(
        self,
        target_date: str,
        target_start_time: str,
        lesson_minutes: int,
        ignore_student_id: Optional[int] = None,
        ignore_original_date: Optional[str] = None,
    ) -> None:
        # Check overlap for one concrete lesson occurrence.
        InputValidator.validate_date_text(target_date, "Lesson date")
        InputValidator.validate_time_hhmm(target_start_time, "Start time")
        # Validate that the target lesson does not overlap with any existing active lesson on the same date
        target_date_object = self.parse_date(target_date)
        new_start_minutes = self.time_to_minutes(target_start_time)
        new_end_minutes = new_start_minutes + int(lesson_minutes)
        # Iterate through all students and their occurrences on the target date to find any time overlap
        for student in self.repo.list_students():
            occurrences = self.get_student_occurrences(student.student_id, target_date_object.year, target_date_object.month)
            for occurrence in occurrences:
                if occurrence["cancelled"] or occurrence["date"] != target_date:
                    continue
                if ignore_student_id is not None and student.student_id == ignore_student_id:
                    if ignore_original_date is not None and occurrence["original_date"] == ignore_original_date:
                        continue
                # Calculate the time range for the existing occurrence and check for overlap with the new lesson time.            
                old_start_minutes = self.time_to_minutes(occurrence["start_time"])
                old_end_minutes = old_start_minutes + int(occurrence["lesson_minutes"])
                if new_start_minutes < old_end_minutes and old_start_minutes < new_end_minutes:
                    raise ValueError(
                        "Time overlap detected.\n\n"
                        f"Existing student: {student.name}\n"
                        f"Date: {occurrence['date']}\n"
                        f"Time: {occurrence['start_time']}-{occurrence['end_time']} ({occurrence['lesson_minutes']}min)"
                    )
    
    def validate_student_schedule(self, student: Student) -> None:
        # Validate a student's schedule before saving.
        if student.is_flexible:
            seen_pairs: set[tuple[str, str]] = set()
            for lesson_item in student.custom_lessons:
                lesson_date = str(lesson_item.get("date", "")).strip()
                start_time = str(lesson_item.get("start_time", "")).strip()
                lesson_minutes = int(lesson_item.get("lesson_minutes", student.lesson_minutes))
                if not lesson_date or not start_time:
                    raise ValueError("Each flexible lesson must include date and start_time.")
                # Check for duplicate date + time pairs within the same student's custom lessons
                key = (lesson_date, start_time)
                if key in seen_pairs:
                    raise ValueError(f"Duplicate flexible lesson found: {lesson_date} {start_time}")
                seen_pairs.add(key)
                # Check for conflicts with existing lessons
                self.check_single_lesson_conflict(
                    target_date=lesson_date,
                    target_start_time=start_time,
                    lesson_minutes=lesson_minutes,
                    ignore_student_id=student.student_id,
                    ignore_original_date=lesson_date,
                )
            return
        # For regular students, check for conflicts based on the regular weekly schedule.
        conflict_message = self._check_regular_conflict(
            lesson_weekday=student.lesson_weekday,
            lesson_start_time=student.lesson_start_time,
            lesson_minutes=student.lesson_minutes,
            ignore_student_id=student.student_id,
        )
        if conflict_message:
            raise ValueError(conflict_message)

    def change_single_lesson(self, student_id: int, original_lesson_date: str, new_lesson_date: str, new_start_time: str) -> None:
        # Move one regular lesson to another date or time.
        student = self.repo.get_by_id(InputValidator.validate_student_id(student_id))
        if not student:
            raise ValueError("Student not found.")
        if student.is_flexible:
            raise ValueError("Single lesson change is only available for regular mode student.")
        # Validate inputs and check for conflicts with the new lesson date and time, ignoring the original lesson occurrence for this student.
        InputValidator.validate_date_text(original_lesson_date, "Original lesson date")
        InputValidator.validate_date_text(new_lesson_date, "New lesson date")
        InputValidator.validate_time_hhmm(new_start_time, "New start time")
        self.check_single_lesson_conflict(new_lesson_date, new_start_time, student.lesson_minutes, student.student_id, original_lesson_date)
        # If no conflicts, save the override for the original lesson date with the new date and time.
        student.lesson_overrides[original_lesson_date] = {
            "date": new_lesson_date,
            "start_time": new_start_time,
            "lesson_minutes": student.lesson_minutes,
            "cancelled": False,
        }
        self.repo.update(student)

    def cancel_single_lesson(self, student_id: int, original_lesson_date: str) -> None:
        # Cancel one regular lesson.
        student = self.repo.get_by_id(InputValidator.validate_student_id(student_id))
        if not student:
            raise ValueError("Student not found.")
        if student.is_flexible:
            raise ValueError("Single lesson cancel is only available for regular mode student.")
        # Validate the original lesson date and save the override with cancelled=True for that date.
        InputValidator.validate_date_text(original_lesson_date, "Original lesson date")
        student.lesson_overrides[original_lesson_date] = {
            "date": original_lesson_date,
            "start_time": student.lesson_start_time,
            "lesson_minutes": student.lesson_minutes,
            "cancelled": True,
        }
        self.repo.update(student)

    def clear_single_lesson_override(self, student_id: int, original_lesson_date: str) -> None:
        # Remove a change or cancellation from one regular lesson.
        student = self.repo.get_by_id(InputValidator.validate_student_id(student_id))
        if not student:
            raise ValueError("Student not found.")
        if student.is_flexible:
            raise ValueError("Clear lesson override is only available for regular mode student.")
        # Validate the original lesson date and remove any override for that date to restore the original schedule.
        InputValidator.validate_date_text(original_lesson_date, "Original lesson date")
        student.lesson_overrides.pop(original_lesson_date, None)
        self.repo.update(student)

    def add_flexible_lesson(self, student_id: int, lesson_date: str, start_time: str, lesson_minutes: int) -> None:
        # Add a new flexible lesson to a flexible student.
        student = self.repo.get_by_id(InputValidator.validate_student_id(student_id))
        if not student:
            raise ValueError("Student not found.")
        if not student.is_flexible:
            raise ValueError("This student is not in flexible mode.")
        # Validate the new lesson details and check for conflicts with the new lesson date and time.
        normalized_lesson = InputValidator.validate_flexible_lesson(
            {"date": lesson_date, "start_time": start_time, "lesson_minutes": lesson_minutes},
            student.lesson_minutes,
        )
        # Check for conflicts with the new lesson date and time, ignoring any existing lesson occurrence for this student on the same original date 
        self.check_single_lesson_conflict(
            normalized_lesson["date"],
            normalized_lesson["start_time"],
            normalized_lesson["lesson_minutes"],
            student.student_id,
            normalized_lesson["date"],
        )

        if any(item["date"] == normalized_lesson["date"] and item["start_time"] == normalized_lesson["start_time"] for item in student.custom_lessons):
            raise ValueError("This flexible lesson already exists.")
        # If no conflicts, add the new lesson to the student's custom lessons.
        student.custom_lessons = [*student.custom_lessons, normalized_lesson]
        self.repo.update(student)

    def remove_flexible_lesson(self, student_id: int, lesson_date: str, start_time: str) -> None:
        # Remove one flexible lesson from a flexible student.
        student = self.repo.get_by_id(InputValidator.validate_student_id(student_id))
        if not student:
            raise ValueError("Student not found.")
        if not student.is_flexible:
            raise ValueError("This student is not in flexible mode.")
        # Validate the lesson details and remove the matching lesson from the student's custom lessons.
        normalized_date = InputValidator.validate_date_text(lesson_date, "Lesson date")
        normalized_start_time = InputValidator.validate_time_hhmm(start_time, "Start time")
        original_count = len(student.custom_lessons)
        student.custom_lessons = [
            lesson_item
            for lesson_item in student.custom_lessons
            if not (lesson_item["date"] == normalized_date and lesson_item["start_time"] == normalized_start_time)
        ]
        # If the count of custom lessons did not decrease, it means the specified lesson was not found for removal.
        if len(student.custom_lessons) == original_count:
            raise ValueError("Flexible lesson not found.")
        self.repo.update(student)

    def daily_schedule_for_date(self, target_date: str) -> list[str]:
        # Return all active lessons for one date.
        target_date_object = self.parse_date(target_date)
        schedule_rows = [
            {
                "date": occurrence["date"],
                "weekday": occurrence["weekday"],
                "start_time": occurrence["start_time"],
                "end_time": occurrence["end_time"],
                "lesson_minutes": occurrence["lesson_minutes"],
                "name": student.name,
                "instrument": student.instrument,
                "place": student.place,
            }
            for student in self.repo.list_students()
            for occurrence in self.get_student_occurrences(student.student_id, target_date_object.year, target_date_object.month)
            if not occurrence["cancelled"] and occurrence["date"] == target_date
        ]
        # Sort the schedule rows by date, start time, and student name for consistent display order.
        sorted_rows = sorted(schedule_rows, key=lambda row: (row["date"], row["start_time"], row["name"]))
        return [
            f"{row['date']} - {row['weekday']} - {row['start_time']}-{row['end_time']} ({row['lesson_minutes']}min) - {row['name']} - {row['instrument']} - {row['place']}"
            for row in sorted_rows
        ]

    def schedule_for_month(self, year: int, month: int) -> list[str]:
        # Return all active lessons for the month as display text.
        rows = [
            (
                occurrence["date"],
                occurrence["start_time"],
                f"{occurrence['date']} - {occurrence['weekday']} - {occurrence['start_time']}-{occurrence['end_time']} ({occurrence['lesson_minutes']}min) - {student.name}",
            )
            for student in self.repo.list_students()
            for occurrence in self.get_student_occurrences(student.student_id, year, month)
            if not occurrence["cancelled"]
        ]
        return [row[2] for row in sorted(rows, key=lambda row: (row[0], row[1]))]

    def monthly_income_statement(self, year: int, month: int) -> dict:
        # Return the monthly income summary used by the PDF exporter.
        statement_rows = []
        total_income = 0
        # For each student, calculate the number of active lessons in the month and the total fee for that student, then aggregate the total income for all students.
        for student in self.repo.list_students():
            active_occurrences = [
                occurrence
                for occurrence in self.get_student_occurrences(student.student_id, year, month)
                if not occurrence["cancelled"] and self.parse_date(occurrence["date"]).year == year and self.parse_date(occurrence["date"]).month == month
            ]
            # Calculate the total fee for the student based on the active lessons.
            lesson_count = len(active_occurrences)
            student_total = lesson_count * int(student.fee_hkd)
            if lesson_count == 0:
                continue
            # Append the student's statement row with their details and total fee for the month, and add to the total income.        
            statement_rows.append(
                {
                    "student_id": student.student_id,
                    "name": student.name,
                    "instrument": student.instrument,
                    "grade": student.grade,
                    "lesson_count": lesson_count,
                    "fee_per_lesson": int(student.fee_hkd),
                    "student_total": student_total,
                }
            )
            total_income += student_total
        # Sort the statement rows by student name for consistent display order, and return the statement data including the month, rows, and total income.
        return {"month": f"{year}-{month:02d}", "rows": statement_rows, "total_income": total_income}
