from django.contrib import admin
from libr.models import *
# Register your models here.
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(TextBook)
admin.site.register(AudioBook)
admin.site.register(Document)
admin.site.register(Narrator)