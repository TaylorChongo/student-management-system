"""Menu-driven console entry point for the student management system."""

from __future__ import annotations

from collections.abc import Callable

from course import Course
from services import (
    CourseReport,
    StudentReport,
    add_course,
    add_student,
    enroll_student,
)
from student import GraduateStudent, Student, UndergraduateStudent

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


def print_menu(output: OutputFunction = print) -> None:
    """Display the available user and instructor actions."""
    output(
        "\nStudent Course Management System\n"
        "1. Register student\n"
        "2. Add course\n"
        "3. Enroll student in course\n"
        "4. Record grade\n"
        "5. View student summary\n"
        "6. View course roster and average\n"
        "7. List students\n"
        "8. List courses\n"
        "0. Exit"
    )


def register_student(
    students: dict[str, Student],
    input_fn: InputFunction = input,
    output: OutputFunction = print,
) -> None:
    """Collect and register a new undergraduate or graduate student."""
    student_id = input_fn("Student ID: ")
    name = input_fn("Name: ")
    email = input_fn("Email: ")
    student_type = input_fn("Type (U for undergraduate, G for graduate): ").upper()
    student_class = GraduateStudent if student_type == "G" else UndergraduateStudent
    add_student(students, student_class(student_id, name, email))
    output(f"Registered {name.strip()} successfully.")


def add_course_from_input(
    courses: dict[str, Course],
    input_fn: InputFunction = input,
    output: OutputFunction = print,
) -> None:
    """Collect and add a course."""
    course = Course(
        input_fn("Course ID: "),
        input_fn("Course title: "),
        input_fn("Instructor: "),
    )
    add_course(courses, course)
    output(f"Added course {course.course_id} successfully.")


def run_cli(
    input_fn: InputFunction = input,
    output: OutputFunction = print,
) -> None:
    """Run the application until the user selects Exit."""
    students: dict[str, Student] = {}
    courses: dict[str, Course] = {}

    while True:
        print_menu(output)
        choice = input_fn("Choose an option: ").strip()
        try:
            if choice == "1":
                register_student(students, input_fn, output)
            elif choice == "2":
                add_course_from_input(courses, input_fn, output)
            elif choice == "3":
                student_id = input_fn("Student ID: ")
                course_id = input_fn("Course ID: ")
                enroll_student(students, courses, student_id, course_id)
                output("Enrollment completed successfully.")
            elif choice == "4":
                course_id = input_fn("Course ID: ")
                student_id = input_fn("Student ID: ")
                grade = float(input_fn("Grade (0-100): "))
                courses[course_id].record_grade(student_id, grade)
                output("Grade recorded successfully.")
            elif choice == "5":
                student_id = input_fn("Student ID: ")
                output(StudentReport(students[student_id], courses).generate())
            elif choice == "6":
                course_id = input_fn("Course ID: ")
                output(CourseReport(courses[course_id], students).generate())
            elif choice == "7":
                output("\n".join(map(str, students.values())) or "No students registered.")
            elif choice == "8":
                output("\n".join(map(str, courses.values())) or "No courses available.")
            elif choice == "0":
                output("Goodbye.")
                return
            else:
                output("Invalid option. Please choose a listed menu option.")
        except (KeyError, ValueError) as error:
            # Expected user-input errors are shown without terminating the CLI.
            output(f"Error: {error}")


if __name__ == "__main__":
    run_cli()
