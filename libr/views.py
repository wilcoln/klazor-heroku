from django.shortcuts import render
from libr.models import Book
from klazor.models import Tag
# Create your views here.


def index(request):
    books = Book.objects.all()
    tags = Tag.objects.all()
    return render(request, 'pages/index_libr.html', {'books': books, 'tags': tags})
