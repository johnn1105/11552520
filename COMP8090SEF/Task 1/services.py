# services.py
# Business logic layer: validate inputs, generate schedule, etc.

from __future__ import annotations
from datetime import date, datetime, timedelta
from typing import List, Optional

from models import Student
from repository import StudentRepository

WEEKDAY_MAP = {
    "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6
}

class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo
    def list_students(self) -> List[Student]:
        """Return all students from repository (used by GUI/CLI)."""
        return self.repo.list_students()
    def ensure_default_student(self) -> None:
        """
        Default case:
        If no student exists, auto-create multiple demo students
        for testing the system.
        """

        if self.repo.list_students():
            return

        default_students = [
            ("John Chan", "2001-01-01", "Trumpet", 8, 45, 500, "Mon", "Studio"),
            ("Alan Lee", "2002-03-12", "Piano", 6, 45, 450, "Tue", "Studio"),
            ("Jace Wong", "2003-07-20", "Violin", 5, 45, 400, "Wed", "Home"),
            ("Mary Ho", "2000-11-02", "Flute", 7, 45, 480, "Thu", "Studio"),
            ("Chris Lau", "2004-09-14", "Drums", 4, 60, 550, "Fri", "Home"),
            ("Emily Ng", "2005-05-10", "Guitar", 6, 45, 420, "Sat", "Studio"),
            ("David Chan", "2002-12-25", "Saxophone", 7, 45, 500, "Sun", "Home"),
            ("Sophia Lam", "2003-08-18", "Cello", 5, 60, 530, "Mon", "Studio"),
            ("Daniel Cheung", "2001-04-30", "Clarinet", 6, 45, 460, "Tue", "Home"),
            ("Kevin Yeung", "2004-06-22", "Trombone", 5, 45, 470, "Wed", "Studio"),
        ]

        for student_data in default_students:
            sid = self.repo.next_id()

            name, birth, instrument, grade, mins, fee, weekday, place = student_data

            y, m, d = map(int, birth.split("-"))

            student = Student(
                student_id=sid,
                name=name,
                birth_date=date(y, m, d),
                instrument=instrument,
                grade=grade,
                lesson_minutes=mins,
                fee_hkd=fee,
                lesson_weekday=weekday,
                place=place,
            )

            self.repo.add(student)
            
    def add_student(
        self,
        name: str,
        birth_date_str: str,  # yyyy-mm-dd
        instrument: str,
        grade: int,
        lesson_minutes: int,
        fee_hkd: int,
        lesson_weekday: str,
        place: str
    ) -> Student:
        # Basic validation
        if lesson_weekday not in WEEKDAY_MAP:
            raise ValueError("lesson_weekday must be one of Mon..Sun")
        if place not in ("Studio", "Home"):
            raise ValueError("place must be Studio or Home")

        y, m, d = map(int, birth_date_str.split("-"))
        bd = date(y, m, d)

        student = Student(
            student_id=self.repo.next_id(),
            name=name.strip(),
            birth_date=bd,
            instrument=instrument.strip(),
            grade=int(grade),
            lesson_minutes=int(lesson_minutes),
            fee_hkd=int(fee_hkd),
            lesson_weekday=lesson_weekday,
            place=place
        )
        self.repo.add(student)
        return student

    def update_student(self, student: Student) -> None:
        self.repo.update(student)

    def delete_student_by_id(self, student_id: int) -> None:
        self.repo.delete_by_id(student_id)

    def find_by_name(self, keyword: str) -> List[Student]:
        keyword = keyword.lower().strip()
        return [s for s in self.repo.list_students() if keyword in s.name.lower()]

    def lesson_dates_in_month(self, year: int, month: int, weekday: str) -> List[str]:
        """
        Return all lesson dates (ISO strings) in a given month for a given weekday.
        Example: 2026-02 + Mon => 2026-02-02, 09, 16, 23
        """
        target = WEEKDAY_MAP[weekday]
        first_day = date(year, month, 1)

        # Find first target weekday in the month
        offset = (target - first_day.weekday()) % 7
        first_lesson = first_day + timedelta(days=offset)

        # Iterate by 7 days until month changes
        result = []
        cur = first_lesson
        while cur.month == month:
            result.append(cur.isoformat())
            cur += timedelta(days=7)
        return result

    def schedule_for_month(self, year: int, month: int) -> List[tuple[str, str]]:
        """
        Show my schedule (one month):
        Returns list of (student_name, date)
        """
        schedule = []
        for s in self.repo.list_students():
            for dt in self.lesson_dates_in_month(year, month, s.lesson_weekday):
                schedule.append((s.name, dt))
        schedule.sort(key=lambda x: x[1])
        return schedule