"""Course domain model."""

from __future__ import annotations


class Course:
    """Represent a course and the unique students enrolled in it."""

    def __init__(self, course_id: str, title: str, instructor: str) -> None:
        if not course_id.strip():
            raise ValueError("Course ID cannot be empty.")
        if not title.strip():
            raise ValueError("Course title cannot be empty.")
        if not instructor.strip():
            raise ValueError("Instructor name cannot be empty.")

        self._course_id = course_id.strip()
        self._title = title.strip()
        self._instructor = instructor.strip()
        self._student_ids: set[str] = set()
        self._grades: dict[str, float] = {}

    @property
    def course_id(self) -> str:
        return self._course_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def instructor(self) -> str:
        return self._instructor

    @property
    def student_ids(self) -> frozenset[str]:
        # Expose a snapshot so consumers cannot mutate the roster directly.
        return frozenset(self._student_ids)

    @property
    def grades(self) -> dict[str, float]:
        # Return a shallow copy to preserve ownership of the internal mapping.
        return self._grades.copy()

    def add_student(self, student_id: str) -> None:
        """Add a student to the roster; sets prevent duplicate enrollment."""
        self._student_ids.add(student_id)

    def remove_student(self, student_id: str) -> None:
        # discard is intentionally used because withdrawal is idempotent.
        self._student_ids.discard(student_id)
        self._grades.pop(student_id, None)

    def record_grade(self, student_id: str, grade: float) -> None:
        if student_id not in self._student_ids:
            raise ValueError("Only enrolled students can receive a grade.")
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100.")
        # Normalize integer and floating-point inputs to one stored type.
        self._grades[student_id] = float(grade)

    def __repr__(self) -> str:
        # !r keeps the representation unambiguous when values contain spaces.
        return (
            f"Course(course_id={self.course_id!r}, title={self.title!r}, "
            f"instructor={self.instructor!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            # Let Python try the other operand's comparison implementation.
            return NotImplemented
        return self.course_id == other.course_id

    def __hash__(self) -> int:
        return hash(self.course_id)
