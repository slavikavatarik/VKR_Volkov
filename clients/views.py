from django.shortcuts import render, redirect
from django.db.models import Avg
from courses.models import Attempt, ClMessage, Client, LTheme, Project, ProjectTask, ProjectTaskStatus, ProjectTeam, Question, ReportThemeRow, Round, RoundRow, StudentGroup
from django.db.models import Q
from django.contrib import messages
import datetime

def profile(request): 
    if request.user is not None:
        user = request.user
        client = Client.objects.filter(user_id=request.user.id)[0]
        attempts = Attempt.objects.filter(user_id=user.id).order_by('-adate')
        if request.method == "POST":
            ln = request.POST["lname"]
            n = request.POST["name"]
            ph = request.POST["phone"]
            client.lname = ln
            client.name = n
            client.phone = ph                
            if request.FILES.get('myimg', False): 
                client.img = request.FILES['myimg'] 
            client.save()             
            messages.success(request, ("Данные изменены."))             
            return render(request, 'profile.html', {'client': client, 'attempts': attempts})
        else:
            return render(request, 'profile.html', {'client': client, 'attempts': attempts})
    else:
        redirect('login')    


def show_info(request, a_id):
    attempt = Attempt.objects.get(pk=a_id)
    rounds = Round.objects.filter(attempt_id=attempt.id)
    qid_list = []
    rows = []
    for round in rounds:
        qid_list.append(round.answer.question.id)
    u_qid_list = list(set(qid_list))
    for qid in u_qid_list:
        question = Question.objects.get(pk=qid)
        ans = []
        for round in rounds:
            if round.answer.question.id == qid:
                ans.append(round.answer)
        rr = RoundRow(question, ans)
        rows.append(rr)
    return render(request, 'show_info.html', {'rows': rows, 'attempt': attempt})
        

def reports(request):
    themes = LTheme.objects.all()
    avg_mark = 0
    err_amount = 0
    r_amount = 0
    results = []
    st_date = None
    ed_date = None
    if request.method == "POST":
        sd = request.POST['startdate']
        ed = request.POST['enddate']         
        st_date = datetime.datetime.strptime(sd, "%Y-%m-%d").date()
        ed_date = datetime.datetime.strptime(ed, "%Y-%m-%d").date()   


        for theme in themes:
            avg_mark = Attempt.objects.filter(Q(theme_id=theme.id) & Q(adate__gte=st_date) & Q(adate__lte=ed_date)).aggregate(am = Avg('mark'))
            err_amount = Round.objects.filter(Q(answer__question__theme_id = theme.id) & Q(answer__status = False) & Q(attempt__adate__gte=st_date) & Q(attempt__adate__lte=ed_date)).count()
            r_amount = Round.objects.filter(Q(answer__question__theme_id = theme.id) & Q(answer__status = True) & Q(attempt__adate__gte=st_date) & Q(attempt__adate__lte=ed_date)).count()
            result = ReportThemeRow(theme=theme, avg_mark=avg_mark, err_amount=err_amount, r_amount=r_amount)
            results.append(result)
    else:
        for theme in themes:
            avg_mark = Attempt.objects.filter(theme_id=theme.id).aggregate(am = Avg('mark'))
            err_amount = Round.objects.filter(Q(answer__question__theme_id = theme.id) & Q(answer__status = False)).count()
            r_amount = Round.objects.filter(Q(answer__question__theme_id = theme.id) & Q(answer__status = True)).count()
            result = ReportThemeRow(theme=theme, avg_mark=avg_mark, err_amount=err_amount, r_amount=r_amount)
            results.append(result)
    return render(request, 'report.html', {'results': results, 'sd': st_date, 'end': ed_date}) 


def my_projects(request):
     client = Client.objects.filter(user_id=request.user.id)[0] 
     if request.user.groups.filter(name='employees').exists():
         project_teams = ProjectTeam.objects.filter(Q(member_id=client.id) & Q(role__title='Руководитель')).order_by('project__startdate')
         return render (request, 'projects.html', {'project_teams': project_teams})
     else:
         project_teams = ProjectTeam.objects.filter(member_id=client.id).order_by('project__startdate')
         return render(request, 'my_projects.html', {'project_teams': project_teams})

 
def about(request): 
    return render(request, 'about.html', {})

def show_user_tasks(request, p_id):
    client = Client.objects.filter(user_id=request.user.id)[0] 
    project = Project.objects.get(pk=p_id)
    p_tasks = ProjectTask.objects.filter(Q(project_id=p_id) & Q(worker_id=client.id))       
    return render(request, 'user_tasks_list.html', {'p_tasks': p_tasks, 'project': project})


def show_project_tasks(request, p_id):
    project = Project.objects.get(pk=p_id)
    p_tasks = ProjectTask.objects.filter(project_id=p_id)        
    return render(request, 'tasks_list.html', {'p_tasks': p_tasks, 'project': project})


def add_user_task(request, p_id):
    project = Project.objects.get(pk=p_id)
    if request.method == "POST":
        ttext = request.POST['ttext'] 
        wid = request.POST['wid'] 
        sd = request.POST['sd'] 
        ed = request.POST['ed']
        worker = Client.objects.get(pk=wid) 
        creator = Client.objects.filter(user_id=request.user.id)[0] 
        sdate = datetime.datetime.strptime(sd, "%Y-%m-%d").date()
        edate = datetime.datetime.strptime(ed, "%Y-%m-%d").date()
        status = ProjectTaskStatus.objects.filter(title='Создана')[0]
        project_task = ProjectTask(creator=creator, worker=worker, tasktext=ttext, status=status, startdate=sdate, enddate=edate, project=project)
        project_task.save()
        messages.success(request, ("Задача добавлена."))
        return redirect('show_project_tasks', p_id=project.id)
    else: 
        workers = ProjectTeam.objects.filter(project_id=p_id)        
        return render(request, 'add_task.html', {'project': project, 'workers': workers})
    

def edit_user_task(request, t_id, p_id):
    task = ProjectTask.objects.get(pk=t_id)
    project = Project.objects.get(pk=p_id)
    if request.method == "POST":
        ttext = request.POST['ttext'] 
        wid = request.POST['wid'] 
        sid = request.POST['sid']
        sd = request.POST['sd'] 
        ed = request.POST['ed']
        worker = Client.objects.get(pk=wid) 
        #creator = Client.objects.filter(user_id=request.user.id)[0] 
        status = ProjectTaskStatus.objects.get(pk=sid)
        sdate = datetime.datetime.strptime(sd, "%Y-%m-%d").date()
        edate = datetime.datetime.strptime(ed, "%Y-%m-%d").date()        
        task.worker=worker
        task.tasktext=ttext
        task.status=status
        task.startdate=sdate
        task.enddate=edate        
        task.save()
        messages.success(request, ("Данные задачи изменены."))
        return redirect('show_project_tasks', p_id=project.id)
    else:
        workers = ProjectTeam.objects.filter(project_id=p_id)  
        statuses = ProjectTaskStatus.objects.all()      
        return render(request, 'edit_task.html', {'project': project, 'task': task, 'workers': workers, 'statuses': statuses})
    

def del_user_task(request, t_id):
    task = ProjectTask.objects.get(pk=t_id)
    pid = task.project.id
    task.delete()
    messages.success(request, ("Задача удалена."))
    return redirect('show_project_tasks', p_id=pid)


def edit_task_status(request, t_id, p_id):
    task = ProjectTask.objects.get(pk=t_id)
    project = Project.objects.get(pk=p_id)
    if request.method == "POST":        
        sid = request.POST['sid']   
        status = ProjectTaskStatus.objects.get(pk=sid)        
        task.status=status              
        task.save()
        messages.success(request, ("Статус задачи изменен."))
        return redirect('show_user_tasks', p_id=project.id)
    else:        
        statuses = ProjectTaskStatus.objects.all()      
        return render(request, 'edit_task_status.html', {'project': project, 'task': task, 'statuses': statuses})
    

def show_chat(request):
    if not request.user.is_authenticated:
        return redirect('login')
    client = Client.objects.filter(user_id=request.user.id)[0]
    if client.studentgroup is None and client.user.groups.filter(name='clients').exists():
        return render(request, 'nogroup.html', {})
    else:
        curator = None
        cl_messages = None
        if request.user.groups.filter(name='clients').exists():
            curator = Client.objects.filter(user_id=client.studentgroup.curator.id)[0]  
            cl_messages = ClMessage.objects.filter((Q(sender_id=client.id) & Q(reciever_id=curator.id)) | (Q(sender_id=curator.id) & Q(reciever_id=client.id))).order_by('senddate') 
        else:
            s_groups = StudentGroup.objects.filter(curator_id=client.user.id)
            return render(request, 'show_groups_list.html', {'s_groups': s_groups})
        if request.method == "POST":
            mtext = request.POST.get('mess', False)         
            new_mess = ClMessage(sender=client, reciever = curator, mtext = mtext, senddate=datetime.datetime.now())
            f = request.FILES.get('myfile', False)
            if not f:
                new_mess.docfile = None
            #if request.FILES.get('myfile', False):                   
            else:
                 new_mess.docfile = request.FILES['myfile'] 
            new_mess.save()
            cl_messages = ClMessage.objects.filter((Q(sender_id=client.id) & Q(reciever_id=curator.id)) | (Q(sender_id=curator.id) & Q(reciever_id=client.id))).order_by('senddate') 
            return render(request, 'show_chat.html', {'cl_messages': cl_messages, 'id':request.user.id})
        else:
            return render(request, 'show_chat.html', {'cl_messages': cl_messages, 'id':request.user.id})
    
 
def open_contacts(request, g_id):
    g_students = Client.objects.filter(studentgroup_id=g_id)
    group = StudentGroup.objects.get(pk=g_id)
    return render(request, 'open_contacts.html', {'g_students': g_students, 'group': group})


def open_chat(request, s_id):
    curator = Client.objects.filter(user_id=request.user.id)[0]
    client = Client.objects.get(pk=s_id)
    if request.method == "POST":
        mtext = request.POST.get('mess', False)   
        new_mess = ClMessage(sender = curator, reciever = client, mtext = mtext, senddate=datetime.datetime.now())
        f = request.FILES.get('myfile', False)
        if not f:
            new_mess.docfile = None
            #if request.FILES.get('myfile', False):                   
        else:
            new_mess.docfile = request.FILES['myfile']                                         
        new_mess.save()
        cl_messages = ClMessage.objects.filter((Q(sender_id=client.id) & Q(reciever_id=curator.id)) | (Q(sender_id=curator.id) & Q(reciever_id=client.id))).order_by('senddate') 
        return render(request, 'show_chat.html', {'cl_messages': cl_messages, 'id':request.user.id})
    else:
        cl_messages = ClMessage.objects.filter((Q(sender_id=client.id) & Q(reciever_id=curator.id)) | (Q(sender_id=curator.id) & Q(reciever_id=client.id))).order_by('senddate')
        return render(request, 'show_chat.html', {'cl_messages': cl_messages, 'id':request.user.id}) 
