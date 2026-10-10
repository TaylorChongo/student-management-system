"""JSON persistence for the student management system."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from course import Course
from student import GraduateStudent, Student, UndergraduateStudent

# Store the default file beside this module rather than depending on cwd.
DEFAULT_DATA_FILE = Path(__file__).with_name("student_data.json")


def load_data(
    data_file: Path = DEFAULT_DATA_FILE,
) -> tuple[dict[str, Student], dict[str, Course]]:
    """Load students and courses from disk, or return empty registries."""
    if not data_file.exists():
        return {}, {}

    try:
        raw_data = json.loads(data_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        # Keep the parser error chained while exposing a domain-specific
        # message to the application layer.
        raise ValueError(f"Could not read saved data: {data_file} is not valid JSON.") from error
    except OSError as error:
        raise OSError(f"Could not read saved data from {data_file}.") from error

    try:
        students = _load_students(raw_data.get("students", []))
        courses = _load_courses(raw_data.get("courses", []))
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Could not read saved data from {data_file}.") from error

    return students, courses


def save_data(
    students: dict[str, Student],
    courses: dict[str, Course],
    data_file: Path = DEFAULT_DATA_FILE,
) -> None:
    """Save students, courses, enrollments, and grades to disk."""
    data = {
        "students": [
            {
                "student_id": student.student_id,
                "name": student.name,
                "email": student.email,
                "type": student.student_type(),
                "course_ids": sorted(student.course_ids),
            }
            for student in students.values()
        ],
        "courses": [
            {
                "course_id": course.course_id,
                "title": course.title,
                "instructor": course.instructor,
                "student_ids": sorted(course.student_ids),
                "grades": course.grades,
            }
            for course in courses.values()
        ],
    }
    try:
        data_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        raise OSError(f"Could not save data to {data_file}.") from error


def _load_students(records: list[dict[str, Any]]) -> dict[str, Student]:
    students: dict[str, Student] = {}
    student_classes = {
        "Undergraduate": UndergraduateStudent,
        "Graduate": GraduateStudent,
    }
    for record in records:
        # The type field selects the concrete subclass during deserialization.
        student_class = student_classes[record["type"]]
        student = student_class(record["student_id"], record["name"], record["email"])
        for course_id in record.get("course_ids", []):
            student.add_course(course_id)
        students[student.student_id] = student
    return students


def _load_courses(records: list[dict[str, Any]]) -> dict[str, Course]:
    courses: dict[str, Course] = {}
    for record in records:
        course = Course(record["course_id"], record["title"], record["instructor"])
        for student_id in record.get("student_ids", []):
            course.add_student(student_id)
        # Grades are loaded after the roster because record_grade requires
        # every graded student to already be enrolled.
        for student_id, grade in record.get("grades", {}).items():
            course.record_grade(student_id, grade)
        courses[course.course_id] = course
    return courses
