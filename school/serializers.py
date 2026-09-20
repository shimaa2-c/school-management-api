from rest_framework import serializers

from .models import (
    TeacherProfile,
    StudentProfile,
    ResponsibleProfile,
    StudentResponsible,
    SchoolClass,
    Subject,
    ClassSubjectAssignment,
)


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = TeacherProfile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'employee_code',
            'phone',
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
        ]

    # def validate_user(self, user):
    #     if user.role != 'teacher':
    #         raise serializers.ValidationError(
    #             'The selected user must have the teacher role.'
    #         )

    #     if hasattr(user, 'teacher_profile'):
    #         raise serializers.ValidationError(
    #             'This user already has a teacher profile.'
    #         )

    #     return user


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )
    class_name = serializers.CharField(
        source='school_class.name',
        read_only=True
    )

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'admission_no',
            'school_class',
            'class_name',
            'date_of_birth',
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'class_name',
        ]

    # def validate_user(self, user):
    #     if user.role != 'student':
    #         raise serializers.ValidationError(
    #             'The selected user must have the student role.'
    #         )

    #     if hasattr(user, 'student_profile'):
    #         raise serializers.ValidationError(
    #             'This user already has a student profile.'
    #         )

    #     return user


class ResponsibleProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = ResponsibleProfile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'phone',
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
        ]

    # def validate_user(self, user):
    #     if user.role != 'responsible':
    #         raise serializers.ValidationError(
    #             'The selected user must have the responsible role.'
    #         )

    #     if hasattr(user, 'responsible_profile'):
    #         raise serializers.ValidationError(
    #             'This user already has a responsible profile.'
    #         )

    #     return user


class StudentResponsibleSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student.user.username',
        read_only=True,
    )
    responsible_name = serializers.CharField(
        source='responsible.user.username',
        read_only=True,
    )

    class Meta:
        model = StudentResponsible
        fields = [
            'id',
            'student',
            'student_name',
            'responsible',
            'responsible_name',
            'relation_type',
        ]
        read_only_fields = [
            'id',
            'student_name',
            'responsible_name',
        ]

    # def validate_student(self, student):
    #     if student.user.role != 'student':
    #         raise serializers.ValidationError(
    #             'The selected user must have the student role.'
    #         )

    #     return student

    # def validate_responsible(self, responsible):
    #     if responsible.user.role != 'responsible':
    #         raise serializers.ValidationError(
    #             'The selected user must have the responsible role.'
    #         )

    #     return responsible


class SchoolClassSerializer(serializers.ModelSerializer):
    homeroom_teacher_name = serializers.CharField(
        source='homeroom_teacher.user.username',
        read_only=True,
    )

    class Meta:
        model = SchoolClass
        fields = [
            'id',
            'name',
            'academic_year',
            'homeroom_teacher',
            'homeroom_teacher_name',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'homeroom_teacher_name',
        ]

    # def validate_homeroom_teacher(self, teacher):
    #     if teacher is not None and teacher.user.role != 'teacher':
    #         raise serializers.ValidationError(
    #             'Homeroom teacher must have the teacher role.'
    #         )

    #     return teacher

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'name',
            'code',
        ]
        
class ClassSubjectAssignmentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(
        source='school_class.name',
        read_only=True,
    )
    subject_name = serializers.CharField(
        source='subject.name',
        read_only=True,
    )
    teacher_name = serializers.CharField(
        source='teacher.user.username',
        read_only=True,
    )

    class Meta:
        model = ClassSubjectAssignment
        fields = [
            'id',
            'school_class',
            'class_name',
            'subject',
            'subject_name',
            'teacher',
            'teacher_name',
        ]
        read_only_fields = [
            'id',
            'class_name',
            'subject_name',
            'teacher_name',
        ]

    # def validate_teacher(self, teacher):
    #     if teacher.user.role != 'teacher':
    #         raise serializers.ValidationError(
    #             'The selected user must have the teacher role.'
    #         )

    #     return teacher