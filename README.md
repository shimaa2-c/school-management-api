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

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd School_management
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in real values:

```bash
cp .env.example .env
```

Required variables:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True`/`False` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins |

By default the project is configured for PostgreSQL. To run against SQLite
instead (also accepted for this task), point `DATABASES["default"]["ENGINE"]`
in `config/settings.py` to `django.db.backends.sqlite3` and drop the
user/password/host/port keys.

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

The default `AbstractUser`-based createsuperuser flow creates a user with
`role="student"` by default — update the role to `admin` afterwards, e.g.
via Django admin (`/admin/`) or:

```bash
python manage.py shell -c "
from accounts.models import User
u = User.objects.get(username='<your-superuser-username>')
u.role = 'admin'
u.save()
"
```

### 6. Run the development server

```bash
python manage.py runserver
```

### 7. Run the test suite

```bash
python manage.py test
```

45 automated tests cover JWT auth, role/object-level permissions, grade
validation, list features (filter/search/order/pagination), and the request
ID middleware.

### Main API URLs

| URL | Purpose |
|---|---|
| `POST /api/auth/register/` | Register a new (student-role) user |
| `POST /api/auth/token/` | Obtain JWT access + refresh tokens |
| `POST /api/auth/token/refresh/` | Refresh an access token |
| `POST /api/auth/logout/` | Blacklist a refresh token |
| `GET /api/auth/me/` | Current authenticated user |
| `POST /api/auth/change-password/` | Change password |
| `/api/users/` | Admin-only user management |
| `/api/students/`, `/api/teachers/`, `/api/responsibles/` | Profile CRUD, scoped by role |
| `/api/classes/`, `/api/subjects/`, `/api/class-subjects/` | Class/subject/assignment CRUD |
| `/api/grades/` | Grade CRUD, scoped by role |
| `/api/students/{id}/report-card/` | Read-only report card (`APIView`) |
| `/api/schema/`, `/api/docs/` | OpenAPI schema and Swagger UI |

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