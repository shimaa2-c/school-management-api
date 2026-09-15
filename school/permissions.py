from rest_framework.permissions import BasePermission, SAFE_METHODS

class StudentProfilePermission(BasePermission):
    """
    Admin:
        Full access.

    Teacher:
        Can read students in classes where the teacher
        is assigned to at least one subject.

    Student:
        Can read/update only their own profile.

    Responsible:
        Can read only linked students.
    """
    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        return (
            user.role in (
                'teacher',
                'student',
                'responsible',
            )
            and request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if request.method not in SAFE_METHODS:
            return False

        if user.role == 'student':
            return obj.user_id == user.id

        if user.role == 'responsible':
            return obj.responsible_links.filter(
                responsible__user_id=user.id
            ).exists()

        if user.role == 'teacher':
            return obj.school_class.subject_assignments.filter(
                teacher__user_id=user.id
            ).exists()

        return False

class TeacherProfilePermission(BasePermission):
    """
    Admin:
        Full access.

    Teacher:
        Read only their own profile.

    Others:
        No access.
    """

    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        if user.role == 'teacher':
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if user.role == 'teacher':
            return (
                request.method in SAFE_METHODS
                and obj.user_id == user.id
            )

        return False


class ResponsibleProfilePermission(BasePermission):
    """
    Admin:
        Full access.

    Responsible:
        Read/update only their own profile.
    """

    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        if user.role == 'responsible':
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if user.role == 'responsible':
            return (
                request.method in SAFE_METHODS
                and obj.user_id == user.id
            )

        return False


class SchoolClassPermission(BasePermission):
    """
    Admin:
        Full CRUD.

    Teacher:
        Read classes assigned to them.

    Student:
        Read their own class.

    Responsible:
        Read classes containing their linked students.
    """
    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        return (
            user.role in (
                'teacher',
                'student',
                'responsible',
            )
            and request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if request.method not in SAFE_METHODS:
            return False

        if user.role == 'teacher':
            return obj.subject_assignments.filter(
                teacher__user_id=user.id
            ).exists()

        if user.role == 'student':
            return (
                hasattr(user, 'student_profile')
                and obj.id == user.student_profile.school_class_id
            )

        if user.role == 'responsible':
            return obj.students.filter(
                responsible_links__responsible__user_id=user.id
            ).exists()

        return False




class SubjectPermission(BasePermission):
    """
    Admin:
        Full CRUD.

    Teacher:
        Read only subjects assigned to them.

    Student:
        Read subjects assigned to their class.

    Responsible:
        Read subjects belonging to linked students' classes.
    """
    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        return (
            user.role in (
                'teacher',
                'student',
                'responsible',
            )
            and request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if request.method not in SAFE_METHODS:
            return False

        if user.role == 'teacher':
            return obj.class_assignments.filter(
                teacher__user_id=user.id
            ).exists()

        if user.role == 'student':
            return obj.class_assignments.filter(
                school_class_id=user.student_profile.school_class_id
            ).exists()

        if user.role == 'responsible':
            return obj.class_assignments.filter(
                school_class__students__responsible_links__responsible__user_id=user.id
            ).exists()

        return False



class StudentResponsiblePermission(BasePermission):
    """
    Admin:
        Full access.

    Responsible:
        Read their own links.

    Student:
        Read links concerning themselves.

    Others:
        No access.
    """
    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        return (
            user.role in ('student', 'responsible')
            and request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if request.method not in SAFE_METHODS:
            return False

        if user.role == 'student':
            return obj.student.user_id == user.id

        if user.role == 'responsible':
            return obj.responsible.user_id == user.id

        return False


class ClassSubjectAssignmentPermission(BasePermission):
    """
    Admin:
        Full CRUD.

    Teacher:
        Read assignments involving themselves.

    Student:
        Read assignments for their class.

    Responsible:
        Read assignments for linked students' classes.
    """
    def has_permission(self, request, view):
        user = request.user

        if not (
            user.is_authenticated
            and user.is_active
        ):
            return False

        if user.role == 'admin':
            return True

        return (
            user.role in (
                'teacher',
                'student',
                'responsible',
            )
            and request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if request.method not in SAFE_METHODS:
            return False

        if user.role == 'teacher':
            return obj.teacher.user_id == user.id

        if user.role == 'student':
            return (
                obj.school_class_id
                == user.student_profile.school_class_id
            )

        if user.role == 'responsible':
            return obj.school_class.students.filter(
                responsible_links__responsible__user_id=user.id
            ).exists()

        return False