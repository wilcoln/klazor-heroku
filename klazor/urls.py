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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from klazor.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Administration views
    path('admin/', admin.site.urls),

    # Authentication views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pages/welcome.html'), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', welcome, name='welcome'),
    url(r'^register/$', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mooc_courses/<int:id>/', view_mooc_course, name='mooc-course'),
    path('school_courses/<int:id>/', view_school_course, name='school-course'),
    path('mooc_course_element/<int:id>/', view_mooc_course_element, name='mooc-course-item'),
    path('course_part/<int:course_part_id>/reach_item/<int:element_sequence>/', mooc_course_element_reach, name='mooc-course-item-reach'),
    path('school_course_element/<int:id>/', view_school_course_element, name='school-course-item'),
    path('school_course/<int:course_part_id>/reach_item/<int:element_sequence>/', school_course_element_reach, name='school-course-item-reach'),
    path('folder/<int:id>/', view_folder, name='folder'),
    path('folder/editor/<int:id>/sheet/<int:sheet_id>', view_folder_editor, name='folder-editor'),
    path('sheet/<int:id>/', view_sheet, name='sheet'),
    path('sheet/new/', new_sheet, name='new-sheet'),
    path('folder/<int:id>/sheet/new/', new_folder_sheet, name='new-folder-sheet'),
    path('sheet/<int:id>/save/', save_sheet, name='save-sheet'),
    path('sheet/<int:id>/cell/save/', save_cell, name='save-cell'),
    path('sheet/delete/<int:id>/', delete_sheet, name='delete-sheet'),
    path('folder/delete/<int:id>/', delete_folder, name='delete-folder'),
    path('folder/rename/<int:id>/', rename_folder, name='rename-folder'),
    path('folder/new/', new_folder, name='new-folder'),
    path('folder/<int:id>/convert/mooc-course', convert_folder_to_mooc_course, name='folder-to-mooc-course'),
    path('folder/file/add/', add_folder_files, name='add-folder-files'),
    path('folder/file/<int:id>/delete/', remove_folder_file, name='remove-folder-file'),
    path('mooc_course/delete/<int:id>/', delete_mooc_course, name='delete-mooc-course'),
    path('school_course/delete/<int:id>/', delete_school_course, name='delete-school-course'),
    path('upload/', upload, name='upload'),
    path('sheet/<int:id>/print', print_sheet, name='print-sheet'),
    path('item/check/<int:id>/', toggle_course_element_status, name='check-item'),

    # Libr urls
    url(r'^libr', include('libr.urls')),
    # Api urls
    url(r'^api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
