from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from accounts.views import UserViewSet
from school.views import (
    StudentProfileViewSet,
    TeacherProfileViewSet,
    ResponsibleProfileViewSet,
    SchoolClassViewSet,
    SubjectViewSet,
    ClassSubjectAssignmentViewSet,
    StudentResponsibleViewSet,
)
from grades.views import GradeViewSet


router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='user',
)

router.register(
    'students',
    StudentProfileViewSet,
    basename='student',
)

router.register(
    'teachers',
    TeacherProfileViewSet,
    basename='teacher',
)

router.register(
    'responsibles',
    ResponsibleProfileViewSet,
    basename='responsible',
)

router.register(
    'classes',
    SchoolClassViewSet,
    basename='school-class',
)

router.register(
    'subjects',
    SubjectViewSet,
    basename='subject',
)

router.register(
    'class-subjects',
    ClassSubjectAssignmentViewSet,
    basename='class-subject',
)

router.register(
    'grades',
    GradeViewSet,
    basename='grade',
)
router.register(
    'student-responsibles',
    StudentResponsibleViewSet,
    basename='student-responsible',
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/',
        include(router.urls),
    ),

    path(
        'api/auth/',
        include('accounts.urls'),
    ),

    path(
        'api/',
        include('school.urls'),
    ),

    # OpenAPI schema
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),

    # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url='/api/schema/'
        ),
        name='swagger-ui',
    ),
]