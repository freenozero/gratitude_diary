from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Data
from datetime import datetime
from django.db import models
# Create your views here.

def main(request):
    return render(request, 'main.html')

def diary_view(request):
    datas = Data.objects.filter(id=request.user.id)
    return render(request, 'Diary.html', {'datas': datas})


def write_view(request):
    if request.method == "POST":
        newData = Data()
        newData.id = request.user.id
        newData.email = request.user.email
        newData.edit_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        newData.write_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        newData.diary_date = request.POST['inputDate']
        newData.content = request.POST['content']
        newData.save()
        return redirect('DiaryWrite')
    else:
        return render(request, 'DiaryWrite.html', {"times":datetime.today()})


def edit_view(request):
    date = request.POST.get('inputDate', False)
    print(date)
    return render(request, 'DiaryEdit.html')


# def erase_view(request):
#     return render(request, 'DiaryWrite.html')
#
#

def read_view(request, diary_cnt):
    if request.method == "POST":
        print("포스트으으")
        datas = Data.objects.filter(diary_cnt=diary_cnt)
        return render(request, 'DiaryRead.html', {'datas':datas})
    else:
        return render(request, 'DiaryRead.html')