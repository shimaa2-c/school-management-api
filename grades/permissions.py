from rest_framework.permissions import BasePermission, SAFE_METHODS


class GradePermission(BasePermission):
    message = "You do not have permission to access this grade."

    def has_permission(self, request, view):
        user = request.user

        if not (user.is_authenticated and user.is_active):
            return False

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return request.method in ["GET", "POST", "PUT", "PATCH"]

        if user.role == "student":
            return request.method in SAFE_METHODS

        if user.role == "responsible":
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "admin":
            return True

        if user.role == "student":
            return (
                request.method in SAFE_METHODS
                and obj.student.user_id == user.id
            )

        if user.role == "responsible":
            return (
                request.method in SAFE_METHODS
                and obj.student.responsible_links.filter(
                    responsible__user_id=user.id
                ).exists()
            )

        if user.role == "teacher":
            return obj.school_class.subject_assignments.filter(
                teacher__user_id=user.id,
                subject_id=obj.subject_id,
            ).exists()

        return False