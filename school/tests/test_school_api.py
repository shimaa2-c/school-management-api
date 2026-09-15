from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from school.models import (
    TeacherProfile,
    StudentProfile,
    SchoolClass,
    Subject,
    ClassSubjectAssignment,
)


class SchoolListFeaturesTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="Teacher123!",
            role="teacher",
        )

        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher,
            employee_code="T001",
        )

        self.class_7a = SchoolClass.objects.create(
            name="7A",
            academic_year="2026/2027",
        )

        self.class_8b = SchoolClass.objects.create(
            name="8B",
            academic_year="2026/2027",
        )

        self.subject = Subject.objects.create(
            name="Mathematics",
            code="MATH101",
        )

        ClassSubjectAssignment.objects.create(
            school_class=self.class_7a,
            subject=self.subject,
            teacher=self.teacher_profile,
        )

        self.student_ali = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="ali",
                email="ali@example.com",
                password="Student123!",
                role="student",
            ),
            admission_no="ST001",
            school_class=self.class_7a,
        )

        self.student_ahmed = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="ahmed",
                email="ahmed@example.com",
                password="Student123!",
                role="student",
            ),
            admission_no="ST002",
            school_class=self.class_7a,
        )

        self.student_mohamed = StudentProfile.objects.create(
            user=User.objects.create_user(
                username="mohamed",
                email="mohamed@example.com",
                password="Student123!",
                role="student",
            ),
            admission_no="ST003",
            school_class=self.class_8b,
        )

        self.client.force_authenticate(
            user=self.teacher
        )

    def test_filter_students_by_class(self):
        response = self.client.get(
            f"/api/students/?school_class={self.class_7a.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        students = response.data["data"]

        self.assertEqual(
            len(students),
            2,
        )

        for student in students:
            self.assertEqual(
                student["school_class"],
                self.class_7a.id,
            )

    def test_search_students_by_username(self):
        response = self.client.get(
            "/api/students/?search=ali"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["success"],
            True,
        )

        students = response.data["data"]

        self.assertEqual(
            len(students),
            1,
        )

        self.assertEqual(
            students[0]["username"],
            "ali",
        )

    def test_search_students_by_admission_number(self):
        response = self.client.get(
            "/api/students/?search=ST002"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        students = response.data["data"]

        self.assertEqual(
            len(students),
            1,
        )

        self.assertEqual(
            students[0]["admission_no"],
            "ST002",
        )

    def test_order_students_by_admission_number(self):
        response = self.client.get(
            "/api/students/?ordering=admission_no"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        students = response.data["data"]

        self.assertEqual(
            students[0]["admission_no"],
            "ST001",
        )

        self.assertEqual(
            students[1]["admission_no"],
            "ST002",
        )

    def test_filter_classes_by_academic_year(self):
      response = self.client.get(
          "/api/classes/?academic_year=2026/2027"
      )

      self.assertEqual(
          response.status_code,
          status.HTTP_200_OK,
      )

      self.assertEqual(
          response.data["success"],
          True,
      )

      classes = response.data["data"]

      self.assertEqual(
          len(classes),
          1,
      )

      self.assertEqual(
          classes[0]["name"],
          "7A",
      )

      self.assertEqual(
          classes[0]["academic_year"],
          "2026/2027",
      )

    def test_search_classes_by_name(self):
        response = self.client.get(
            "/api/classes/?search=7A"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        classes = response.data["data"]

        self.assertEqual(
            len(classes),
            1,
        )

        self.assertEqual(
            classes[0]["name"],
            "7A",
        )