from django.contrib import admin

from courses.models import Attempt, Client, Course, LTheme, Lection, Project, ProjectRole, ProjectTask, ProjectTaskStatus, ProjectTeam, QAnswer, Question, Round, StudentGroup

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')
    ordering = ('title',)
    search_fields = ('summary',)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'curator')
    ordering = ('title',)
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('lname', 'name', 'phone', 'img', 'user')
    ordering = ('lname',)
    search_fields = ('lname',)


@admin.register(LTheme)
class LThemeAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'summary', 'course')
    ordering = ('number','title')
    search_fields = ('title', 'summary')


@admin.register(Lection)
class LectionAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'file_path', 'theme')
    ordering = ('number',)
    search_fields = ('title', 'theme')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qtext', 'qtype', 'theme')    
    search_fields = ('qtext', )


@admin.register(QAnswer)
class QAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'atext', 'status')    
    search_fields = ('atext', )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'adate', 'theme')    
    search_fields = ('user', 'adate')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'answer')  


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'startdate', 'enddate', 'files_archive')
    ordering = ('startdate',)
    search_fields = ('title', 'summary')  


@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')
    ordering = ('title',)
    search_fields = ('title', 'summary') 


@admin.register(ProjectTaskStatus)
class ProjectTaskStatusAdmin(admin.ModelAdmin):
    list_display = ('title', )
    ordering = ('title',)
    search_fields = ('title', )    


@admin.register(ProjectTeam)
class ProjectTeamAdmin(admin.ModelAdmin):
    list_display = ('project', 'member', 'role')
    ordering = ('-id',)   


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('creator', 'worker', 'tasktext', 'status', 'startdate', 'project', 'enddate')
    ordering = ('project__id',)
    search_fields = ('tasktext', 'status')    