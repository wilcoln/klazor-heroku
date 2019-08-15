from klazor.models import *
import copy


def to_audio_playlist(obj):
    pass


def to_video_playlist(obj):
    pass


def to_playlist(obj, type='audio'):
    if type == 'audio':
        return to_audio_playlist(obj)
    elif type == 'video':
        return to_video_playlist(obj)


def to_folder(obj):
    pass


def to_course(obj):
    if isinstance(obj, Folder):
        return folder_to_course(obj)


def folder_to_course(folder):
    course = Course()
    course.folder = folder.parent
    course.user = folder.user
    course.title = folder.name
    course.save()
    for i, subfolder in enumerate(folder.folder_set.all()):
        course_part = CoursePart()
        course_part.sequence = i+1
        course_part.level = 1
        course_part.label, course_part.sequence, course_part.title = subfolder.name.split(':')
        course_part.course = course
        course_part.save()
        for j, sheet in enumerate(subfolder.item_set.all()):
            course_element = CourseElement()
            course_element.sequence = j+1
            course_element.user = sheet.user
            course_element.course_part = course_part
            course_element.title = sheet.title
            course_element.save()
            for cell in sheet.cell_set.all():
                cell.sheet = course_element
                cell.pk = None
                cell.save()
    return course
