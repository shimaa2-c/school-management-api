from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from grades.models import Grade
from school.models import (
    TeacherProfile,
    StudentProfile,
    SchoolClass,
    Subject,
    ClassSubjectAssignment,
)


class GradeListFeaturesTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher1",
            password="TestPass123!",
            role="teacher",
        )

        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher,
            employee_code="T001",
        )

        self.school_class = SchoolClass.objects.create(
            name="7A",
            academic_year="2025/2026",
        )

        self.subject = Subject.objects.create(
            name="Math",
            code="MATH",
        )

        ClassSubjectAssignment.objects.create(
            school_class=self.school_class,
            subject=self.subject,
            teacher=self.teacher_profile,
        )

        self.student = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="student1",
                password="TestPass123!",
                role="student",
            ),
            admission_no="S001",
            school_class=self.school_class,
        )

        self.client.force_authenticate(
            user=self.teacher
        )

        Grade.objects.create(
            student=self.student,
            school_class=self.school_class,
            subject=self.subject,
            teacher=self.teacher_profile,
            term="term1",
            score=70,
        )

        Grade.objects.create(
            student=self.student,
            school_class=self.school_class,
            subject=self.subject,
            teacher=self.teacher_profile,
            term="term2",
            score=90,
        )

    def test_filter_by_term(self):
        response = self.client.get(
            "/api/grades/?term=term1"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        data = response.data["data"]

        self.assertEqual(
            len(data),
            1,
        )

        self.assertEqual(
            data[0]["term"],
            "term1",
        )

    def test_filter_by_student(self):
        response = self.client.get(
            f"/api/grades/?student={self.student.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        data = response.data["data"]

        self.assertEqual(
            len(data),
            2,
        )

        for grade in data:
            self.assertEqual(
                grade["student"],
                self.student.id,
            )

    def test_ordering_by_score(self):
        response = self.client.get(
            "/api/grades/?ordering=score"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        data = response.data["data"]

        self.assertEqual(
            data[0]["score"],
            "70.00",
        )

        self.assertEqual(
            data[1]["score"],
            "90.00",
        )

    def test_pagination_meta_exists(self):
        response = self.client.get(
            "/api/grades/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        self.assertIn(
            "meta",
            response.data,
        )

        self.assertIn(
            "pagination",
            response.data["meta"],
        )