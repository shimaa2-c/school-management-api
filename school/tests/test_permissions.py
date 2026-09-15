from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from school.models import (
    TeacherProfile,
    StudentProfile,
    ResponsibleProfile,
    StudentResponsible,
    SchoolClass,
    Subject,
    ClassSubjectAssignment,
)


class PermissionTests(APITestCase):

    def setUp(self):
        # Admin
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Admin123!',
            role='admin',
        )

        # Teacher A
        self.teacher_a = User.objects.create_user(
            username='teacher_a',
            email='teacher_a@example.com',
            password='Teacher123!',
            role='teacher',
        )

        self.teacher_a_profile = TeacherProfile.objects.create(
            user=self.teacher_a,
            employee_code='T001',
            phone='01000000001',
        )

        # Teacher B
        self.teacher_b = User.objects.create_user(
            username='teacher_b',
            email='teacher_b@example.com',
            password='Teacher123!',
            role='teacher',
        )

        self.teacher_b_profile = TeacherProfile.objects.create(
            user=self.teacher_b,
            employee_code='T002',
            phone='01000000002',
        )

        # Classes
        self.class_7a = SchoolClass.objects.create(
            name='7A',
            academic_year='2026/2027',
            homeroom_teacher=self.teacher_a_profile,
        )

        self.class_8b = SchoolClass.objects.create(
            name='8B',
            academic_year='2026/2027',
            homeroom_teacher=self.teacher_b_profile,
        )

        # Subjects
        self.math = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
        )

        self.science = Subject.objects.create(
            name='Science',
            code='SCI101',
        )

        # Teacher A teaches Math in 7A
        ClassSubjectAssignment.objects.create(
            school_class=self.class_7a,
            subject=self.math,
            teacher=self.teacher_a_profile,
        )

        # Teacher B teaches Science in 8B
        ClassSubjectAssignment.objects.create(
            school_class=self.class_8b,
            subject=self.science,
            teacher=self.teacher_b_profile,
        )

        # Student A
        self.student_a = User.objects.create_user(
            username='student_a',
            email='student_a@example.com',
            password='Student123!',
            role='student',
        )

        self.student_a_profile = StudentProfile.objects.create(
            user=self.student_a,
            admission_no='ST001',
            school_class=self.class_7a,
        )

        # Student B
        self.student_b = User.objects.create_user(
            username='student_b',
            email='student_b@example.com',
            password='Student123!',
            role='student',
        )

        self.student_b_profile = StudentProfile.objects.create(
            user=self.student_b,
            admission_no='ST002',
            school_class=self.class_8b,
        )

        # Responsible A
        self.responsible_a = User.objects.create_user(
            username='responsible_a',
            email='responsible_a@example.com',
            password='Responsible123!',
            role='responsible',
        )

        self.responsible_a_profile = ResponsibleProfile.objects.create(
            user=self.responsible_a,
            phone='01100000001',
        )

        # Responsible A is linked only to Student A
        StudentResponsible.objects.create(
            student=self.student_a_profile,
            responsible=self.responsible_a_profile,
            relation_type='father',
        )

    def authenticate(self, user):
        response = self.client.post(
            '/api/auth/token/',
            {
                'username': user.username,
                'password': self.get_password(user),
            },
            format='json',
        )

        access_token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

    def get_password(self, user):
        passwords = {
            self.admin.username: 'Admin123!',
            self.teacher_a.username: 'Teacher123!',
            self.teacher_b.username: 'Teacher123!',
            self.student_a.username: 'Student123!',
            self.student_b.username: 'Student123!',
            self.responsible_a.username: 'Responsible123!',
        }

        return passwords[user.username]
    
    def test_student_can_see_only_own_profile(self):
        self.authenticate(self.student_a)

        response = self.client.get(
            f'/api/students/{self.student_a_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_student_cannot_see_another_student(self):
        self.authenticate(self.student_a)

        response = self.client.get(
            f'/api/students/{self.student_b_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_student_list_contains_only_their_profile(self):
        self.authenticate(self.student_a)

        response = self.client.get(
            '/api/students/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        students = response.data['data']

        self.assertEqual(
            len(students),
            1,
        )

        self.assertEqual(
            students[0]['id'],
            self.student_a_profile.id,
        )

    def test_teacher_can_see_assigned_students(self):
        self.authenticate(self.teacher_a)

        response = self.client.get('/api/students/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        students = response.data['data']

        self.assertEqual(len(students), 1)
        self.assertEqual(
            students[0]['id'],
            self.student_a_profile.id,
        )

    def test_teacher_cannot_see_students_from_unassigned_class(self):
        self.authenticate(self.teacher_a)

        response = self.client.get(
            f'/api/students/{self.student_b_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_teacher_cannot_create_student_profile(self):
        self.authenticate(self.teacher_a)

        response = self.client.post(
            '/api/students/',
            {
                'user': self.student_b.id,
                'admission_no': 'ST003',
                'school_class': self.class_7a.id,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_teacher_can_see_own_profile(self):
        self.authenticate(self.teacher_a)

        response = self.client.get(
            f'/api/teachers/{self.teacher_a_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_teacher_cannot_see_another_teacher_profile(self):
        self.authenticate(self.teacher_a)

        response = self.client.get(
            f'/api/teachers/{self.teacher_b_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
    
    def test_responsible_can_see_linked_student(self):
        self.authenticate(self.responsible_a)

        response = self.client.get(
            f'/api/students/{self.student_a_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_responsible_cannot_see_unlinked_student(self):
        self.authenticate(self.responsible_a)

        response = self.client.get(
            f'/api/students/{self.student_b_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_responsible_list_contains_only_linked_students(self):
        self.authenticate(self.responsible_a)

        response = self.client.get(
            '/api/students/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        students = response.data['data']

        self.assertEqual(
            len(students),
            1,
        )

        self.assertEqual(
            students[0]['id'],
            self.student_a_profile.id,
        )

    def test_responsible_can_see_own_profile(self):
        self.authenticate(self.responsible_a)

        response = self.client.get(
            f'/api/responsibles/{self.responsible_a_profile.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_responsible_cannot_create_grade(self):
        self.authenticate(self.responsible_a)

        response = self.client.post(
            '/api/grades/',
            {
                'student': self.student_a_profile.id,
                'school_class': self.class_7a.id,
                'subject': self.math.id,
                'term': 'first',
                'score': 90,
                'notes': 'Test',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )