from django import template


register = template.Library()


@register.filter
def iconify(filename):
    ext = filename.split('.')[-1]
    if ext in ['txt']:
        return 'fa-file-text-o'
    elif ext in ['png', 'jpeg', 'jpg', 'gif']:
        return 'fa-file-image-o'
    elif ext in ['pdf']:
        return 'fa-file-pdf-o'
    elif ext in ['mp4', 'mkv', 'avi']:
        return 'fa-file-movie-o'
    elif ext in ['mp3', 'ogg', 'webm']:
        return 'fa-file-movie-o'
    else:
        return 'fa-file-o'
