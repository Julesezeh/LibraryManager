# Library Management System

A Django REST API for managing library books and loans with JWT authentication.

---

## Features

* User registration and JWT authentication
* Book browsing for anonymous users
* Book borrowing and returning for authenticated users
* Admin panel for managing books and users
* Filtering, searching, and pagination
* API documentation with Swagger and ReDoc
* Unit and integration tests
* Docker support
* PostgreSQL database
* Security features (CSRF, XSS protection, SQL injection prevention)

---

## Prerequisites

* Python 3.12+
* PostgreSQL 15+
* Docker and Docker Compose (optional)
* Git

---

## Installation

### Option 1: Using Docker (Recommended)

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

2. **Create environment file**

```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Build and run with Docker Compose**

```bash
docker-compose up --build
```

4. **Run migrations and create a superuser**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application**

* API: [http://localhost:8000/api/](http://localhost:8000/api/)
* Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

### Option 2: Local Setup

1. **Clone the repository and set up a virtual environment**

```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create PostgreSQL database**

```bash
createdb library_db
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run migrations and start server**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## API Endpoints

### Authentication

* `POST /api/users/register/` – Register a new user
* `POST /api/users/login/` – Login and obtain JWT tokens
* `POST /api/users/token/refresh/` – Refresh access token
* `GET /api/users/profile/` – Retrieve or update user profile

### Books

* `GET /api/books/` – List all books (supports filtering)
* `POST /api/books/` – Create a book (admin only)
* `GET /api/books/{id}/` – Retrieve book details
* `PUT /api/books/{id}/` – Update a book (admin only)
* `DELETE /api/books/{id}/` – Delete a book (admin only)

### Loans

* `GET /api/books/loans/` – List user loans
* `POST /api/books/loans/borrow/` – Borrow a book
* `POST /api/books/loans/{id}/return_book/` – Return a book
* `GET /api/books/loans/{id}/` – Retrieve loan details

---

## API Usage Examples

### Register a User

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

### List Books with Filters

```bash
# Available books by author
curl "http://localhost:8000/api/books/?author=Tolkien&available_only=true"

# Search books
curl "http://localhost:8000/api/books/?search=python"
```

### Borrow a Book

```bash
curl -X POST http://localhost:8000/api/books/loans/borrow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "duration_days": 14
  }'
```

### Return a Book

```bash
curl -X POST http://localhost:8000/api/books/loans/1/return_book/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Filtering and Pagination

### Book Filters

* `?title=<text>` – Filter by title (case-insensitive)
* `?author=<text>` – Filter by author (case-insensitive)
* `?isbn=<isbn>` – Filter by ISBN (exact match)
* `?available_only=true` – Show only available books
* `?search=<text>` – Search title, author, ISBN, and description
* `?ordering=title` – Order results (prefix with `-` for descending)

### Loan Filters

* `?is_active=true` – Show active loans only
* `?is_overdue=true` – Show overdue loans only

### Pagination

```bash
# Default page size is 10
curl "http://localhost:8000/api/books/?page=2"
```

Example response:

```json
{
  "count": 50,
  "next": "http://localhost:8000/api/books/?page=3",
  "previous": "http://localhost:8000/api/books/?page=1",
  "results": []
}
```

---

## Running Tests

### Run all tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=books --cov=users --cov-report=html
open htmlcov/index.html
```

### Run a specific test file

```bash
pytest books/tests/test_models.py
```

### Run tests in Docker

```bash
docker-compose exec web pytest
```