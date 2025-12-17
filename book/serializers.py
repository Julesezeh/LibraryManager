from rest_framework import serializers
from .models import Book, Loan
from django.utils import timezone
from datetime import timedelta


class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        if "total_copies" in attrs and "available_copies" in attrs:
            if attrs["available_copies"] > attrs["total_copies"]:
                raise serializers.ValidationError(
                    "Available copies cannot exceed total copies"
                )
        return attrs


class LoanSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)
    is_overdue = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Loan
        fields = "__all__"
        read_only_fields = ("user", "borrowed_date", "returned_date")

    def validate_book(self, value):
        if not value.is_available:
            raise serializers.ValidationError("This book is not available for loan")
        return value


class BorrowBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    duration_days = serializers.IntegerField(default=14, min_value=1, max_value=90)

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
            if not book.is_available:
                raise serializers.ValidationError("This book is not available")
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        book = Book.objects.get(id=validated_data["book_id"])
        due_date = timezone.now() + timedelta(days=validated_data["duration_days"])

        loan = Loan.objects.create(user=user, book=book, due_date=due_date)

        book.available_copies -= 1
        book.save()

        return loan
