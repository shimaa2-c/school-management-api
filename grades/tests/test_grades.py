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
from grades.models import Grade


class GradeTests(APITestCase):

    def setUp(self):
        # -----------------------------
        # Users
        # -----------------------------

        self.teacher_a = User.objects.create_user(
            username='teacher_a',
            email='teacher_a@example.com',
            password='Teacher123!',
            role='teacher',
        )

        self.teacher_a_profile = TeacherProfile.objects.create(
            user=self.teacher_a,
            employee_code='T001',
        )

        self.teacher_b = User.objects.create_user(
            username='teacher_b',
            email='teacher_b@example.com',
            password='Teacher123!',
            role='teacher',
        )

        self.teacher_b_profile = TeacherProfile.objects.create(
            user=self.teacher_b,
            employee_code='T002',
        )

        self.student_a = User.objects.create_user(
            username='student_a',
            email='student_a@example.com',
            password='Student123!',
            role='student',
        )

        self.student_b = User.objects.create_user(
            username='student_b',
            email='student_b@example.com',
            password='Student123!',
            role='student',
        )

        # -----------------------------
        # Classes
        # -----------------------------

        self.class_7a = SchoolClass.objects.create(
            name='7A',
            academic_year='2026/2027',
        )

        self.class_8b = SchoolClass.objects.create(
            name='8B',
            academic_year='2026/2027',
        )

        # -----------------------------
        # Subjects
        # -----------------------------

        self.math = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
        )

        self.science = Subject.objects.create(
            name='Science',
            code='SCI101',
        )

        # -----------------------------
        # Teacher assignments
        # -----------------------------

        ClassSubjectAssignment.objects.create(
            school_class=self.class_7a,
            subject=self.math,
            teacher=self.teacher_a_profile,
        )

        ClassSubjectAssignment.objects.create(
            school_class=self.class_8b,
            subject=self.science,
            teacher=self.teacher_b_profile,
        )

        # -----------------------------
        # Student profiles
        # -----------------------------

        self.student_a_profile = StudentProfile.objects.create(
            user=self.student_a,
            admission_no='ST001',
            school_class=self.class_7a,
        )

        self.student_b_profile = StudentProfile.objects.create(
            user=self.student_b,
            admission_no='ST002',
            school_class=self.class_8b,
        )

    def authenticate(self, user, password):
        response = self.client.post(
            '/api/auth/token/',
            {
                'username': user.username,
                'password': password,
            },
            format='json',
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )

    def test_teacher_can_create_grade_for_assigned_class_and_subject(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_7a.id,
                'subject': self.math.id,
                'term': 'first',
                'score': 90,
                'notes': 'Excellent',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Grade.objects.count(),
            1,
        )

        grade = Grade.objects.first()

        self.assertEqual(
            grade.teacher,
            self.teacher_a_profile,
        )

    def test_teacher_cannot_grade_unassigned_class(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_b_profile.id,
                'school_class': self.class_8b.id,
                'subject': self.math.id,
                'term': 'first',
                'score': 90,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_teacher_cannot_grade_unassigned_subject(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_7a.id,
                'subject': self.science.id,
                'term': 'first',
                'score': 90,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_teacher_cannot_grade_student_from_wrong_class(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_8b.id,
                'subject': self.science.id,
                'term': 'first',
                'score': 90,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_score_below_zero_is_rejected(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_7a.id,
                'subject': self.math.id,
                'term': 'first',
                'score': -1,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_score_above_100_is_rejected(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_7a.id,
                'subject': self.math.id,
                'term': 'first',
                'score': 101,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_grade_is_rejected(self):
        self.authenticate(
            self.teacher_a,
            'Teacher123!',
        )

        data = {
            'student': self.student_a_profile.id,
            'school_class': self.class_7a.id,
            'subject': self.math.id,
            'term': 'first',
            'score': 90,
        }

        first_response = self.client.post(
            '/api/grades/',
            data,
            format='json',
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_response = self.client.post(
            '/api/grades/',
            data,
            format='json',
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_student_cannot_create_grade(self):
        self.authenticate(
            self.student_a,
            'Student123!',
        )

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_7a.id,
                'subject': self.math.id,
                'term': 'first',
                'score': 90,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )