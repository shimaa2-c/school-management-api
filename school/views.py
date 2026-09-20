from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.responses import success_response
from core.responses import CustomResponseMixin

from .models import (
    StudentProfile,
    TeacherProfile,
    ResponsibleProfile,
    SchoolClass,
    Subject,
    ClassSubjectAssignment,
    StudentResponsible,
)

from .permissions import (
    StudentProfilePermission,
    TeacherProfilePermission,
    ResponsibleProfilePermission,
    SchoolClassPermission,
    SubjectPermission,
    ClassSubjectAssignmentPermission,
    StudentResponsiblePermission,
)

from .serializers import (
    StudentProfileSerializer,
    TeacherProfileSerializer,
    ResponsibleProfileSerializer,
    SchoolClassSerializer,
    ClassSubjectAssignmentSerializer,
    StudentResponsibleSerializer,
    SubjectSerializer,
)

from grades.models import Grade
from grades.serializers import GradeSerializer

def get_student_class_id(user):
    
    try:
        student_profile = user.student_profile
    except StudentProfile.DoesNotExist:
        return None

    return student_profile.school_class_id

class StudentProfileViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Students retrieved successfully.",
        "retrieve": "Student retrieved successfully.",
        "create": "Student created successfully.",
        "update": "Student updated successfully.",
        "partial_update": "Student updated successfully.",
        "destroy": "Student deleted successfully.",
    }

    serializer_class = StudentProfileSerializer
    permission_classes = [StudentProfilePermission]

    filterset_fields = ["school_class"]

    search_fields = [
        "user__username",
        "user__email",
        "admission_no",
    ]

    ordering_fields = [
        "user__username",
        "admission_no",
    ]

    ordering = ["admission_no"]

    def get_queryset(self):
        user = self.request.user

        queryset = StudentProfile.objects.select_related(
            "user",
            "school_class",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(
                school_class__subject_assignments__teacher__user_id=user.id
            ).distinct()

        if user.role == "student":
            return queryset.filter(
                user_id=user.id
            )

        if user.role == "responsible":
            return queryset.filter(
                responsible_links__responsible__user_id=user.id
            ).distinct()

        return queryset.none()
    
    def _validate_business_rules(self, data, instance=None):
        user = data.get(
            "user",
            instance.user if instance else None
        )

        if user.role != "student":
            return {
                "user": "The selected user must have the student role."
            }

        if (
            hasattr(user, "student_profile")
            and (
                instance is None
                or user.student_profile.id != instance.id
            )
        ):
            return {
                "user": "This user already has a student profile."
            }

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        student = serializer.save()

        return Response(
            {
                "message": "Student created successfully.",
                "data": self.get_serializer(student).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        student = self.get_object()

        serializer = self.get_serializer(
            student,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=student,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        student = serializer.save()

        return Response(
            {
                "message": "Student updated successfully.",
                "data": self.get_serializer(student).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        student = self.get_object()

        serializer = self.get_serializer(
            student,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=student,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        student = serializer.save()

        return Response(
            {
                "message": "Student updated successfully.",
                "data": self.get_serializer(student).data,
            },
            status=status.HTTP_200_OK,
        )


class TeacherProfileViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Teachers retrieved successfully.",
        "retrieve": "Teacher retrieved successfully.",
        "create": "Teacher created successfully.",
        "update": "Teacher updated successfully.",
        "partial_update": "Teacher updated successfully.",
        "destroy": "Teacher deleted successfully.",
    }

    serializer_class = TeacherProfileSerializer
    permission_classes = [TeacherProfilePermission]

    def get_queryset(self):
        user = self.request.user

        queryset = TeacherProfile.objects.select_related(
            "user"
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(
                user_id=user.id
            )

        return queryset.none()
    
    def _validate_business_rules(self, data, instance=None):
        user = data.get(
            "user",
            instance.user if instance else None
        )

        if user.role != "teacher":
            return {
                "user": "The selected user must have the teacher role."
            }

        if (
            hasattr(user, "teacher_profile")
            and (
                instance is None
                or user.teacher_profile.id != instance.id
            )
        ):
            return {
                "user": "This user already has a teacher profile."
            }

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher = serializer.save()

        return Response(
            {
                "message": "Teacher created successfully.",
                "data": self.get_serializer(teacher).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        teacher = self.get_object()

        serializer = self.get_serializer(
            teacher,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=teacher,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher = serializer.save()

        return Response(
            {
                "message": "Teacher updated successfully.",
                "data": self.get_serializer(teacher).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        teacher = self.get_object()

        serializer = self.get_serializer(
            teacher,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=teacher,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher = serializer.save()

        return Response(
            {
                "message": "Teacher updated successfully.",
                "data": self.get_serializer(teacher).data,
            },
            status=status.HTTP_200_OK,)


class ResponsibleProfileViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Responsibles retrieved successfully.",
        "retrieve": "Responsible retrieved successfully.",
        "create": "Responsible created successfully.",
        "update": "Responsible updated successfully.",
        "partial_update": "Responsible updated successfully.",
        "destroy": "Responsible deleted successfully.",
    }

    serializer_class = ResponsibleProfileSerializer
    permission_classes = [ResponsibleProfilePermission]

    def get_queryset(self):
        user = self.request.user

        queryset = ResponsibleProfile.objects.select_related(
            "user"
        )

        if user.role == "admin":
            return queryset

        if user.role == "responsible":
            return queryset.filter(
                user_id=user.id
            )

        return queryset.none()
    
    def _validate_business_rules(self, data, instance=None):
        user = data.get(
            "user",
            instance.user if instance else None
        )

        if user.role != "responsible":
            return {
                "user": (
                    "The selected user must have "
                    "the responsible role."
                )
            }

        if (
            hasattr(user, "responsible_profile")
            and (
                instance is None
                or user.responsible_profile.id != instance.id
            )
        ):
            return {
                "user": (
                    "This user already has "
                    "a responsible profile."
                )
            }

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        responsible = serializer.save()

        return Response(
            {
                "message": "Responsible created successfully.",
                "data": self.get_serializer(responsible).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        responsible = self.get_object()

        serializer = self.get_serializer(
            responsible,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=responsible,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        responsible = serializer.save()

        return Response(
            {
                "message": "Responsible updated successfully.",
                "data": self.get_serializer(responsible).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        responsible = self.get_object()

        serializer = self.get_serializer(
            responsible,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=responsible,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        responsible = serializer.save()

        return Response(
            {
                "message": "Responsible updated successfully.",
                "data": self.get_serializer(responsible).data,
            },
            status=status.HTTP_200_OK,
        )


class SchoolClassViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Classes retrieved successfully.",
        "retrieve": "Class retrieved successfully.",
        "create": "Class created successfully.",
        "update": "Class updated successfully.",
        "partial_update": "Class updated successfully.",
        "destroy": "Class deleted successfully.",
    }

    serializer_class = SchoolClassSerializer
    permission_classes = [SchoolClassPermission]

    filterset_fields = ["academic_year"]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
        "academic_year",
        "created_at",
    ]

    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user

        queryset = SchoolClass.objects.select_related(
            "homeroom_teacher__user"
        )

        
        if user.role == "admin":
            return queryset

        
        if user.role == "teacher":
            return queryset.filter(
                subject_assignments__teacher__user_id=user.id
            ).distinct()

        
        if user.role == "student":
            class_id = get_student_class_id(user)

            
            if class_id is None:
                return queryset.none()

            return queryset.filter(
                id=class_id
            )

        
        if user.role == "responsible":
            return queryset.filter(
                students__responsible_links__responsible__user_id=user.id
            ).distinct()

        return queryset.none()
    
    def _validate_business_rules(self, data, instance=None):
        teacher = data.get(
            "homeroom_teacher",
            instance.homeroom_teacher if instance else None
        )

        if teacher is not None and teacher.user.role != "teacher":
            return {
                "homeroom_teacher": (
                    "Homeroom teacher must have "
                    "the teacher role."
                )
            }

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        school_class = serializer.save()

        return Response(
            {
                "message": "Class created successfully.",
                "data": self.get_serializer(school_class).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        school_class = self.get_object()

        serializer = self.get_serializer(
            school_class,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=school_class,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        school_class = serializer.save()

        return Response(
            {
                "message": "Class updated successfully.",
                "data": self.get_serializer(school_class).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        school_class = self.get_object()

        serializer = self.get_serializer(
            school_class,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=school_class,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        school_class = serializer.save()

        return Response(
            {
                "message": "Class updated successfully.",
                "data": self.get_serializer(school_class).data,
            },
            status=status.HTTP_200_OK,
        )


class SubjectViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Subjects retrieved successfully.",
        "retrieve": "Subject retrieved successfully.",
        "create": "Subject created successfully.",
        "update": "Subject updated successfully.",
        "partial_update": "Subject updated successfully.",
        "destroy": "Subject deleted successfully.",
    }

    serializer_class = SubjectSerializer
    permission_classes = [SubjectPermission]

    search_fields = [
        "name",
        "code",
    ]

    ordering_fields = [
        "name",
        "code",
    ]

    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user

        queryset = Subject.objects.all()

        
        if user.role == "admin":
            return queryset

        
        if user.role == "teacher":
            return queryset.filter(
                class_assignments__teacher__user_id=user.id
            ).distinct()

        
        if user.role == "student":
            class_id = get_student_class_id(user)

            if class_id is None:
                return queryset.none()

            return queryset.filter(
                class_assignments__school_class_id=class_id
            ).distinct()

        
        if user.role == "responsible":
            return queryset.filter(
                class_assignments__school_class__students__responsible_links__responsible__user_id=user.id
            ).distinct()

        return queryset.none()


class ClassSubjectAssignmentViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Assignments retrieved successfully.",
        "retrieve": "Assignment retrieved successfully.",
        "create": "Assignment created successfully.",
        "update": "Assignment updated successfully.",
        "partial_update": "Assignment updated successfully.",
        "destroy": "Assignment deleted successfully.",
    }

    serializer_class = ClassSubjectAssignmentSerializer
    permission_classes = [ClassSubjectAssignmentPermission]

    def get_queryset(self):
        user = self.request.user

        queryset = ClassSubjectAssignment.objects.select_related(
            "school_class",
            "subject",
            "teacher__user",
        )

        
        if user.role == "admin":
            return queryset

        
        if user.role == "teacher":
            return queryset.filter(
                teacher__user_id=user.id
            )

        
        if user.role == "student":
            class_id = get_student_class_id(user)

            if class_id is None:
                return queryset.none()

            return queryset.filter(
                school_class_id=class_id
            )

        
        if user.role == "responsible":
            return queryset.filter(
                school_class__students__responsible_links__responsible__user_id=user.id
            ).distinct()

        return queryset.none()
    
    def _validate_business_rules(self, data, instance=None):
        teacher = data.get(
            "teacher",
            instance.teacher if instance else None
        )

        if teacher.user.role != "teacher":
            return {
                "teacher": (
                    "The selected user must have "
                    "the teacher role."
                )
            }

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        assignment = serializer.save()

        return Response(
            {
                "message": "Assignment created successfully.",
                "data": self.get_serializer(assignment).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()

        serializer = self.get_serializer(
            assignment,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=assignment,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        assignment = serializer.save()

        return Response(
            {
                "message": "Assignment updated successfully.",
                "data": self.get_serializer(assignment).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        assignment = self.get_object()

        serializer = self.get_serializer(
            assignment,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=assignment,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        assignment = serializer.save()

        return Response(
            {
                "message": "Assignment updated successfully.",
                "data": self.get_serializer(assignment).data,
            },
            status=status.HTTP_200_OK,
        )



class StudentResponsibleViewSet(
    CustomResponseMixin,
    viewsets.ModelViewSet,
):
    success_messages = {
        "list": "Student-responsible links retrieved successfully.",
        "retrieve": "Student-responsible link retrieved successfully.",
        "create": "Student-responsible link created successfully.",
        "update": "Student-responsible link updated successfully.",
        "partial_update": "Student-responsible link updated successfully.",
        "destroy": "Student-responsible link deleted successfully.",
    }

    serializer_class = StudentResponsibleSerializer
    permission_classes = [StudentResponsiblePermission]

    def get_queryset(self):
        user = self.request.user

        queryset = StudentResponsible.objects.select_related(
            "student__user",
            "student__school_class",
            "responsible__user",
        )

        
        if user.role == "admin":
            return queryset

        
        if user.role == "student":
            return queryset.filter(
                student__user_id=user.id
            )

        
        if user.role == "responsible":
            return queryset.filter(
                responsible__user_id=user.id
            )

        return queryset.none()
    
    def _validate_business_rules(self, data, instance=None):
        student = data.get(
            "student",
            instance.student if instance else None
        )

        responsible = data.get(
            "responsible",
            instance.responsible if instance else None
        )

        if student.user.role != "student":
            return {
                "student": (
                    "The selected user must have "
                    "the student role."
                )
            }

        if responsible.user.role != "responsible":
            return {
                "responsible": (
                    "The selected user must have "
                    "the responsible role."
                )
            }

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        relationship = serializer.save()

        return Response(
            {
                "message": "Student-responsible link created successfully.",
                "data": self.get_serializer(relationship).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        relationship = self.get_object()

        serializer = self.get_serializer(
            relationship,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=relationship,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        relationship = serializer.save()

        return Response(
            {
                "message": "Student-responsible link updated successfully.",
                "data": self.get_serializer(relationship).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        relationship = self.get_object()

        serializer = self.get_serializer(
            relationship,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        errors = self._validate_business_rules(
            serializer.validated_data,
            instance=relationship,
        )

        if errors:
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        relationship = serializer.save()

        return Response(
            {
                "message": "Student-responsible link updated successfully.",
                "data": self.get_serializer(relationship).data,
            },
            status=status.HTTP_200_OK,
        )


class StudentReportCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user

        try:
            student = StudentProfile.objects.select_related(
                "user",
                "school_class",
            ).get(pk=pk)

        except StudentProfile.DoesNotExist:
            from rest_framework.exceptions import NotFound

            raise NotFound(
                "Student not found."
            )

        if user.role == "admin":
            allowed = True

        elif user.role == "student":
            allowed = student.user_id == user.id

        elif user.role == "responsible":
            allowed = student.responsible_links.filter(
                responsible__user_id=user.id
            ).exists()

        elif user.role == "teacher":
            allowed = student.school_class.subject_assignments.filter(
                teacher__user_id=user.id
            ).exists()

        else:
            allowed = False

        if not allowed:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You do not have permission to view this report card."
            )

        grades = Grade.objects.select_related(
            "student__user",
            "school_class",
            "subject",
            "teacher__user",
        ).filter(
            student=student
        )

        serializer = GradeSerializer(
            grades,
            many=True,
            context={
                "request": request
            },
        )


        data = {
            "student": {
                "id": student.id,
                "username": student.user.username,
                "admission_no": student.admission_no,
                "school_class": student.school_class.name,
            },
            "grades": serializer.data,
        }

        return success_response(
            data=data,
            message="Student report card retrieved successfully.",
            status=status.HTTP_200_OK,
            request=request,
        )