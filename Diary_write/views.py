import data as data
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
        newData.diary_date = request.POST['input_date']
        newData.content = request.POST['content']
        newData.save()
        return redirect('Diary')
    else:
        return render(request, 'DiaryWrite.html', {"times":datetime.today()})


def edit_view(request, diary_cnt):
    datas = Data.objects.get(diary_cnt=diary_cnt)
    if request.method == "POST":
        return render(request, 'DiaryEdit.html', {'datas':datas})
    elif request.method == "GET":
        content = request.GET['content']
        datas.edit_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        datas.content = content
        datas.save()
        return redirect('Diary')
    return render(request, 'DiaryEdit.html')


def read_view(request, diary_cnt):
    if request.method == "POST":
        datas = Data.objects.get(diary_cnt=diary_cnt)
        return render(request, 'DiaryRead.html', {'datas': datas})
    else:
        return render(request, 'DiaryRead.html')


def erase_view(request, diary_cnt):
    datas = Data.objects.get(diary_cnt=diary_cnt)
    if request.method == 'POST':
        name = request.GET['name']
        print(name)
        if name == 're_ask':
            datas.delete()
            return redirect('Diary')
        else:
            return render(request, 'DiaryErase.html', {'datas':datas})
    return render(request, 'DiaryErase.html')