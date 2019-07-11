from django.shortcuts import render
from libr.models import Book
# Create your views here.


def index(request):
    books = Book.objects.all()
    return render(request, 'pages/libr.html', {
        'books': books
    })