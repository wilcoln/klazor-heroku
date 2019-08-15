from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.shortcuts import redirect
from klazor.models import *
from klazor.forms import *
from klazor import converters as cvt
import io
import base64
import json


# Organize all these views into CourseView, SheetView, FolderView, CellView, FileView


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def welcome(request):
    if request.user.is_authenticated:
        quick_access = Sheet.objects.filter(folder_id__isnull=False, user_id=request.user.id).order_by('-updated_at')[
                       :6]
        root_folder = Folder.objects.get(pk=1)
        courses = Course.objects.filter(user_id=request.user.id, folder_id=1)
        folders = Folder.objects.filter(parent_id=1, user_id=request.user.id)  # We remove the root folder
        # sheets libres # les course elements n'ont pas de dossier parent
        free_sheets = Sheet.objects.filter(folder=1, user_id=request.user.id)
        file_items = FileItem.objects.filter(folder=1, user_id=request.user.id)
        return render(request, 'pages/welcome.html', {
            'quick_access': quick_access,
            'folder': root_folder,
            'courses': courses,
            'sub_folders': folders,
            'sheets': free_sheets,
            'file_items': file_items
        })
    return redirect('/login')


def view_course(request, id):
    course = Course.objects.get(pk=id)
    return render(request, 'pages/course.html', {'course': course})


def view_course_element(request, course_id, part_sequence, element_sequence):
    course = Course.objects.get(pk=course_id)
    course_part = course.coursepart_set.all()[part_sequence - 1]
    try:
        course_element = course_part.courseelement_set.all()[element_sequence - 1]
        return render(request, 'pages/course_element.html', {'course_element': course_element})
    except IndexError:
        return redirect('/course/' + str(course.id))


def view_folder(request, id):
    if id == 1:
        return redirect('welcome')
    courses = Course.objects.filter(folder=id)
    sheets = Sheet.objects.filter(folder=id)
    file_items = FileItem.objects.filter(folder=id)
    folder = Folder.objects.get(pk=id)
    sub_folders = folder.folder_set.all()
    return render(request, 'pages/folder.html',
                  {'folder': folder, 'sub_folders': sub_folders, 'courses': courses, 'sheets': sheets,
                   'file_items': file_items})


def view_folder_editor(request, id, sheet_id):
    courses = Course.objects.filter(folder=id)
    active_sheet = Sheet.objects.get(pk=sheet_id)
    sheets = Sheet.objects.filter(folder=id)
    folder = Folder.objects.get(pk=id)
    file_items = FileItem.objects.filter(folder=id)
    return render(request, 'pages/folder_editor.html',
                  {'folder': folder, 'active_sheet': active_sheet, 'courses': courses, 'sheets': sheets,
                   'file_items': file_items})


def convert_folder_to_course(request, id):
    folder = Folder.objects.get(pk=id)
    cvt.to_course(folder)  # by default type == ''
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    return render(request, 'pages/sheet.html', {'sheet': sheet, 'edit_mode': False})


def save_cell(request, id):
    data = json.loads(request.body)
    cell_dict = json.loads(data['cell'])  # Contains modified data and is a dictionary
    sheet = Sheet.objects.get(pk=id)  # The saved sheet, and is instance of Sheet

    cell_type = cell_dict['type']
    if cell_type == 'VIDEO':
        video_cell = VideoCell()
        video_cell.sheet = sheet
        video_cell.sequence = cell_dict['sequence']
        video_cell.title = cell_dict['title']
        video_cell.scale = cell_dict['scale']
        video_cell.video = cell_dict['video']
        video_cell.save()
    elif cell_type == 'IMAGE':
        image_cell = ImageCell()
        image_cell.sheet = sheet
        image_cell.sequence = cell_dict['sequence']
        image_cell.title = cell_dict['title']
        image_cell.scale = cell_dict['scale']
        image_cell.image = cell_dict['image']
        image_cell.save()
    elif cell_type == 'AUDIO':
        audio_cell = AudioCell()
        audio_cell.sheet = sheet
        audio_cell.sequence = cell_dict['sequence']
        audio_cell.title = cell_dict['title']
        audio_cell.audio = cell_dict['audio']
        audio_cell.save()
    elif cell_type == 'MARKDOWN':
        markdown_cell = MarkdownCell()
        markdown_cell.sheet = sheet
        markdown_cell.sequence = cell_dict['sequence']
        markdown_cell.text = cell_dict['text']
        markdown_cell.save()
    elif cell_type == 'YOUTUBE':
        youtube_cell = YoutubeCell()
        youtube_cell.sheet = sheet
        youtube_cell.sequence = cell_dict['sequence']
        youtube_cell.youtube = cell_dict['youtube']
        youtube_cell.title = cell_dict['title']
        youtube_cell.scale = cell_dict['scale']
        youtube_cell.save()
    elif cell_type == 'FILE':
        file_cell = FileCell()
        file_cell.sheet = sheet
        file_cell.sequence = cell_dict['sequence']
        file_cell.title = cell_dict['title']
        file_cell.file = cell_dict['file']
        file_cell.save()
    elif cell_type == 'NUMERICAL_QUESTION':
        numerical_question_cell = NumericalQuestionCell()
        numerical_question_cell.sheet = sheet
        numerical_question_cell.sequence = cell_dict['sequence']
        numerical_question_cell.answer = cell_dict['answer']
        numerical_question_cell.save()
    elif cell_type == 'OPEN_ENDED_QUESTION':
        open_ended_question_cell = OpenEndedQuestionCell()
        open_ended_question_cell.sheet = sheet
        open_ended_question_cell.sequence = cell_dict['sequence']
        open_ended_question_cell.answer = cell_dict['answer']
        open_ended_question_cell.save()
    elif cell_type == 'MULTIPLE_CHOICE_QUESTION':
        multiple_choice_question_cell = MultipleChoiceQuestionCell()
        multiple_choice_question_cell.sheet = sheet
        multiple_choice_question_cell.sequence = cell_dict['sequence']
        multiple_choice_question_cell.save()
        propositions = cell_dict['propositions']
        for proposition_dict in propositions:
            proposition = Proposition()
            proposition.question_cell = multiple_choice_question_cell
            proposition.statement = proposition_dict['statement']
            proposition.is_true = proposition_dict['isTrue']
            proposition.save()

    return HttpResponse(str(cell_dict))


def delete_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    sheet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def save_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    sheet.title = request.POST['title']
    # retrieve all old cells
    old_cells = sheet.cell_set.all()
    # Delete all old cells
    for old_cell in old_cells:
        old_cell.delete()
    sheet.save()
    return HttpResponse("success")


def delete_folder(request, id):
    folder = Folder.objects.get(pk=id)
    folder.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_course(request, folder_id):
    course = Course()
    course.user = request.user
    course.folder_id = folder_id
    course.title = 'New Course'
    course.save()

    form = CourseForm()

    return render(request, 'pages/edit_course.html', {'course': course, 'form': form})


def delete_course(request, id):
    course = Course.objects.get(pk=id)
    course.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def new_folder(request):
    folder = Folder()
    folder.user = request.user
    folder.parent_id = request.POST['parent-id']
    folder.name = request.POST['folder-name']
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def rename_folder(request, id):
    folder = Folder.objects.get(pk=id)
    folder.name = request.POST['folder-name']
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def move_sheet(request, id, destination_id):
    sheet = Sheet.objects.get(pk=id)
    sheet.folder_id = destination_id
    sheet.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def move_folder(request, id, destination_id):
    folder = Folder.objects.get(pk=id)
    folder.parent_id = destination_id
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_folder_files(request):
    folder_id = request.POST['folder-id']
    folder = Folder.objects.get(pk=folder_id)
    files = request.FILES.getlist('files')
    user = request.user
    for file in files:
        file_item = FileItem()
        file_item.folder = folder
        file_item.user = user
        file_item.title = file.name
        file_item.file = file
        file_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_folder_file(request, id):
    file_item = FileItem.objects.filter(pk=id)
    file_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_sheet(request, id):
    new_sheet = Sheet()
    new_sheet.title = "Nouveau titre"
    new_sheet.user = request.user
    folder = Folder.objects.get(pk=id)
    new_sheet.folder = folder
    new_sheet.save()
    if id == 1:
        return redirect('sheet', new_sheet.id)
    else:
        return redirect('folder-editor', folder.id, new_sheet.id)


def upload(request):
    data = request.POST['file']
    filename = request.POST['filename']
    if ';base64,' in data:
        filename = request.POST['title'].lower().replace(' ', '_')
        format, file_str = data.split(';base64,')
        ext = format.split('/')[-1]
        storage = FileSystemStorage()
        filename = filename + '.' + ext
        path = ''
        if 'image' in format:
            path = 'images/' + filename
        elif 'audio' in format:
            path = 'audios/' + filename
        elif 'video' in format:
            path = 'videos/' + filename

        if not storage.exists(path):
            storage.save(path, ContentFile(base64.b64decode(file_str)))
    return HttpResponse(filename)


def toggle_course_element_status(request, id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # TODO Implement this
    # item = CourseElement.objects.get(pk=id)
    # item.completed = not item.completed
    # item.save()
    # return redirect(request.META.get('HTTP_REFERER'))


# Test pdf generation
def print_sheet(request, id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileItemResponse sets the Cell-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
