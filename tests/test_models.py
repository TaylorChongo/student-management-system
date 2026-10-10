"""Focused tests for the stage-one domain models."""

import unittest

from course import Course
from enrollment import Enrollment
from student import GraduateStudent, UndergraduateStudent


class ModelTests(unittest.TestCase):
    def test_student_subclasses_share_identity_equality(self) -> None:
        first = UndergraduateStudent("S001", "Alex", "alex@example.com")
        same_identity = GraduateStudent("S001", "Different", "other@example.com")

        self.assertEqual(first, same_identity)
        self.assertEqual(first.student_type(), "Undergraduate")
        self.assertEqual(same_identity.student_type(), "Graduate")

    def test_course_roster_is_unique_and_grades_are_validated(self) -> None:
        course = Course("CS101", "Python Basics", "Dr. Lee")
        course.add_student("S001")
        course.add_student("S001")
        course.record_grade("S001", 92)

        self.assertEqual(course.student_ids, frozenset({"S001"}))
        self.assertEqual(course.grades, {"S001": 92.0})
        with self.assertRaises(ValueError):
            course.record_grade("S002", 80)

    def test_enrollment_is_hashable(self) -> None:
        # Equal frozen dataclass instances collapse to one set entry.
        enrollments = {Enrollment("S001", "CS101"), Enrollment("S001", "CS101")}

        self.assertEqual(len(enrollments), 1)


if __name__ == "__main__":
    unittest.main()
