from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
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
        quick_access = Sheet.objects.filter(owner_id=request.user.id).order_by('-updated_at')[
                       :6]
        root_folder = Folder.objects.get(pk=1)
        courses = Course.objects.filter(owner_id=request.user.id, folder_id=1)
        folders = Folder.objects.filter(parent_id=1, owner_id=request.user.id)  # We remove the root folder
        # sheets libres # les course elements n'ont pas de dossier parent
        free_sheets = Sheet.objects.filter(folder=1, owner_id=request.user.id)
        file_items = FileItem.objects.filter(folder=1, owner_id=request.user.id)
        return render(request, 'pages/welcome.html', {
            'quick_access': quick_access,
            'folder': root_folder,
            'courses': courses,
            'sub_folders': folders,
            'sheets': free_sheets,
            'file_items': file_items
        })
    return redirect('/login')


def view_shared_with_me(request):
    if request.user.is_authenticated:
        shared_with_me = SharedItem.shared_with(request.user)
        # return HttpResponse(str(shared_with_me[0].type()))
        #courses = [item for item in shared_with_me if item.type() == 'Course']
        #folders = [item for item in shared_with_me if item.type() == 'Folder']
        #folders = Folder.objects.filter(parent_id=1, user_id=request.user.id)  # We remove the root folder
        # sheets libres # les course elements n'ont pas de dossier parent
        sheets = [item for item in shared_with_me if item.type() == 'Sheet']
        file_items = [item for item in shared_with_me if item.type() == 'FileItem']
        return render(request, 'pages/shared_with_me.html', {
            #'courses': courses,
            #'sub_folders': folders,
            'sheets': sheets,
            'file_items': file_items
        })
    return redirect('/login')


def view_course(request, id):
    course = Course.objects.get(pk=id)
    #UserItemLog.save_log(UserItemLog.VIEWED, user=request.user, item=course)
    return render(request, 'pages/course.html', {'course': course})


def view_course_element(request, course_id, part_sequence, element_sequence):
    course = Course.objects.get(pk=course_id)
    #UserItemLog.save_log(UserItemLog.VIEWED, user=request.user, item=course)
    course_part = course.coursepart_set.all()[part_sequence - 1]
    try:
        course_element = course_part.courseelement_set.all()[element_sequence - 1]
        #UserItemLog.save_log(UserItemLog.VIEWED, user=request.user, item=course_element)
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
                  {'folder': folder, 'active_sheet': active_sheet, 'courses': courses, 'sheets': sheets, 'file_items': file_items})


def convert_folder_to_course(request, id):
    folder = Folder.objects.get(pk=id)
    cvt.to_course(folder)  # by default type == ''
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    return render(request, 'pages/sheet.html', {'sheet': sheet})


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
        video_cell.url = cell_dict['url']
        video_cell.save()
    elif cell_type == 'IMAGE':
        image_cell = ImageCell()
        image_cell.sheet = sheet
        image_cell.sequence = cell_dict['sequence']
        image_cell.title = cell_dict['title']
        image_cell.scale = cell_dict['scale']
        image_cell.url = cell_dict['url']
        image_cell.save()
    elif cell_type == 'AUDIO':
        audio_cell = AudioCell()
        audio_cell.sheet = sheet
        audio_cell.sequence = cell_dict['sequence']
        audio_cell.title = cell_dict['title']
        audio_cell.url = cell_dict['url']
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
        youtube_cell.url = cell_dict['url']
        youtube_cell.title = cell_dict['title']
        youtube_cell.scale = cell_dict['scale']
        youtube_cell.save()
    elif cell_type == 'FILE':
        file_cell = FileCell()
        file_cell.sheet = sheet
        file_cell.sequence = cell_dict['sequence']
        file_cell.title = cell_dict['title']
        file_cell.url = cell_dict['url']
        file_cell.save()
    elif cell_type == 'NUMERICAL_INPUT':
        numerical_question_cell = NumericalInputCell()
        numerical_question_cell.sheet = sheet
        numerical_question_cell.sequence = cell_dict['sequence']
        numerical_question_cell.answer = cell_dict['answer']
        numerical_question_cell.save()
    elif cell_type == 'OPEN_ENDED_INPUT':
        open_ended_question_cell = OpenEndedInputCell()
        open_ended_question_cell.sheet = sheet
        open_ended_question_cell.sequence = cell_dict['sequence']
        open_ended_question_cell.answer = cell_dict['answer']
        open_ended_question_cell.save()
    elif cell_type == 'MULTIPLE_CHOICE_INPUT':
        multiple_choice_question_cell = MultipleChoiceInputCell()
        multiple_choice_question_cell.sheet = sheet
        multiple_choice_question_cell.sequence = cell_dict['sequence']
        multiple_choice_question_cell.save()
        propositions = cell_dict['propositions']
        for proposition_dict in propositions:
            proposition = Proposition()
            proposition.input_cell = multiple_choice_question_cell
            proposition.statement = proposition_dict['statement']
            proposition.is_true = proposition_dict['isTrue']
            proposition.save()

    return HttpResponse(str(cell_dict))


def delete_item(request, id):
    item = Item.objects.get(pk=id)
    item.owner_id = User.objects.filter(username='trash').first().id
    item.save()
    try:
        item.delete()
    finally:
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
    folder.owner_id = User.objects.filter(username='trash').first().id
    folder.save()
    try:
        folder.delete()
    finally:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_course(request, folder_id):
    course = Course()
    course.owner = request.user
    course.folder_id = folder_id
    course.title = 'New Course'
    course.save()
    return redirect('/course/edit/' + str(course.id))


def edit_course(request, id):
    course = Course.objects.get(pk=id)
    form = CourseForm()
    return render(request, 'pages/edit_course.html', {'course': course, 'form': form})


def save_course(request, id):
    course = None
    old_course = Course.objects.get(pk=id)
    folder_id = old_course.folder_id
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            course.owner = old_course.owner
            course.folder_id = folder_id
            course.save()
            old_course.delete()
            # TODO : if sucess redirect to course element creation
    return redirect('course', course.id)


def add_course_part(request, course_id):
    course_part = CoursePart()
    course_part.course_id = course_id
    course_part.title = request.POST['part-title']
    course_part.label = request.POST['part-label']
    course_part.sequence = request.POST['part-sequence']
    course_part.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_course_element(request, course_part_id):
    course_element = CourseElement()
    course_element.owner = request.user
    course_element.course_part_id = course_part_id
    course_element.title = request.POST['element-title']
    course_element.sequence = request.POST['element-sequence']
    course_element.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_folder(request):
    folder = Folder()
    folder.owner = request.user
    folder.parent_id = request.POST['parent-id']
    folder.name = request.POST['folder-name']
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_tag(request):
    tag = Tag()
    tag.name = request.POST['tag-name']
    tag.save()
    tag_dict = {'id': tag.id, 'name': tag.name}
    return HttpResponse(json.dumps(tag_dict))


def add_instructor(request):
    instructor = Instructor()
    instructor.name = request.POST['instructor-name']
    instructor.link = request.POST['instructor-link']
    instructor.save()
    instructor_dict = {'id': instructor.id, 'name': instructor.name}
    return HttpResponse(json.dumps(instructor_dict))


def rename_folder(request, id):
    folder = Folder.objects.get(pk=id)
    folder.name = request.POST['folder-name']
    folder.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def move_item(request, id, destination_id):
    item = Item.objects.get(pk=id)
    item.folder_id = destination_id
    item.save()
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
    for file in files:
        file_item = FileItem()
        file_item.folder = folder
        file_item.owner = request.user
        file_item.title = file.name
        file_item.file = file
        file_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_sheet(request, id):
    new_sheet = Sheet()
    new_sheet.title = "Nouveau titre"
    new_sheet.owner = request.user
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
    completed_course_element_log = CompletedCourseElementLog()

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
