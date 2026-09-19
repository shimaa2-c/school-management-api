from rest_framework import viewsets
from core.responses import CustomResponseMixin
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        errors = serializer.validate_data(
            serializer.to_internal_value(request.data)
        )

        if errors:
            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        if request.user.role == 'teacher':
            data['teacher'] = request.user.teacher_profile

        grade = Grade.objects.create(**data)

        response_serializer = self.get_serializer(grade)

        return Response(
            {
                'message': 'Grade created successfully.',
                'data': response_serializer.data,
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        grade = self.get_object()

        serializer = self.get_serializer(
            grade,
            data=request.data
        )

        data = serializer.to_internal_value(request.data)

        errors = serializer.validate_data(data)

        if errors:
            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.role == 'teacher':
            data['teacher'] = request.user.teacher_profile

        for field, value in data.items():
            setattr(grade, field, value)

        grade.save()

        response_serializer = self.get_serializer(grade)

        return Response(
            {
                'message': 'Grade updated successfully.',
                'data': response_serializer.data,
            },
            status=status.HTTP_200_OK
    )

    def partial_update(self, request, *args, **kwargs):

        grade = self.get_object()

        serializer = self.get_serializer(
            grade,
            data=request.data,
            partial=True
        )

        data = serializer.to_internal_value(request.data)

        errors = serializer.validate_data(data)

        if errors:
            return Response(
                {
                    'message': 'Validation failed.',
                    'errors': errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.role == 'teacher':
            data['teacher'] = request.user.teacher_profile

        for field, value in data.items():
            setattr(grade, field, value)

        grade.save()

        response_serializer = self.get_serializer(grade)

        return Response(
            {
                'message': 'Grade updated successfully.',
                'data': response_serializer.data,
            },
            status=status.HTTP_200_OK
        )

    # def perform_create(self, serializer):
    #     user = self.request.user

    #     if user.role == 'teacher':
    #         serializer.save(
    #             teacher=user.teacher_profile
    #         )
    #     else:
    #         serializer.save()