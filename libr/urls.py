from django.urls import path
from libr.views import *

urlpatterns = [
    path('', index, name='libr')
]