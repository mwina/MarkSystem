from django.db import models

# Create your models here.
from django.db.models import Q
from django.http import HttpResponse, request


class PaperGrade(models.Model):
    PaperFile = models.FileField(upload_to='File/')
    PaperName = models.CharField(max_length=256, default=PaperFile.name)

    FirstChecker = models.CharField(max_length=20, blank=True)
    FirstGrade = models.IntegerField(default=0)

    SecondChecker = models.CharField(max_length=20, blank=True)
    SecondGrade = models.IntegerField(default=0)

    ThirdChecker = models.CharField(max_length=20, blank=True)
    ThirdGrade = models.IntegerField(default=0)

    CheckerNumber = models.IntegerField(default=0)
    isUsable = models.BooleanField(default=False)
    FinalGrade = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)

    threshold = 10
    '''阈值'''

    def logic_delete(self):
        self.isDelete = True
        self.save()
        return None

    def file_type(self):
        file = self.PaperFile
        file_type = file.name.split('.')[-1].lower()
        return file_type

    def usable_check(self):  #阈值合理性判断
        if abs(self.FirstGrade - self.SecondGrade) <= self.threshold and \
                abs(self.FirstGrade - self.ThirdGrade) <= self.threshold and \
                abs(self.SecondGrade - self.ThirdGrade) <= self.threshold:
            self.isUsable = True
            self.save()
        return None

    def update(self, PaperGrade, CheckerName):
        '''项目 项目成绩 评卷人'''
        if self.CheckNumber <= 2:
            if self.CheckNumber == 0:
                self.FirstGrade = PaperGrade
                self.FirstChecker = CheckerName
                self.CheckNumber = self.CheckNumber + 1
            elif self.CheckNumber == 1:
                self.SecondGrade = PaperGrade
                self.SecondChecker = CheckerName
                self.CheckNumber = self.CheckNumber + 1
            else:
                self.ThirdGrade = PaperGrade
                self.ThirdChecker = CheckerName
                self.CheckNumber = self.CheckNumber + 1
            if self.CheckNumber == 3:
                self.FinalGrade = (self.FirstGrade + self.SecondGrade + self.ThirdGrade) / 3
                self.usable_check()
            self.save()
            return HttpResponse('评分成功')
        else:
            return HttpResponse('打分失败，已有三人进行该项目的评分')

    def my_checked(self, name):
        if self.FirstChecker == name or self.SecondChecker == name or self.ThirdChecker == name:
            return (['http://127.0.0.1:8000/All/index?filename='+self.PaperName, self.PaperName])
        else:
            return None

    def my_will_check(self, name):
        if self.FirstChecker != name and self.SecondChecker != name and self.ThirdChecker != name:
            return (['http://127.0.0.1:8000/All/index?filename='+self.PaperName, self.PaperName])


class UserInfo(models.Model):
    Name = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)



