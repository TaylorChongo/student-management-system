"""Enrollment value object linking a student to a course."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Enrollment:
    """Represent one student-course relationship."""

    student_id: str
    course_id: str

    def __post_init__(self) -> None:
        if not self.student_id.strip() or not self.course_id.strip():
            raise ValueError("Enrollment requires both student and course IDs.")
