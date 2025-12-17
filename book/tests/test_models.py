import pytest
from django.utils import timezone
from datetime import timedelta
from book.models import Book, Loan
from user.models import User


@pytest.mark.django_db
class TestBookModel:
    def test_create_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            total_copies=5,
            available_copies=5,
        )
        assert book.title == "Test Book"
        assert book.is_available is True

    def test_book_availability(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            total_copies=1,
            available_copies=0,
        )
        assert book.is_available is False


@pytest.mark.django_db
class TestLoanModel:
    def test_create_loan(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            available_copies=1,
        )
        loan = Loan.objects.create(
            user=user, book=book, due_date=timezone.now() + timedelta(days=14)
        )
        assert loan.is_active is True
        assert loan.is_overdue is False

    def test_overdue_loan(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
        )
        loan = Loan.objects.create(
            user=user, book=book, due_date=timezone.now() - timedelta(days=1)
        )
        assert loan.is_overdue is True
