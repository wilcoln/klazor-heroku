from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from klazor.models import *
import base64
import json


def welcome(request):
    return view_folder(request,1)
    # mooc_courses = MoocCourse.objects.all()
    # school_courses = SchoolCourse.objects.all()
    # folders = Folder.objects.filter(parent_id=1, id__gt=1)  # We remove the root folder
    # folder_free_sheets = Sheet.objects.filter(folder=1) # sheets libre de tout dossier
    # free_sheets = [sheet for sheet in folder_free_sheets if
    #                not hasattr(sheet, 'item')]  # sheets libre de tout dossier ET non Item
    # return render(request, 'pages/welcome.html', {
    #     'mooc_courses': mooc_courses,
    #     'school_courses': school_courses,
    #     'folders': folders,
    #     'free_sheets': free_sheets,
    # })


def view_mooc_course(request, id):
    mooc_course = MoocCourse.objects.get(pk=id)
    return render(request, 'pages/mooc_course.html', {'mooc_course': mooc_course})


def view_school_course(request, id):
    school_course = SchoolCourse.objects.get(pk=id)
    return render(request, 'pages/school_course.html', {'school_course': school_course})


def view_mooc_course_item(request, id):
    mooc_course_item = CourseItem.objects.get(pk=id)
    return render(request, 'pages/mooc_course_item.html', {'mooc_course_item': mooc_course_item})


# Manages mooc course item nav
def mooc_course_item_reach(request, week_id, item_sequence):
    week = Week.objects.get(pk=week_id)
    try:
        mooc_course_item = week.item_set.all()[item_sequence-1]
        return render(request, 'pages/mooc_course_item.html', {'mooc_course_item': mooc_course_item})
    except IndexError:
        return render(request, 'pages/mooc_course.html', {'mooc_course':  week.mooc_course})


def view_school_course_item(request, id):
    school_course_item = CourseItem.objects.get(pk=id)
    return render(request, 'pages/school_course_item.html', {'school_course_item': school_course_item})


# Manages school course item nav
def school_course_item_reach(request, school_course_id, item_sequence):
    school_course = SchoolCourse.objects.get(pk=school_course_id)
    try:
        school_course_item = school_course.item_set.all()[item_sequence-1]
        return render(request, 'pages/school_course_item.html', {'school_course_item': school_course_item})
    except IndexError:
        return render(request, 'pages/school_course.html', {'school_course': school_course})


def view_folder(request, id):
    sheets = Sheet.objects.filter(folder=id)
    file_items = FileItem.objects.filter(folder=id)
    folder = Folder.objects.get(pk=id)
    return render(request, 'pages/folder.html', {'folder': folder, 'sheets': sheets, 'file_items': file_items})


def view_folder_editor(request, id, sheet_id):
    active_sheet = Sheet.objects.get(pk=sheet_id)
    sheets = Sheet.objects.filter(folder=id)
    folder = Folder.objects.get(pk=id)
    file_items = FileItem.objects.filter(folder=id)
    return render(request, 'pages/folder_editor.html', {'folder': folder, 'active_sheet': active_sheet, 'sheets': sheets, 'file_items': file_items})


def view_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    return render(request, 'pages/sheet.html', {'sheet': sheet, 'edit_mode': False})


def new_sheet(request):
    new_sheet = Sheet()
    new_sheet.title = "Nouveau titre"
    new_sheet.save()
    return redirect('sheet', new_sheet.id)


def save_content(request, id):
    data = json.loads(request.body)
    content_dict = json.loads(data['content'])  # Contains modified data and is a dictionary
    sheet = Sheet.objects.get(pk=id)  # The saved sheet, and is instance of Sheet

    storage = FileSystemStorage()
    if 'video' in content_dict:
        filename = str(content_dict['filename'])
        video_content = VideoContent()
        video_content.sheet = sheet
        video_content.sequence = content_dict['sequence']
        video_content.title = content_dict['title']
        video_content.scale = content_dict['scale']
        video_content.video.save(filename, storage.open('videos/'+filename))
        video_content.save()
        storage.delete('videos/' + filename)
    elif 'image' in content_dict:
        filename = str(content_dict['filename'])
        image_content = ImageContent()
        image_content.sheet = sheet
        image_content.sequence = content_dict['sequence']
        image_content.title = content_dict['title']
        image_content.scale = content_dict['scale']
        image_content.image.save(filename, storage.open('images/'+filename))
        image_content.save()
        storage.delete('images/' + filename)
    elif 'audio' in content_dict:
        filename = str(content_dict['filename'])
        audio_content = AudioContent()
        audio_content.sheet = sheet
        audio_content.sequence = content_dict['sequence']
        audio_content.title = content_dict['title']
        audio_content.audio.save(filename, storage.open('audios/'+filename))
        audio_content.save()
        storage.delete('audios/' + filename)
    elif 'text' in content_dict:
        markdown_content = MarkdownContent()
        markdown_content.sheet = sheet
        markdown_content.sequence = content_dict['sequence']
        markdown_content.text = content_dict['text']
        markdown_content.save()

    return HttpResponse(str(content_dict))


def delete_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    sheet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def save_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    sheet.title = request.POST['title']
    # retrieve all old contents
    old_contents = sheet.content_set.all()
    # Delete all old contents
    for old_content in old_contents:
        old_content.delete()
    sheet.save()
    return HttpResponse("success")


def delete_folder(request, id):
    folder = Folder.objects.get(pk=id)
    folder.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_mooc_course(request, id):
    mooc_course = MoocCourse.objects.get(pk=id)
    mooc_course.delete()
    return redirect('welcome')


def delete_school_course(request, id):
    school_course = SchoolCourse.objects.get(pk=id)
    school_course.delete()
    return redirect('welcome')


def new_folder(request):
    folder = Folder()
    folder.parent_id = request.POST['parent-id']
    folder.name = request.POST['folder-name']
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_folder_file(request):
    file_item = FileItem()
    folder_id = request.POST['folder-id']
    folder = Folder.objects.get(pk=folder_id)
    file_item.folder = folder
    file_item.file = request.FILES['file']
    file_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_folder_file(request, id):
    file_item = FileItem.objects.filter(pk=id)
    file_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def new_folder_sheet(request, id):
    new_sheet = Sheet()
    new_sheet.title = "Nouveau titre"
    new_sheet.save()
    folder = Folder.objects.get(pk=id)
    new_sheet.folder = folder
    new_sheet.save()
    return redirect('folder-editor', folder.id, new_sheet.id)


def upload(request):
    data = request.POST['file']
    if ';base64,' in data:
        filename = request.POST['title'].lower().replace(' ', '_')
        format, file_str = data.split(';base64,')
        ext = format.split('/')[-1]
        storage = FileSystemStorage()
        path = ''
        filename = filename + '.' + ext
        if 'image' in format:
            path = 'images/' + filename
        elif 'audio' in format:
            path = 'audios/' + filename
        elif 'video' in format:
            path = 'videos/' + filename
        if not storage.exists(path):
            storage.save(path, ContentFile(base64.b64decode(file_str)))
        return HttpResponse(filename)
    return HttpResponse('no_new_name')


def toggle_course_item_status(request, id):
    item = CourseItem.objects.get(pk=id)
    item.completed = not item.completed
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))

