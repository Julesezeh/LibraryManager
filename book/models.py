from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.IntegerField(validators=[MinValueValidator(1)])
    publisher = models.CharField(max_length=255, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    available_copies = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    total_copies = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["isbn"]),
            models.Index(fields=["title"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        return self.available_copies > 0


class Loan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loans"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-borrowed_date"]
        indexes = [
            models.Index(fields=["user", "returned_date"]),
            models.Index(fields=["book", "returned_date"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    @property
    def is_overdue(self):
        if self.returned_date:
            return False
        return timezone.now() > self.due_date

    @property
    def is_active(self):
        return self.returned_date is None
