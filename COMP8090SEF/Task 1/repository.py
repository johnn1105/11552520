# repository.py
# Abstract repository 

import json
import os
from abc import ABC, abstractmethod
from typing import List, Optional

from models import Student

class StudentRepository(ABC):
    @abstractmethod
    def list_students(self) -> List[Student]:
        pass

    @abstractmethod
    def get_by_id(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    def add(self, student: Student) -> None:
        pass

    @abstractmethod
    def update(self, student: Student) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, student_id: int) -> None:
        pass

    @abstractmethod
    def next_id(self) -> int:
        pass


class JsonStudentRepository(StudentRepository):
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            # Create default empty storage
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"students": []}, f, ensure_ascii=False, indent=2)

    def _load(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: dict) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def list_students(self) -> List[Student]:
        data = self._load()
        return [Student.from_dict(x) for x in data.get("students", [])]

    def get_by_id(self, student_id: int) -> Optional[Student]:
        for s in self.list_students():
            if s.student_id == student_id:
                return s
        return None

    def add(self, student: Student) -> None:
        data = self._load()
        students = data.get("students", [])
        students.append(student.to_dict())
        data["students"] = students
        self._save(data)

    def update(self, student: Student) -> None:
        data = self._load()
        students = data.get("students", [])
        updated = False
        for i, d in enumerate(students):
            if int(d["student_id"]) == student.student_id:
                students[i] = student.to_dict()
                updated = True
                break
        if not updated:
            raise ValueError("Student not found for update.")
        data["students"] = students
        self._save(data)

    def delete_by_id(self, student_id: int) -> None:
        data = self._load()
        students = data.get("students", [])
        students = [d for d in students if int(d["student_id"]) != student_id]
        data["students"] = students
        self._save(data)

    def next_id(self) -> int:
        students = self.list_students()
        if not students:
            return 1
        return max(s.student_id for s in students) + 1
