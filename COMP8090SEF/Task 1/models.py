# models.py

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from abc import ABC, abstractmethod

class Person(ABC):

    @abstractmethod
    def display_name(self) -> str:
        pass

@dataclass
class Student(Person):
    student_id: int
    name: str
    birth_date: date
    instrument: str
    grade: int
    lesson_minutes: int
    fee_hkd: int
    lesson_weekday: str   
    place: str           

    def display_name(self) -> str:
        return f"{self.name} (#{self.student_id})"

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "birth_date": self.birth_date.isoformat(),
            "instrument": self.instrument,
            "grade": self.grade,
            "lesson_minutes": self.lesson_minutes,
            "fee_hkd": self.fee_hkd,
            "lesson_weekday": self.lesson_weekday,
            "place": self.place,
        }

    @staticmethod
    def from_dict(d: dict) -> "Student":
        """Create Student from dict."""
        y, m, day = map(int, d["birth_date"].split("-"))
        return Student(
            student_id=int(d["student_id"]),
            name=d["name"],
            birth_date=date(y, m, day),
            instrument=d["instrument"],
            grade=int(d["grade"]),
            lesson_minutes=int(d["lesson_minutes"]),
            fee_hkd=int(d["fee_hkd"]),
            lesson_weekday=d["lesson_weekday"],
            place=d["place"],
        )

@dataclass
class Invoice:
    invoice_no: str
    month: str        
    student_name: str
    instrument: str
    grade: int
    lesson_dates: list[str]
    fee_hkd: int
    total_hkd: int
