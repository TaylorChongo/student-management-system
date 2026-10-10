"""Focused tests for business services and reports."""

import unittest

from course import Course
from services import (
    CourseReport,
    StudentReport,
    add_course,
    add_student,
    calculate_average,
    enroll_student,
)
from student import UndergraduateStudent


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.students = {}
        self.courses = {}
        add_student(
            self.students,
            UndergraduateStudent("S001", "Alex", "alex@example.com"),
            "active",
            cohort="2026",
        )
        add_course(self.courses, Course("CS101", "Python Basics", "Dr. Lee"))

    def test_enrollment_updates_both_sides(self) -> None:
        enrollment = enroll_student(self.students, self.courses, "S001", "CS101")

        self.assertEqual(enrollment.student_id, "S001")
        self.assertIn("CS101", self.students["S001"].course_ids)
        self.assertIn("S001", self.courses["CS101"].student_ids)

    def test_average_handles_empty_and_non_empty_grades(self) -> None:
        self.assertEqual(calculate_average([]), 0.0)
        self.assertEqual(calculate_average([80, 90, 100]), 90.0)

    def test_reports_use_student_polymorphism(self) -> None:
        enroll_student(self.students, self.courses, "S001", "CS101")
        self.courses["CS101"].record_grade("S001", 95)

        student_report = StudentReport(self.students["S001"], self.courses).generate()
        course_report = CourseReport(self.courses["CS101"], self.students).generate()

        self.assertIn("Undergraduate", student_report)
        self.assertIn("Average: 95.00", course_report)


if __name__ == "__main__":
    unittest.main()
