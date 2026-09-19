from rest_framework import serializers

from school.models import ClassSubjectAssignment, TeacherProfile
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
            'created_at',
            'updated_at',
        ]
    def validate_data(self,attrs):
        errors={}
        student=attrs.get('student',getattr(self.instance, 'student', None))
        school_class=attrs.get('school_class',getattr(self.instance, 'school_class', None))
        subject=attrs.get('subject',getattr(self.instance, 'subject', None))
        teacher=attrs.get('teacher',getattr(self.instance, 'teacher', None))
        request=self.context.get('request')

        if 'score' in attrs:
            score = attrs['score']
            if score < 0 or score > 100:
                errors['score'] = 'Score must be between 0 and 100.'
        
        if student and school_class:
            if student.school_class_id != school_class.id:
                errors['school_class'] = (
                    'The selected class does not belong '
                    'to this student.'
                )
        
        if request:
            user = request.user

            if user.role == 'teacher':

                teacher_profile = user.teacher_profile

                if teacher and teacher != teacher_profile:
                    errors['teacher'] = (
                        'You can only manage your own grades.'
                    )

                if school_class and subject:

                    assignment_exists = (
                        ClassSubjectAssignment.objects.filter(
                            school_class=school_class,
                            subject=subject,
                            teacher=teacher_profile,
                        ).exists()
                    )

                    if not assignment_exists:
                        errors['subject'] = (
                            'You are not assigned to this subject '
                            'for this class.'
                        )

            elif user.role == 'admin':

                if self.instance is None and not teacher:
                    errors['teacher'] = (
                        'Teacher is required for Admin.'
                    )

        return errors
    
    # def validate_score(self, value):
    #     if value < 0 or value > 100:
    #         raise serializers.ValidationError(
    #             'Score must be between 0 and 100.'
    #         )
    #     return value

    # def validate(self, attrs):
    #     student = attrs.get('student')
    #     school_class = attrs.get('school_class')
    #     subject = attrs.get('subject')

    #     # Validate student/class relationship.
    #     if student and school_class:
    #         if student.school_class_id != school_class.id:
    #             raise serializers.ValidationError({
    #                 'school_class': (
    #                     'The selected class does not belong '
    #                     'to this student.'
    #                 )
    #             })

    #     request = self.context.get('request')

    #     if request:
    #         if request.user.role == 'teacher':
    #             teacher_profile = request.user.teacher_profile

    #             # Never allow a teacher to choose another teacher.
    #             attrs['teacher'] = teacher_profile

    #             if school_class and subject:
    #                 assignment_exists = (
    #                     ClassSubjectAssignment.objects.filter(
    #                         school_class=school_class,
    #                         subject=subject,
    #                         teacher=teacher_profile,
    #                     ).exists()
    #                 )

    #                 if not assignment_exists:
    #                     raise serializers.ValidationError({
    #                         'subject': (
    #                             'You are not assigned to this subject '
    #                             'for this class.'
    #                         )
    #                     })

    #         elif request.user.role == 'admin':
    #             if not attrs.get('teacher'):
    #                 raise serializers.ValidationError({
    #                     'teacher': 'This field is required for Admin.'
    #                 })

    #     return attrs