from django.db import models

class Vac(models.Model):
    name     = models.CharField('Title', max_length=200)
    desc     = models.TextField('Description', max_length=400, default = '')
    empler   = models.CharField('Employer', max_length=200, default = '')
    skills   = models.CharField('Skills', max_length=200, default = '')
    salary   = models.IntegerField('Salary', blank = True)
    sphere   = models.CharField('Sphere', max_length=200, default = '')
    datetime = models.DateTimeField('Date published', auto_now = True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title    = models.CharField('Course Title', max_length=200)
    contact  = models.CharField('Contacts', max_length=200)
    descript = models.TextField('Course Description', max_length=500)
    sphere   = models.CharField('Sphere', max_length=200, default = '')
    def __str__(self):
        return self.title
