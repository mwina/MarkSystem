

# Register your models here.
from django.contrib import admin
from All.models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Password', 'isDelete']


class PaperGradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'PaperName',
                    'FirstChecker', 'FirstGrade',
                    'SecondChecker', 'SecondGrade',
                    'ThirdChecker', 'ThirdGrade',
                    'CheckerNumber', 'isUsable',
                    'FinalGrade', 'isDelete']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(PaperGrade, PaperGradeAdmin)
