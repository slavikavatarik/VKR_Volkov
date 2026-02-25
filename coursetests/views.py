from django.shortcuts import render, redirect
from courses.models import Client
from courses.models import Attempt, LTheme, QAnswer, Question, Round
from django.db.models import Q
import datetime


def get_courses(request):
    client = Client.objects.filter(user_id=request.user.id)[0]
    if client.studentgroup is None:
        return render(request, 'nogroup.html', {})
    else:
        courses = client.studentgroup.courses.all()
        return render(request, 't_courses.html', {'courses': courses, 'client': client})
 

def show_test_themes(request, c_id):
    themes = LTheme.objects.filter(course_id=c_id).order_by('number')
    return redirect("ttests")
    #return render(request, 'show_test_themes.html', {'themes': themes})


def ttests(request):
    if request.method == "POST":
        t_id = request.POST['theme_id'] 
        return redirect('starttest', th_id=t_id)   
    else:
        themes = LTheme.objects.all()
        client = Client.objects.filter(user_id=request.user.id)[0]
        courses = client.studentgroup.courses.all()
        return render(request, 'ttests.html', {'themes': themes})


def starttest(request, th_id):
    clear_results(request,th_id)
    request.session['generated'] = []
    request.session['current_q'] = None
    request.session['answered'] = 0
    request.session['attempt'] = 0
    request.session['tid'] = th_id
    questions = Question.objects.filter(theme_id=th_id)
    while True:
        random_q = questions.order_by('?').first()        
        if random_q.id in request.session['generated']:
            continue
        else:
            request.session['generated'].append(random_q.id)
            if len(request.session['generated']) == 5:
                break
    request.session['current_q'] = request.session['generated'][0]
    return redirect('show_question')


def clear_results(request,tid):
    attempt = Attempt.objects.filter(Q(theme_id=tid) & Q(user_id=request.user.id))
    if attempt.count() > 0:
        rounds = Round.objects.all()
        for round in rounds:
            if round.attempt.id == attempt[0].id:
                round.delete()
        attempt[0].delete()


def show_question(request):  
    answers = QAnswer.objects.filter(question_id=request.session['current_q'])
    question = Question.objects.get(pk=request.session['current_q'])
    theme = LTheme.objects.get(pk=request.session['tid'])
    if request.method == "POST":
        if request.session['answered'] == 0:
            theme = LTheme.objects.get(pk=request.session['tid'])
            attempt = Attempt(user= request.user, adate = datetime.date.today(), theme = theme)
            attempt.save()
            request.session['attempt'] = attempt.id
        if question.qtype == '1':
            ans_id = request.POST['ans'] 
            attempt_obj = Attempt.objects.get(pk=request.session['attempt'])
            answ = QAnswer.objects.get(pk=ans_id)
            round = Round(attempt=attempt_obj, answer=answ)
            round.save()
            q_amount = int(request.session['answered']) + 1
            if q_amount >= 5:
                return redirect('show_result')
            else:
                request.session['answered'] = q_amount
                request.session['current_q'] = request.session['generated'][q_amount]
                return redirect('show_question')
        else:
            ans_list = request.POST.getlist('anw')              
            attempt_obj = Attempt.objects.get(pk=request.session['attempt'])            
            for answ in ans_list:
                if answ != None:
                    answ_ = QAnswer.objects.get(pk=answ)
                    round = Round(attempt=attempt_obj, answer=answ_)
                    round.save()
            q_amount = int(request.session['answered']) + 1
            if q_amount >= 5:
                return redirect('show_result')
            else:
                request.session['answered'] = q_amount
                request.session['current_q'] = request.session['generated'][q_amount]
                return redirect('show_question')
    return render(request, 'show_question.html', {'q': question, 'answers': answers, 'theme': theme})   


def show_result(request):    
    theme = LTheme.objects.get(pk=request.session['tid']) 
    attempt = Attempt.objects.get(pk=request.session['attempt'])
    rounds = Round.objects.filter(attempt_id=attempt.id)
    err_flag = False
    points = 0
    for qid in request.session['generated']:
        ans = rounds.filter(answer__question_id=qid)        
        for an in ans:
            if not an.answer.status:
                err_flag = True
                break
        if err_flag:
            pass
        else:
            points = points + 1            
        err_flag = False  
    attempt.mark = points
    attempt.save()
    return render(request, 'show_result.html', {'theme': theme, 'points': points})
