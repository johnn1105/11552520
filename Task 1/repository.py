# =========================================================
# Repository layer for student storage.
# Defines an abstract repository interface 
# JSON-based implementation for storing student data.
# =========================================================
from __future__ import annotations# Allow forward references in type hints (for Python 3.7+ compatibility)

import json  # Used for reading/writing JSON data
from abc import ABC, abstractmethod  # Abstract base class
from pathlib import Path  # File system handling
from typing import Optional

from models import Student  # Domain model


class StudentRepository(ABC):
    # Abstract student repository.

    @abstractmethod
    def list_students(self) -> list[Student]:
        """Return all students."""

    @abstractmethod
    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Find a student by ID."""

    @abstractmethod
    def add(self, student: Student) -> None:
        """Persist a new student."""

    @abstractmethod
    def update(self, student: Student) -> None:
        """Persist changes for a student."""

    @abstractmethod
    def delete_by_id(self, student_id: int) -> None:
        """Delete a student by ID."""

    @abstractmethod
    def next_id(self) -> int:
        """Return the next available student ID."""


class JsonStudentRepository(StudentRepository):
    """JSON-backed student repository."""

    def __init__(self, filepath: str):
        # Ensure the JSON file exists and is initialized with an empty student list.
        self.file_path = Path(filepath)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save({"students": []})

    def _load(self) -> dict:
        # Load raw JSON data.
        try:
            with self.file_path.open("r", encoding="utf-8") as file_object:
                return json.load(file_object)
        except json.JSONDecodeError:
            return {"students": []}

    def _save(self, data: dict) -> None:
        # Write raw JSON data.
        with self.file_path.open("w", encoding="utf-8") as file_object:
            json.dump(data, file_object, ensure_ascii=False, indent=2)

    def list_students(self) -> list[Student]:
        # Return all student objects.
        return [Student.from_dict(item) for item in self._load().get("students", [])]

    def get_by_id(self, student_id: int) -> Optional[Student]:
        # Return the matching student or None.
        return next((student for student in self.list_students() if student.student_id == student_id), None)

    def add(self, student: Student) -> None:
        # Append a student record to the JSON file.
        data = self._load()
        data["students"] = [*data.get("students", []), student.to_dict()]
        self._save(data)

    def update(self, student: Student) -> None:
        # Replace a matching student record.
        data = self._load()
        student_dicts = data.get("students", [])
        matching_indexes = [index for index, item in enumerate(student_dicts) if int(item["student_id"]) == student.student_id]
        if not matching_indexes:
            raise ValueError("Student not found for update.")

        student_dicts[matching_indexes[0]] = student.to_dict()
        data["students"] = student_dicts
        self._save(data)

    def delete_by_id(self, student_id: int) -> None:
        # Delete a student if the ID exists.
        data = self._load()
        data["students"] = [item for item in data.get("students", []) if int(item["student_id"]) != student_id]
        self._save(data)

    def next_id(self) -> int:
        # Return the next available integer ID.
        student_ids = [student.student_id for student in self.list_students()]
        return max(student_ids, default=0) + 1
