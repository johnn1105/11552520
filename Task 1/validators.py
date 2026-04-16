# =========================================================
# Validation helpers for user input and persistence data
# =========================================================
from __future__ import annotations # Allow forward references in type hints (for Python 3.7+ compatibility)
from datetime import date # Date handling for validating date strings
from constants import ALLOWED_GRADES, ALLOWED_LESSON_MINUTES, ALLOWED_PLACES, ALLOWED_WEEKDAYS, PLAN_TYPES # Allowed values for various fields


class ValidationError(ValueError):
    """Custom validation error used across CLI, GUI, and services."""


class InputValidator:
    """Centralized validation to keep UI code small and consistent."""

    @staticmethod
    def validate_non_empty_text(value: str, field_name: str) -> str:
        """Validate a required text field."""
        normalized_value = str(value).strip()
        if not normalized_value:
            raise ValidationError(f"{field_name} cannot be empty.")
        return normalized_value

    @staticmethod
    def validate_positive_integer(value: int | str, field_name: str) -> int:
        """Validate a positive integer field."""
        try:
            normalized_value = int(str(value).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError(f"{field_name} must be an integer.") from error

        if normalized_value <= 0:
            raise ValidationError(f"{field_name} must be a positive integer.")
        return normalized_value

    @staticmethod
    def validate_name(name_text: str) -> str:
        """Validate a student name string."""
        normalized_name = InputValidator.validate_non_empty_text(name_text, "Name")
        if not all(character.isalpha() or character in " -'" for character in normalized_name):
            raise ValidationError("Name can contain only letters, spaces, hyphens, and apostrophes.")
        return normalized_name

    @staticmethod
    def validate_instrument(instrument_text: str) -> str:
        """Validate an instrument name."""
        return InputValidator.validate_non_empty_text(instrument_text, "Instrument")

    @staticmethod
    def parse_date(date_text: str, field_name: str = "Date") -> date:
        """Parse a YYYY-MM-DD string into a date object."""
        normalized_date = InputValidator.validate_non_empty_text(date_text, field_name)
        parts = normalized_date.split("-")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise ValidationError(f"{field_name} must be in YYYY-MM-DD format.")
        year, month, day = map(int, parts)
        try:
            return date(year, month, day)
        except ValueError as error:
            raise ValidationError(str(error)) from error

    @staticmethod
    def validate_date_text(date_text: str, field_name: str = "Date") -> str:
        """Validate and normalize a YYYY-MM-DD date string."""
        return InputValidator.parse_date(date_text, field_name).isoformat()

    @staticmethod
    def validate_time_hhmm(time_text: str, field_name: str = "Start time") -> str:
        """Validate a four-digit HHMM time string."""
        normalized_time = InputValidator.validate_non_empty_text(time_text, field_name)
        if len(normalized_time) != 4 or not normalized_time.isdigit():
            raise ValidationError(f"{field_name} must be 4 digits, for example 1300.")

        hour = int(normalized_time[:2])
        minute = int(normalized_time[2:])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValidationError(f"Invalid {field_name.lower()}. Please use HHMM format.")
        return normalized_time

    @staticmethod
    def validate_weekday(weekday_text: str) -> str:
        """Validate the lesson weekday."""
        normalized_weekday = InputValidator.validate_non_empty_text(weekday_text, "Lesson weekday")
        if normalized_weekday not in ALLOWED_WEEKDAYS:
            raise ValidationError(f"Lesson weekday must be one of: {', '.join(ALLOWED_WEEKDAYS)}")
        return normalized_weekday

    @staticmethod
    def validate_place(place_text: str) -> str:
        """Validate the lesson location."""
        normalized_place = InputValidator.validate_non_empty_text(place_text, "Place")
        if normalized_place not in ALLOWED_PLACES:
            raise ValidationError(f"Place must be one of: {', '.join(ALLOWED_PLACES)}")
        return normalized_place

    @staticmethod
    def validate_grade(grade_text: str) -> str:
        """Validate grade text against the supported grade list."""
        normalized_grade = InputValidator.validate_non_empty_text(grade_text, "Grade").upper()
        if normalized_grade not in ALLOWED_GRADES:
            raise ValidationError(f"Grade must be one of: {', '.join(ALLOWED_GRADES)}")
        return normalized_grade

    @staticmethod
    def validate_lesson_minutes(lesson_minutes: int | str) -> int:
        """Validate lesson duration."""
        try:
            normalized_minutes = int(lesson_minutes)
        except (TypeError, ValueError) as error:
            raise ValidationError("Lesson minutes must be an integer.") from error

        if normalized_minutes not in ALLOWED_LESSON_MINUTES:
            raise ValidationError(f"Lesson minutes must be one of: {ALLOWED_LESSON_MINUTES}")
        return normalized_minutes

    @staticmethod
    def validate_fee_hkd(fee_value: int | str) -> int:
        """Validate lesson fee in HKD."""
        try:
            normalized_fee = int(str(fee_value).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError("Fee must be an integer.") from error

        if normalized_fee < 0:
            raise ValidationError("Fee cannot be negative.")
        return normalized_fee

    @staticmethod
    def validate_student_id(student_id: int | str) -> int:
        """Validate a student ID."""
        return InputValidator.validate_positive_integer(student_id, "Student ID")

    @staticmethod
    def parse_month_text(month_text: str) -> tuple[int, int]:
        """Parse YYYY-MM text into year and month numbers."""
        normalized_month = InputValidator.validate_non_empty_text(month_text, "Month")
        parts = normalized_month.split("-")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            raise ValidationError("Month must be in YYYY-MM format.")

        year, month = map(int, parts)
        if not 1 <= month <= 12:
            raise ValidationError("Month must be between 01 and 12.")
        return year, month

    @staticmethod
    def validate_plan_type(plan_type_text: str) -> str:
        """Validate the scheduling mode."""
        normalized_plan_type = InputValidator.validate_non_empty_text(plan_type_text, "Plan type").lower()
        if normalized_plan_type not in PLAN_TYPES:
            raise ValidationError(f"Plan type must be one of: {', '.join(PLAN_TYPES)}")
        return normalized_plan_type

    @staticmethod
    def validate_flexible_lesson(lesson_item: dict, default_lesson_minutes: int = 45) -> dict:
        """Validate one flexible lesson dictionary."""
        lesson_date = InputValidator.validate_date_text(str(lesson_item.get("date", "")).strip(), "Lesson date")
        start_time = InputValidator.validate_time_hhmm(str(lesson_item.get("start_time", "")).strip(), "Start time")
        lesson_minutes = InputValidator.validate_lesson_minutes(lesson_item.get("lesson_minutes", default_lesson_minutes))
        return {
            "date": lesson_date,
            "start_time": start_time,
            "lesson_minutes": lesson_minutes,
        }
