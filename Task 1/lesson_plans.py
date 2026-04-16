# =========================================================
# Lesson plan strategies for regular and flexible students
# =========================================================
from __future__ import annotations # For forward references in type hints (e.g., LessonOccurrence)

from abc import ABC, abstractmethod  # Used to define abstract base class (interface)

from models import LessonOccurrence, Student

class LessonPlan(ABC):
    # Strategy interface for lesson occurrence generation.

    @abstractmethod
    def get_occurrences(self, schedule_service, student: Student, year: int, month: int) -> list[LessonOccurrence]:
        """Return concrete lesson occurrences for the target month."""


class RegularLessonPlan(LessonPlan):
    """Generate lesson occurrences from a fixed weekly schedule."""

    def get_occurrences(self, schedule_service, student: Student, year: int, month: int) -> list[LessonOccurrence]:
        student.lesson_overrides = student.lesson_overrides or {}
        base_dates = schedule_service.lesson_dates_in_month(year, month, student.lesson_weekday)
        occurrences: list[LessonOccurrence] = []
        # First, process the base schedule and apply any overrides (cancellations or moves)
        for original_date in base_dates:
            override_data = student.lesson_overrides.get(original_date)
            if not override_data:
                occurrences.append(
                    schedule_service.build_occurrence(
                        student=student,
                        original_date=original_date,
                        actual_date=original_date,
                        start_time=student.lesson_start_time,
                        lesson_minutes=student.lesson_minutes,
                        cancelled=False,
                        is_override=False,
                    )
                )
                continue
            # Apply any overrides (cancellations or moves)
            cancelled = bool(override_data.get("cancelled", False))
            actual_date = str(override_data.get("date", original_date))
            start_time = str(override_data.get("start_time", student.lesson_start_time))
            lesson_minutes = int(override_data.get("lesson_minutes", student.lesson_minutes))
            actual_date_object = schedule_service.parse_date(actual_date)
            # Only include the occurrence if it's cancelled (to show in schedule) or if the new date is in the target month
            if cancelled:
                occurrences.append(
                    schedule_service.build_occurrence(
                        student=student,
                        original_date=original_date,
                        actual_date=original_date,
                        start_time=student.lesson_start_time,
                        lesson_minutes=student.lesson_minutes,
                        cancelled=True,
                        is_override=True,
                    )
                )
            # If not cancelled, only include if the new date is still in the same month (moved within month)
            elif actual_date_object.year == year and actual_date_object.month == month:
                occurrences.append(
                    schedule_service.build_occurrence(
                        student=student,
                        original_date=original_date,
                        actual_date=actual_date,
                        start_time=start_time,
                        lesson_minutes=lesson_minutes,
                        cancelled=False,
                        is_override=True,
                    )
                )
        # Next, add any moved-in lessons that are not part of the original schedule
        moved_in_occurrences = [
            schedule_service.build_occurrence(
                student=student,
                original_date=original_date,
                actual_date=str(override_data.get("date", original_date)),
                start_time=str(override_data.get("start_time", student.lesson_start_time)),
                lesson_minutes=int(override_data.get("lesson_minutes", student.lesson_minutes)),
                cancelled=False,
                is_override=True,
            )
            for original_date, override_data in student.lesson_overrides.items()
            if original_date not in base_dates
            and not bool(override_data.get("cancelled", False))
            and schedule_service.parse_date(str(override_data.get("date", original_date))).year == year
            and schedule_service.parse_date(str(override_data.get("date", original_date))).month == month
        ]
        # Add moved-in lessons to the occurrences list
        occurrences.extend(moved_in_occurrences)
        return sorted(occurrences, key=lambda item: (item.date, item.start_time, item.original_date))


class FlexibleLessonPlan(LessonPlan):
    # Generate lesson occurrences from explicitly stored lesson dates.

    def get_occurrences(self, schedule_service, student: Student, year: int, month: int) -> list[LessonOccurrence]:
        # For flexible students, we ignore the base schedule and just use the custom lessons defined in student.custom_lessons.
        student.custom_lessons = student.custom_lessons or []
        occurrences = [
            schedule_service.build_occurrence(
                student=student,
                original_date=str(lesson_item["date"]),
                actual_date=str(lesson_item["date"]),
                start_time=str(lesson_item["start_time"]),
                lesson_minutes=int(lesson_item.get("lesson_minutes", student.lesson_minutes)),
                cancelled=False,
                is_override=False,
            )
            # Only include lessons that are in the target month
            for lesson_item in student.custom_lessons
            if schedule_service.parse_date(str(lesson_item["date"])).year == year
            and schedule_service.parse_date(str(lesson_item["date"])).month == month
        ]
        # Sort occurrences by date, start time, and original date
        return sorted(occurrences, key=lambda item: (item.date, item.start_time, item.original_date))
