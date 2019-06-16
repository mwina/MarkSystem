from django.db.models import Q
from django.shortcuts import render, redirect
from django import http
# Create your views here.
from pydocx import PyDocX

from All.models import PaperGrade, UserInfo


def checked(request, name):
    #查看用户批阅情况
    paper_list = PaperGrade.objects.filter(Q(FirstChecker=name) | Q(SecondChecker=name) | Q(ThirdChecker=name))
    for Paper in paper_list:
        print(Paper.PaperName, Paper.FirstChecker, Paper.FirstGrade,
              Paper.SecondChecker, Paper.SecondGrade,
              Paper.ThirdChecker, Paper.ThirdGrade,
              Paper.FinalGrade)

    return render(request, 'All/user.html')


def show(request):
    #展示已知所有批改情况
    paper_list = PaperGrade.objects.all()
    for Paper in paper_list:
        print(Paper.PaperName, Paper.FirstChecker, Paper.FirstGrade,
              Paper.SecondChecker, Paper.SecondGrade,
              Paper.ThirdChecker, Paper.ThirdGrade,
              Paper.FinalGrade)
    return render(request, 'All/show.html')


def login(request):
    #登陆
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = UserInfo.objects.get(Name=username)
            except:
                return render(request, 'All/login.html')
            else:
                if user.Password == password:
                    request.session.setdefault('username', user.Name)
                    return http.HttpResponseRedirect('http://127.0.0.1:8000/All/list')
                else:
                    return render(request, 'All/login.html')
    return render(request, 'All/login.html')


def list(request):
    username = request.session.get('username', None)
    reviewList = []
    unReviewList = []
    paper_list = PaperGrade.objects.filter(CheckerNumber__lte=2)
    for paper1 in paper_list:
        if paper1.my_checked(username) is not None:
            reviewList.append(paper1.my_checked(username))
    for paper2 in paper_list:
        if paper2.my_will_check(username) is not None:
            unReviewList.append(paper2.my_will_check(username))

    request.session.set_expiry(0)

    return render(request, 'All/list.html', {'reviewList': reviewList, 'unReviewList': unReviewList})


def index(request):
    if request.method == "GET":
        papername = request.GET.get('filename', None)
        paper = PaperGrade.objects.get(PaperName=papername)
        username = request.session.get('username', None)
        user = UserInfo.objects.get(Name=username)
        user.PaperChecking = papername
        user.save()
        if paper.file_type() is 'docx':
            html = PyDocX.to_html(paper)
            return render(request, html)  #不知对错
        else:
            return render(request, 'All/index.html', {'filename': r'/File/' + paper.PaperName})  #url写法自我怀疑人生中
    else:
        return render(request, 'All/index.html')
    return render(request, 'All/index.html')


def gcore(request):
    username = request.session.get('username', None)
    user = UserInfo.objects.get(Name=username)
    papername = user.PaperChecking
    paper = PaperGrade.objects.get(PaperName=papername)
    if request.method == "POST":
        papergrade = request.POST.get('grade', None)
        paper.update(papergrade, username)
    user.PaperChecking = None
    user.save()
    return http.HttpResponseRedirect('http://127.0.0.1:8000/All/list')