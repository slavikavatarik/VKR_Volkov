from django.db import models
from django.contrib.auth.models import User
import os


class Course(models.Model):
    title = models.CharField('Название', max_length=255)
    summary = models.TextField('Описание', max_length=7000)        

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Курс')
        verbose_name_plural = ('Курсы')


class StudentGroup(models.Model):
    title = models.CharField('Название', max_length=255)
    courses = models.ManyToManyField(Course, verbose_name='Курсы')
    curator = models.ForeignKey(
        User, verbose_name='Куратор', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Группа')
        verbose_name_plural = ('Группы')


class Client(models.Model):
    lname = models.CharField('Фамилия', max_length=255)
    name = models.CharField('Имя', max_length=255)
    phone = models.CharField('Телефон', max_length=255)
    img = models.ImageField(
        'Изображение', null=True, blank=True, upload_to="images/clients/")
    studentgroup = models.ForeignKey(
        StudentGroup, verbose_name='Группа', null=True, blank=True, on_delete=models.DO_NOTHING)

    user = models.OneToOneField(
        User, verbose_name='Логин', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.lname + " " + self.name + ", " + self.phone

    class Meta:
        verbose_name = ('Участник')
        verbose_name_plural = ('Участники')


class LTheme(models.Model):
    title = models.CharField('Название', max_length=255)
    summary = models.TextField('Описание', max_length=7000)
    number = models.IntegerField('Номер', blank=True, null=True)
    course = models.ForeignKey(
        Course, verbose_name='Курс', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Тема')
        verbose_name_plural = ('Темы')


class Lection(models.Model):
    title = models.CharField('Название', max_length=255)
    file_path = models.FileField('Файл', upload_to="docs/", max_length=255)
    theme = models.ForeignKey(
        LTheme, verbose_name='Тема', on_delete=models.DO_NOTHING)
    number = models.IntegerField('Номер', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.file_path.name)
    

    class Meta:
        verbose_name = ('Лекция')
        verbose_name_plural = ('Лекции')


class Question(models.Model):
    qtext = models.TextField('Текст', max_length=7000)
    qtype = models.CharField('Тип', max_length=10)
    theme = models.ForeignKey(
        LTheme, verbose_name='Тема', on_delete=models.DO_NOTHING)   
    def __str__(self):
        return self.qtext

    class Meta:
        verbose_name = ('Вопрос')
        verbose_name_plural = ('Вопросы')


class QAnswer(models.Model):
    question = models.ForeignKey(
        Question, verbose_name='Вопрос', on_delete=models.DO_NOTHING)
    atext = models.CharField('Ответ', max_length=255)
    status = models.BooleanField('Статус', max_length=255)

    def __str__(self):
        return self.atext

    class Meta:
        verbose_name = ('Ответ')
        verbose_name_plural = ('Ответы')


class Attempt(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.DO_NOTHING)
    adate = models.DateField('Дата') 
    theme = models.ForeignKey(
        LTheme, verbose_name='Тема', on_delete=models.DO_NOTHING, blank=True, null=True)   
    mark = models.IntegerField('Оценка', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ('Попытка')
        verbose_name_plural = ('Попытки')


class Round(models.Model):
    attempt = models.ForeignKey(
        Attempt, verbose_name='Попытка', on_delete=models.DO_NOTHING)
    answer = models.ForeignKey(
        QAnswer, verbose_name='Ответ', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ('Раунд')
        verbose_name_plural = ('Раунды')



class Project(models.Model):
    title = models.CharField('Название', max_length=255)
    summary = models.TextField('Описание', max_length=7000)    
    startdate = models.DateField('Начат')     
    enddate = models.DateField('Завершен')    
    files_archive = models.FileField('Файл', upload_to="docs/", max_length=255)   

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Проект')
        verbose_name_plural = ('Проекты')


class ProjectRole(models.Model):
    title = models.CharField('Название', max_length=255)
    summary = models.TextField('Описание', max_length=7000)        

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Роль')
        verbose_name_plural = ('Роли')


class ProjectTaskStatus(models.Model):
    title = models.CharField('Название', max_length=255)            

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Статус')
        verbose_name_plural = ('Статусы')


class ProjectTeam(models.Model):
    project = models.ForeignKey(
        Project, verbose_name='Проект', on_delete=models.DO_NOTHING, blank=True, null=True)   
    member = models.ForeignKey(
        Client, verbose_name='Участник', on_delete=models.DO_NOTHING, blank=True, null=True)   
    role = models.ForeignKey(
        ProjectRole, verbose_name='Роль', on_delete=models.DO_NOTHING, blank=True, null=True)   
    
    def __str__(self):
        return self.project.title

    class Meta:
        verbose_name = ('Команда проекта')
        verbose_name_plural = ('Команды проекта')
    

class ProjectTask(models.Model):
    creator = models.ForeignKey(
        Client, verbose_name='Создатель', on_delete=models.DO_NOTHING, blank=True, null=True)   
    worker = models.ForeignKey(
        Client, related_name='proj_task_worker', verbose_name='Исполнитель', on_delete=models.DO_NOTHING, blank=True, null=True)   
    tasktext = models.TextField('Задача', max_length=7000)
    status = models.ForeignKey(
        ProjectTaskStatus, verbose_name='Статус', on_delete=models.DO_NOTHING, blank=True, null=True)   
    startdate = models.DateField('Начата')     
    project = models.ForeignKey(
        Project, verbose_name='Проект', on_delete=models.DO_NOTHING, blank=True, null=True)   
    enddate = models.DateField('Завершена')   

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ('Задача проекта')
        verbose_name_plural = ('Задачи проекта')


class ClMessage(models.Model):
    sender = models.ForeignKey(Client, related_name='msender', verbose_name='Отправитель',
                               on_delete=models.DO_NOTHING)
    reciever = models.ForeignKey(Client, related_name='msrec', verbose_name='Получатель',
                               on_delete=models.DO_NOTHING)    
    mtext = models.TextField('Сообщение', max_length=7000)
    senddate = models.DateTimeField('Дата и время отправки')
    docfile = models.FileField('Файл', blank=True, null=True, upload_to='files/')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ('Сообщение')
        verbose_name_plural = ('Сообщения')


class RoundRow:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers


class ReportThemeRow:
    def __init__(self, theme, avg_mark, err_amount, r_amount):
        self.theme = theme
        self.avg_mark =avg_mark
        self.err_amount = err_amount
        self.r_amount = r_amount