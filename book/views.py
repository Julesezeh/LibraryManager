from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer, BorrowBookSerializer
from .permissions import IsAdminOrReadOnly
from .filters import BookFilter, LoanFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = BookFilter
    search_fields = ["title", "author", "isbn", "description"]
    ordering_fields = ["title", "author", "created_at", "available_copies"]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = LoanFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def borrow(self, request):
        serializer = BorrowBookSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            loan = serializer.save()
            return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        loan = self.get_object()

        if loan.returned_date:
            return Response(
                {"error": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not request.user.is_staff and loan.user != request.user:
            return Response(
                {"error": "You can only return your own loans"},
                status=status.HTTP_403_FORBIDDEN,
            )

        loan.returned_date = timezone.now()
        loan.save()

        book = loan.book
        book.available_copies += 1
        book.save()

        return Response(LoanSerializer(loan).data, status=status.HTTP_200_OK)
