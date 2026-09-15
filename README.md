# School Management REST API

A secure School Management REST API built with Django and Django REST Framework.

The API manages users, teachers, students, responsibles/guardians, classes,
subjects, teacher assignments, and grades.

---

## Technologies

- Python
- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT
- django-cors-headers
- django-filter
- drf-spectacular
- python-dotenv

---

## Features

- JWT authentication with access and refresh tokens
- Refresh-token blacklist for logout
- Current authenticated user endpoint
- Password change
- Role-based permissions
- Object-level and queryset-level access control
- Admin, Teacher, Student, and Responsible roles
- Student/responsible relationships
- Classes and subjects
- Teacher/class/subject assignments
- Grade creation and validation
- Grade score validation from 0 to 100
- Duplicate grade prevention
- Filtering, search, ordering, and pagination
- Request ID middleware
- Request duration logging
- CORS configuration
- Consistent success/error responses
- Swagger/OpenAPI documentation
- Automated API tests

---

## Project Structure

```text
School_management/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests/
│
├── school/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests/
│
├── grades/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── tests/
│
├── core/
│   ├── middleware.py
│   ├── responses.py
│   ├── exceptions.py
│   └── tests/
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
