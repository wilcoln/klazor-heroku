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
    path('course/<int:id>/', view_course, name='course'),
    path('course/<int:course_id>/part/<int:part_sequence>/element/<int:element_sequence>/',
         view_course_element, name='course-element'),
    path('folder/<int:id>/', view_folder, name='folder'),
    path('folder/editor/<int:id>/sheet/<int:sheet_id>', view_folder_editor, name='folder-editor'),
    path('sheet/<int:id>/', view_sheet, name='sheet'),
    path('folder/<int:id>/sheet/new/', add_sheet, name='add-sheet'),
    path('sheet/<int:id>/save/', save_sheet, name='save-sheet'),
    path('sheet/<int:id>/cell/save/', save_cell, name='save-cell'),
    path('sheet/move/<int:id>/into/<int:destination_id>', move_sheet, name='move-sheet'),
    path('sheet/delete/<int:id>/', delete_sheet, name='delete-sheet'),
    path('folder/delete/<int:id>/', delete_folder, name='delete-folder'),
    path('folder/move/<int:id>/into/<int:destination_id>', move_folder, name='move-folder'),
    path('folder/rename/<int:id>/', rename_folder, name='rename-folder'),
    path('folder/new/', new_folder, name='new-folder'),
    path('folder/<int:id>/convert/course', convert_folder_to_course, name='folder-to-course'),
    path('folder/file/add/', add_folder_files, name='add-folder-files'),
    path('folder/file/<int:id>/delete/', remove_folder_file, name='remove-folder-file'),
    path('course/add/into/<int:folder_id>/', add_course, name='add-course'),
    path('course/delete/<int:id>/', delete_course, name='delete-course'),
    path('upload/', upload, name='upload'),
    path('sheet/<int:id>/print', print_sheet, name='print-sheet'),
    path('course-element/check/<int:id>/', toggle_course_element_status, name='check-course-element'),

    # Libr urls
    url(r'^libr/', include('libr.urls')),
    # Api urls
    url(r'^api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
