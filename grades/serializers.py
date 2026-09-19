from rest_framework import serializers

from school.models import TeacherProfile
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):

    teacher = serializers.PrimaryKeyRelatedField(
        queryset=TeacherProfile.objects.all(),
        required=False
    )

    student_name = serializers.CharField(
        source='student.user.username',
        read_only=True
    )

    class_name = serializers.CharField(
        source='school_class.name',
        read_only=True
    )

    subject_name = serializers.CharField(
        source='subject.name',
        read_only=True
    )

    teacher_name = serializers.CharField(
        source='teacher.user.username',
        read_only=True
    )

    class Meta:
        model = Grade

        fields = [
            'id',
            'student',
            'student_name',
            'school_class',
            'class_name',
            'subject',
            'subject_name',
            'teacher',
            'teacher_name',
            'term',
            'score',
            'notes',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'student_name',
            'class_name',
            'subject_name',
            'teacher_name',
            'created_at',
            'updated_at',
        ]

