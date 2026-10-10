"""Student domain models.

The module demonstrates encapsulation, inheritance, polymorphism, class
methods, static methods, and magic methods required by the project brief.
"""

# Postpones annotation evaluation so the Student return type can refer to the
# class while it is still being defined.
from __future__ import annotations

from abc import ABC, abstractmethod


class Student(ABC):
    """Base class shared by all student types."""

    def __init__(self, student_id: str, name: str, email: str) -> None:
        if not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        if "@" not in email:
            raise ValueError("Student email must contain '@'.")

        self._student_id = student_id.strip()
        self._name = name.strip()
        self._email = email.strip()
        # Keep the mutable collection private; callers receive a read-only
        # snapshot through the course_ids property.
        self._course_ids: set[str] = set()

    @property
    def student_id(self) -> str:
        """Return the immutable identity used to identify this student."""
        return self._student_id

    @property
    def name(self) -> str:
        """Return the student's display name."""
        return self._name

    @property
    def email(self) -> str:
        """Return the student's email address."""
        return self._email

    @property
    def course_ids(self) -> frozenset[str]:
        """Expose enrollments without allowing callers to mutate the set."""
        # A frozenset prevents external code from changing the private set.
        return frozenset(self._course_ids)

    def add_course(self, course_id: str) -> None:
        """Record a course enrollment once."""
        self._course_ids.add(course_id)

    def remove_course(self, course_id: str) -> None:
        """Remove an enrollment when a student is withdrawn."""
        self._course_ids.discard(course_id)

    @classmethod
    def from_record(cls, record: dict[str, str]) -> Student:
        """Build a student from a dictionary-like data record."""
        # cls preserves the concrete subclass when this factory is inherited.
        return cls(record["student_id"], record["name"], record["email"])

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Perform the small validation needed by this console application."""
        # rsplit limits the check to the domain portion after the final "@".
        return "@" in email and "." in email.rsplit("@", 1)[-1]

    @abstractmethod
    def student_type(self) -> str:
        """Return the type-specific label used in reports."""

    def __repr__(self) -> str:
        # !r makes whitespace and empty values visible in debug output.
        return (
            f"{type(self).__name__}(student_id={self.student_id!r}, "
            f"name={self.name!r}, email={self.email!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            # Returning NotImplemented lets Python try the reflected comparison
            # instead of declaring unrelated types equal.
            return NotImplemented
        return self.student_id == other.student_id

    def __hash__(self) -> int:
        return hash(self.student_id)


class UndergraduateStudent(Student):
    """Student enrolled in an undergraduate programme."""

    def student_type(self) -> str:
        return "Undergraduate"


class GraduateStudent(Student):
    """Student enrolled in a graduate programme."""

    def student_type(self) -> str:
        return "Graduate"
