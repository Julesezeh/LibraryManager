import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from book.models import Book, Loan
from user.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", password="pass123", email="test@test.com"
    )


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="admin", password="admin123", is_staff=True
    )


@pytest.fixture
def book():
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        isbn="1234567890123",
        page_count=200,
        available_copies=5,
        total_copies=5,
    )


@pytest.mark.django_db
class TestBookAPI:
    def test_list_books_anonymous(self, api_client, book):
        response = api_client.get("/api/books/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_create_book_anonymous(self, api_client):
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "9876543210123",
            "page_count": 300,
        }
        response = api_client.post("/api/books/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_book_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "9876543210123",
            "page_count": 300,
            "available_copies": 1,
            "total_copies": 1,
        }
        response = api_client.post("/api/books/", data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestLoanAPI:
    def test_borrow_book(self, api_client, user, book):
        api_client.force_authenticate(user=user)
        data = {"book_id": book.id, "duration_days": 14}
        response = api_client.post("/api/books/loans/borrow/", data)
        assert response.status_code == status.HTTP_201_CREATED
        book.refresh_from_db()
        assert book.available_copies == 4

    def test_return_book(self, api_client, user, book):
        api_client.force_authenticate(user=user)
        loan = Loan.objects.create(
            user=user, book=book, due_date=timezone.now() + timedelta(days=14)
        )
        book.available_copies = 4
        book.save()

        response = api_client.post(f"/api/books/loans/{loan.id}/return_book/")
        assert response.status_code == status.HTTP_200_OK
        book.refresh_from_db()
        assert book.available_copies == 5
