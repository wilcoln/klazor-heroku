from django.urls import path
from libr.views import *

app_name = 'libr'
urlpatterns = [
    path('', index, name='index')
]