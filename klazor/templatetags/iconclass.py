from django import template


register = template.Library()


@register.filter
def iconclass(filename):
    ext = filename.split('.')[-1]
    if ext in ['txt', 'tex']:
        return 'fa-file-text-o'
    elif ext in ['png', 'jpeg', 'jpg', 'gif']:
        return 'fa-file-image-o'
    elif ext in ['pdf']:
        return 'fa-file-pdf-o'
    elif ext in ['odt', 'doc', 'docx', 'rtf', 'wks', 'wps', 'wpd']:
        return 'fa-file-word-o'
    elif ext in ['ppt', 'pptx', 'pps', 'odp', 'key']:
        return 'fa-file-powerpoint-o'
    elif ext in ['xls', 'xlsx', 'csv', 'xlr', 'ods']:
        return 'fa-file-excel-o'
    elif ext in ['htm', 'html', 'xhtml', 'xml']:
        return 'fa-file-code-o'
    elif ext in ['7z', 'arj', 'rar', 'deb', 'pkg', 'rpm', 'tar.gz', 'z', 'zip']:
        return 'fa-file-archive-o'
    elif ext in ['mp4', 'mkv', 'avi', 'mov', 'flv', '3gp', 'wmv', 'vob', 'swf', 'mpg', 'mpeg', '3g2']:
        return 'fa-file-movie-o'
    elif ext in ['mp3', 'ogg', 'webm', 'aif', 'cda', 'mpa', 'wav', 'wma', 'wpl']:
        return 'fa-file-movie-o'
    else:
        return 'fa-file-o'
