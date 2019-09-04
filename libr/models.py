from django.db import models
from klazor.models import FileItem
# Create your models here.


class Publisher(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'publisher'


class Author(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'


class Narrator(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'narrator'


class Document(FileItem):
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'document'


class Book(Document):
    release_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True)
    publisher = models.ForeignKey(Publisher, models.CASCADE)
    author_set = models.ManyToManyField(Author)
    lang_alpha2 = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        db_table = 'book'


class TextBook(Book):
    nb_pages = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'paper_book'


class AudioBook(Book):
    narrator_set = models.ManyToManyField(Author, blank=True)

    class Meta:
        db_table = 'audio_book'


class DocumentFile(Document):
    nb_pages = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'document_file'

