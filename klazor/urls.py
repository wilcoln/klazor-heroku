"""Klazor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from klazor.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),
    path('welcome/', welcome),
    path('mooc_courses/<int:id>/', view_mooc_course, name='mooc-course'),
    path('school_courses/<int:id>/', view_school_course, name='school-course'),
    path('mooc_course_item/<int:id>/', view_mooc_course_item, name='mooc-course-item'),
    path('week/<int:week_id>/reach_item/<int:item_sequence>/', mooc_course_item_reach, name='mooc-course-item-reach'),
    path('school_course_item/<int:id>/', view_school_course_item, name='school-course-item'),
    path('school_course/<int:school_course_id>/reach_item/<int:item_sequence>/', school_course_item_reach, name='school-course-item-reach'),
    path('folder/<int:id>/', view_folder, name='folder'),
    path('folder/editor/<int:id>/sheet/<int:sheet_id>', view_folder_editor, name='folder-editor'),
    path('sheet/<int:id>/', view_sheet, name='sheet'),
    path('sheet/new/', new_sheet, name='new-sheet'),
    path('folder/<int:id>/sheet/new/', new_folder_sheet, name='new-folder-sheet'),
    path('sheet/<int:id>/save/', save_sheet, name='save-sheet'),
    path('sheet/<int:id>/content/save/', save_content, name='save-content'),
    path('sheet/delete/<int:id>/', delete_sheet, name='delete-sheet'),
    path('folder/delete/<int:id>/', delete_folder, name='delete-folder'),
    path('folder/new/', new_folder, name='new-folder'),
    path('folder/file/add/', add_folder_file, name='add-folder-file'),
    path('folder/file/<int:id>/delete/', remove_folder_file, name='remove-folder-file'),
    path('mooc_course/delete/<int:id>/', delete_mooc_course, name='delete-mooc-course'),
    path('school_course/delete/<int:id>/', delete_school_course, name='delete-school-course'),
    path('upload/', upload, name='upload'),
    path('item/check/<int:id>/', toggle_course_item_status, name='check-item')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
