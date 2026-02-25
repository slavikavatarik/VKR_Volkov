from django.shortcuts import render
import json
from courses.models import Client, Course, LTheme, Lection

def home(request):
    return render(request, 'home.html', {})


def courses(request):
    client = Client.objects.filter(user_id=request.user.id)[0]
    if client.studentgroup is None:
        return render(request, 'nogroup.html', {})
    else:
        courses = client.studentgroup.courses.all()
        return render(request, 'courses.html', {'client': client, 'courses': courses})


def show_themes(request, c_id):
    themes = LTheme.objects.filter(course_id=c_id).order_by('number')
    return render(request, 'show_themes.html', {'themes': themes})


def show_lections(request, t_id):
    lecs = Lection.objects.filter(theme_id=t_id).order_by('number')
    theme = LTheme.objects.get(pk=t_id)
    return render(request, 'lections.html', {'theme': theme, 'lecs': lecs})


def open_lection(request, l_id):
    lection = Lection.objects.get(pk=l_id)    
    return render(request, 'open_lection.html', {'lection': lection, 'file_path_json': json.dumps(lection.filename())})