from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from school.models import TeacherProfile, Subject, SchoolClass, ClassSubjectAssignment


class SubjectListTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher1",
            password="Teacher123!",
            role="teacher",
        )

        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher,
            employee_code="T001",
        )

        self.school_class = SchoolClass.objects.create(
            name="7A",
            academic_year="2026/2027",
        )

        self.math = Subject.objects.create(
            name="Mathematics",
            code="MATH101",
        )

        self.science = Subject.objects.create(
            name="Science",
            code="SCI101",
        )

        ClassSubjectAssignment.objects.create(
            school_class=self.school_class,
            subject=self.math,
            teacher=self.teacher_profile,
        )

        self.client.force_authenticate(
            user=self.teacher
        )

    def test_teacher_can_search_subject(self):
        response = self.client.get(
            "/api/subjects/?search=Math"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        subjects = response.data["data"]

        self.assertEqual(
            len(subjects),
            1,
        )

        self.assertEqual(
            subjects[0]["code"],
            "MATH101",
        )

    def test_teacher_can_search_subject_by_code(self):
        response = self.client.get(
            "/api/subjects/?search=SCI101"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        subjects = response.data["data"]

        # Teacher is only authorized to see Mathematics.
        self.assertEqual(
            len(subjects),
            0,
        )

    def test_subject_ordering(self):
        response = self.client.get(
            "/api/subjects/?ordering=name"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        subjects = response.data["data"]

        self.assertEqual(
            subjects[0]["name"],
            "Mathematics",
        )