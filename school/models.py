from django.conf import settings
from django.db import models


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_code = models.CharField(
        max_length=50,
        unique=True
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.employee_code}"


class SchoolClass(models.Model):
    name = models.CharField(
        max_length=100
    )
    academic_year = models.CharField(
        max_length=20
    )
    homeroom_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='homeroom_classes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    admission_no = models.CharField(
        max_length=50,
        unique=True
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name='students'
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.admission_no}"


class ResponsibleProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responsible_profile'
    )
    phone = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.user.username


class StudentResponsible(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='responsible_links'
    )
    responsible = models.ForeignKey(
        ResponsibleProfile,
        on_delete=models.CASCADE,
        related_name='student_links'
    )
    relation_type = models.CharField(
        max_length=50
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'responsible'],
                name='unique_student_responsible'
            )
        ]

    def __str__(self):
        return (
            f"{self.responsible.user.username} -> "
            f"{self.student.user.username}"
        )


class Subject(models.Model):
    name = models.CharField(
        max_length=100
    )
    code = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class ClassSubjectAssignment(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='subject_assignments'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_assignments'
    )
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name='subject_assignments'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['school_class', 'subject', 'teacher'],
                name='unique_class_subject_teacher'
            )
        ]

    def __str__(self):
        return (
            f"{self.school_class} - "
            f"{self.subject} - "
            f"{self.teacher}"
        )


