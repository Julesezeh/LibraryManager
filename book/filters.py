import django_filters
from .models import Book, Loan


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(lookup_expr="icontains")
    isbn = django_filters.CharFilter(lookup_expr="exact")
    available_only = django_filters.BooleanFilter(method="filter_available")

    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "available_only"]

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset


class LoanFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(method="filter_active")
    is_overdue = django_filters.BooleanFilter(method="filter_overdue")

    class Meta:
        model = Loan
        fields = ["user", "book", "is_active", "is_overdue"]

    def filter_active(self, queryset, name, value):
        if value:
            return queryset.filter(returned_date__isnull=True)
        return queryset.filter(returned_date__isnull=False)

    def filter_overdue(self, queryset, name, value):
        from django.utils import timezone

        if value:
            return queryset.filter(
                returned_date__isnull=True, due_date__lt=timezone.now()
            )
        return queryset
