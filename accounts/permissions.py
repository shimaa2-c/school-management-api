from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveAuthenticated(BasePermission):
    message = "Authentication is required and the account must be active."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
        )


class IsAdminRole(BasePermission):
    message = "Only administrators are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == "admin"
        )


class IsTeacherRole(BasePermission):
    message = "Only teachers are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == "teacher"
        )


class IsStudentRole(BasePermission):
    message = "Only students are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == "student"
        )


class IsResponsibleRole(BasePermission):
    message = "Only responsibles are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role == "responsible"
        )


class IsAdminOrReadOnly(BasePermission):
    message = "Only administrators can modify this resource."

    def has_permission(self, request, view):
        if not (
            request.user.is_authenticated
            and request.user.is_active
        ):
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == "admin"


class IsAdminOrTeacher(BasePermission):
    message = "Only administrators or teachers are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.role in ("admin", "teacher")
        )