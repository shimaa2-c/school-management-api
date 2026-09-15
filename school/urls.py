from django.urls import path

from .views import StudentReportCardView


urlpatterns = [
    path(
        'students/<int:pk>/report-card/',
        StudentReportCardView.as_view(),
        name='student-report-card',
    ),
]