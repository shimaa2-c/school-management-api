from rest_framework import status, viewsets
from rest_framework.response import Response

from core.responses import CustomResponseMixin
from school.models import ClassSubjectAssignment

from .models import Grade
from .permissions import GradePermission
from .serializers import GradeSerializer


class GradeViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):

    serializer_class = GradeSerializer
    permission_classes = [GradePermission]

    success_messages = {
        "list": "Grades retrieved successfully.",
        "retrieve": "Grade retrieved successfully.",
        "create": "Grade created successfully.",
        "update": "Grade updated successfully.",
        "partial_update": "Grade updated successfully.",
        "destroy": "Grade deleted successfully.",
    }

    filterset_fields = [
        'student',
        'school_class',
        'subject',
        'term',
    ]

    ordering_fields = [
        'score',
        'created_at',
        'updated_at',
    ]

    ordering = [
        '-created_at',
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Grade.objects.select_related(
            'student__user',
            'school_class',
            'subject',
            'teacher__user',
        )

        if user.role == 'admin':
            return queryset

        if user.role == 'teacher':
            return queryset.filter(
                school_class__subject_assignments__teacher__user_id=user.id
            ).distinct()

        if user.role == 'student':
            return queryset.filter(
                student__user_id=user.id
            )

        if user.role == 'responsible':
            return queryset.filter(
                student__responsible_links__responsible__user_id=user.id
            ).distinct()

        return queryset.none()

    def _validate_grade_business_rules(self, data, grade=None):

        student = data.get(
            'student',
            grade.student if grade else None
        )

        school_class = data.get(
            'school_class',
            grade.school_class if grade else None
        )

        subject = data.get(
            'subject',
            grade.subject if grade else None
        )

        teacher = data.get(
            'teacher',
            grade.teacher if grade else None
        )

        score = data.get(
            'score',
            grade.score if grade else None
        )

        user = self.request.user


        if score is not None and (score < 0 or score > 100):

            return {
                'score': 'Score must be between 0 and 100.'
            }, status.HTTP_400_BAD_REQUEST


        if student and school_class:

            if student.school_class_id != school_class.id:

                return {
                    'school_class': (
                        'The selected class does not belong '
                        'to this student.'
                    )
                }, status.HTTP_400_BAD_REQUEST


        if user.role == 'teacher':

            teacher_profile = user.teacher_profile

            teacher = teacher_profile

            if school_class and subject:

                assignment_exists = (
                    ClassSubjectAssignment.objects.filter(
                        school_class=school_class,
                        subject=subject,
                        teacher=teacher_profile,
                    ).exists()
                )

                if not assignment_exists:

                    return {
                        'subject': (
                            'You are not assigned to this '
                            'subject for this class.'
                        )
                    }, status.HTTP_403_FORBIDDEN


        elif user.role == 'admin':

            if not teacher:

                return {
                    'teacher': 'This field is required for Admin.'
                }, status.HTTP_400_BAD_REQUEST

        else:

            return {
                'error': 'You are not allowed to manage grades.'
            }, status.HTTP_403_FORBIDDEN

        return {
            'teacher': teacher
        }, None

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        business_data, error_status = (
            self._validate_grade_business_rules(
                serializer.validated_data
            )
        )

        if error_status:

            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': business_data,
                },
                status=error_status
            )

        grade = serializer.save(
            teacher=business_data['teacher']
        )

        return Response(
            {
                'message': 'Grade created successfully.',
                'data': self.get_serializer(grade).data,
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        grade = self.get_object()

        serializer = self.get_serializer(
            grade,
            data=request.data,
        )

        if not serializer.is_valid():

            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        business_data, error_status = (
            self._validate_grade_business_rules(
                serializer.validated_data,
                grade=grade
            )
        )

        if error_status:

            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': business_data,
                },
                status=error_status
            )

        grade = serializer.save(
            teacher=business_data['teacher']
        )

        return Response(
            {
                'message': 'Grade updated successfully.',
                'data': self.get_serializer(grade).data,
            },
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):

        grade = self.get_object()

        serializer = self.get_serializer(
            grade,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():

            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        business_data, error_status = (
            self._validate_grade_business_rules(
                serializer.validated_data,
                grade=grade
            )
        )

        if error_status:

            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': business_data,
                },
                status=error_status
            )

        grade = serializer.save(
            teacher=business_data['teacher']
        )

        return Response(
            {
                'message': 'Grade updated successfully.',
                'data': self.get_serializer(grade).data,
            },
            status=status.HTTP_200_OK
        )

