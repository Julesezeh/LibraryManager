from django.contrib import admin
from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "isbn",
        "available_copies",
        "total_copies",
        "is_available",
    )
    list_filter = ("created_at", "publication_date")
    search_fields = ("title", "author", "isbn")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "book",
        "borrowed_date",
        "due_date",
        "returned_date",
        "is_overdue",
    )
    list_filter = ("borrowed_date", "due_date", "returned_date")
    search_fields = ("user__username", "book__title")
    readonly_fields = ("borrowed_date",)
