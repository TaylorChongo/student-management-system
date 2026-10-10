"""Enrollment value object linking a student to a course."""

from __future__ import annotations

from dataclasses import dataclass


# frozen prevents an enrollment from changing after creation; slots avoids a
# per-instance __dict__ for this small value object.
@dataclass(frozen=True, slots=True)
class Enrollment:
    """Represent one student-course relationship."""

    student_id: str
    course_id: str

    def __post_init__(self) -> None:
        if not self.student_id.strip() or not self.course_id.strip():
            raise ValueError("Enrollment requires both student and course IDs.")
