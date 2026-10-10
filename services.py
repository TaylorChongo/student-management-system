"""Reusable business functions and report abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from course import Course
from enrollment import Enrollment
from student import Student


def add_student(
    students: dict[str, Student],
    student: Student,
    *tags: str,
    **metadata: str,
) -> Student:
    """Add a student to an ID-indexed registry.

    ``tags`` and ``metadata`` demonstrate flexible function arguments while
    keeping the registry focused on the domain object.
    """
    del tags, metadata  # Reserved for future filtering and audit metadata.
    if student.student_id in students:
        raise ValueError(f"Student '{student.student_id}' already exists.")
    students[student.student_id] = student
    return student


def add_course(
    courses: dict[str, Course],
    course: Course,
    *labels: str,
    **metadata: str,
) -> Course:
    """Add a course to an ID-indexed registry."""
    del labels, metadata
    if course.course_id in courses:
        raise ValueError(f"Course '{course.course_id}' already exists.")
    courses[course.course_id] = course
    return course


def enroll_student(
    students: dict[str, Student],
    courses: dict[str, Course],
    student_id: str,
    course_id: str,
) -> Enrollment:
    """Enroll a known student in a known course."""
    student = students.get(student_id)
    course = courses.get(course_id)
    if student is None:
        raise KeyError(f"Student '{student_id}' was not found.")
    if course is None:
        raise KeyError(f"Course '{course_id}' was not found.")
    if course_id in student.course_ids:
        raise ValueError("Student is already enrolled in this course.")

    student.add_course(course_id)
    course.add_student(student_id)
    return Enrollment(student_id, course_id)


def calculate_average(grades: Iterable[float]) -> float:
    """Return the arithmetic mean, or zero when no grades exist."""
    values = [float(grade) for grade in grades]
    return sum(values) / len(values) if values else 0.0


def calculate_course_average(course: Course) -> float:
    """Calculate the average of all grades recorded for a course."""
    return calculate_average(course.grades.values())


def students_for_course(
    students: dict[str, Student],
    course: Course,
) -> list[Student]:
    """Return enrolled student objects using a list comprehension."""
    return [students[student_id] for student_id in course.student_ids if student_id in students]


class Report(ABC):
    """Abstract report contract used for polymorphic reporting."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a human-readable report."""


class StudentReport(Report):
    """Generate a report for one student."""

    def __init__(self, student: Student, courses: dict[str, Course]) -> None:
        self.student = student
        self.courses = courses

    def generate(self) -> str:
        course_names = [
            self.courses[course_id].title
            for course_id in sorted(self.student.course_ids)
            if course_id in self.courses
        ]
        courses_text = ", ".join(course_names) if course_names else "No courses"
        return (
            f"{self.student.name} ({self.student.student_type()})\n"
            f"Student ID: {self.student.student_id}\n"
            f"Email: {self.student.email}\n"
            f"Courses: {courses_text}"
        )


class CourseReport(Report):
    """Generate a roster and average report for one course."""

    def __init__(self, course: Course, students: dict[str, Student]) -> None:
        self.course = course
        self.students = students

    def generate(self) -> str:
        roster = [
            self.students[student_id].name
            for student_id in sorted(self.course.student_ids)
            if student_id in self.students
        ]
        roster_text = ", ".join(roster) if roster else "No students"
        return (
            f"{self.course.course_id}: {self.course.title}\n"
            f"Instructor: {self.course.instructor}\n"
            f"Roster: {roster_text}\n"
            f"Average: {calculate_course_average(self.course):.2f}"
        )
