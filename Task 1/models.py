# =========================================================
# Domain models for the music lesson system.
# Represents the data layer
# Used across services, repository, CLI, and GUI
# =========================================================
from __future__ import annotations

from abc import ABC, abstractmethod  # Abstract base class support
from dataclasses import dataclass, field  # Simplified class creation
from datetime import date # Date handling for student birth dates and lesson occurrences
from typing import Any # For flexible type hints in dictionaries

from validators import InputValidator  # Central validation logic


class Person(ABC):
    # Base class for domain entities that can be displayed by name.

    @abstractmethod
    def display_name(self) -> str:
        """Return a human-readable name for the object."""


@dataclass
class LessonOccurrence:
    """A concrete lesson occurrence for a calendar date."""

    original_date: str
    date: str
    weekday: str
    start_time: str
    end_time: str
    lesson_minutes: int
    cancelled: bool = False
    is_override: bool = False

    @property
    def display_text(self) -> str:
        # Return the formatted lesson text used by CLI and GUI.
        suffix_text = " [CANCELLED]" if self.cancelled else " [CHANGED]" if self.is_override else ""
        return f"{self.date} - {self.weekday} - {self.start_time}-{self.end_time} ({self.lesson_minutes}min){suffix_text}"

    def to_dict(self) -> dict[str, Any]:
        # Convert the occurrence into a dictionary for UI layers.
        return {
            "original_date": self.original_date,
            "date": self.date,
            "weekday": self.weekday,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "lesson_minutes": self.lesson_minutes,
            "cancelled": self.cancelled,
            "is_override": self.is_override,
            "display_text": self.display_text,
        }


@dataclass
class Student(Person):
    """Student entity stored in JSON."""

    student_id: int
    name: str
    birth_date: date
    instrument: str
    grade: str
    lesson_minutes: int
    lesson_start_time: str
    fee_hkd: int
    lesson_weekday: str
    place: str
    plan_type: str = "regular"
    lesson_overrides: dict[str, dict[str, Any]] = field(default_factory=dict)
    custom_lessons: list[dict[str, Any]] = field(default_factory=list)

    @property
    def is_flexible(self) -> bool:
        # Return True when the student uses flexible scheduling.
        return self.plan_type == "flexible"

    @property
    def mode_label(self) -> str:
        # Return the text shown in CLI and GUI tables.
        return "Flexible" if self.is_flexible else "Regular"

    def display_name(self) -> str:
        # Return a human-readable display name.
        return f"{self.name} (#{self.student_id})"

    def to_dict(self) -> dict[str, Any]:
        # Serialize the student for JSON storage.
        return {
            "student_id": self.student_id,
            "name": self.name,
            "birth_date": self.birth_date.isoformat(),
            "instrument": self.instrument,
            "grade": self.grade,
            "lesson_minutes": int(self.lesson_minutes),
            "lesson_start_time": self.lesson_start_time,
            "fee_hkd": int(self.fee_hkd),
            "lesson_weekday": self.lesson_weekday,
            "place": self.place,
            "plan_type": self.plan_type,
            "lesson_overrides": self.lesson_overrides,
            "custom_lessons": self.custom_lessons,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Student":
        # Build a student from JSON data.
        birth_date = InputValidator.parse_date(str(data["birth_date"]), "Birth date")
        lesson_overrides = data.get("lesson_overrides", {}) if isinstance(data.get("lesson_overrides", {}), dict) else {}
        custom_lessons = data.get("custom_lessons", []) if isinstance(data.get("custom_lessons", []), list) else []
        plan_type = InputValidator.validate_plan_type(str(data.get("plan_type", "regular"))) if str(data.get("plan_type", "regular")).strip().lower() in {"regular", "flexible"} else "regular"
        # Validate all fields and construct the Student object.
        return cls(
            student_id=InputValidator.validate_student_id(data["student_id"]),
            name=InputValidator.validate_name(str(data["name"])),
            birth_date=birth_date,
            instrument=InputValidator.validate_instrument(str(data["instrument"])),
            grade=InputValidator.validate_grade(str(data.get("grade", ""))),
            lesson_minutes=InputValidator.validate_lesson_minutes(data.get("lesson_minutes", 45)),
            lesson_start_time=InputValidator.validate_time_hhmm(str(data.get("lesson_start_time", "1300"))),
            fee_hkd=InputValidator.validate_fee_hkd(data["fee_hkd"]),
            lesson_weekday=InputValidator.validate_weekday(str(data.get("lesson_weekday", "Mon"))),
            place=InputValidator.validate_place(str(data["place"])),
            plan_type=plan_type,
            lesson_overrides=lesson_overrides,
            custom_lessons=[InputValidator.validate_flexible_lesson(item, data.get("lesson_minutes", 45)) for item in custom_lessons],
        )


@dataclass
class Invoice:
    # Invoice data used for PDF generation.
    invoice_no: str
    month: str
    student_name: str
    instrument: str
    grade: str
    lesson_dates: list[str]
    lesson_details: list[str]
    fee_hkd: int
    total_hkd: int
