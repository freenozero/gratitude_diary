from django.shortcuts import render, redirect
from .models import Data
import datetime

def main(request):
    return render(request, 'main.html')


def diary_view(request):
    datas = Data.objects.filter(id=request.user.id)
    times = datetime.date.today()
    day_of_week = datetime.date.today().weekday()
    this_month = datetime.date.today().month
    this_month_firstday = datetime.date(times.year, times.month, 1).weekday()
    if this_month in [1, 3, 5, 7, 8, 10, 12]:
        last_day = 31
    elif this_month == 2:
        if times.year % 4 == 0:
            last_day = 29
        else:
            last_day = 28
    else:
        last_day = 30
    return render(request, 'Diary.html', {'datas':datas, 'times':times, 'day_of_week':day_of_week, 'last_day':last_day, 'firstday':this_month_firstday})


def write_view(request):
    times = datetime.date.today()
    if request.method == "POST":
        newData = Data()
        newData.id = request.user.id
        newData.email = request.user.email
        newData.edit_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        newData.write_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        newData.diary_date = request.POST['input_date']
        newData.content = request.POST['content']
        try:
            datas = Data.objects.get(id=request.user.id, diary_date=newData.diary_date)
            return render(request, 'DiaryRead.html', {'datas':datas})
        except Data.DoesNotExist: #datas로 받아온 다이어라가 없을 때 그냥 저장
            newData.save()
            return redirect('Diary')
    return render(request, 'DiaryWrite.html', {'times':times})


def edit_view(request, diary_cnt):
    datas = Data.objects.get(diary_cnt=diary_cnt)
    if request.method == "POST":
        return render(request, 'DiaryEdit.html', {'datas':datas})
    elif request.method == "GET":
        content = request.GET['content']
        datas.edit_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        datas.content = content
        print(datas.content)
        datas.save()
        return redirect('Diary')
    return render(request, 'Diary.html')


def read_view(request, year, month, day):
    if request.method == "POST":
        datas = Data.objects.get(diary_date__year=year, diary_date__month=month, diary_date__day=day)
        return render(request, 'DiaryRead.html', {'datas':datas})
    else:
        return render(request, 'DiaryRead.html')


def erase_view(request, diary_cnt):
    datas = Data.objects.get(diary_cnt=diary_cnt)
    print(request.POST)
    if 're_ask' in request.POST:
        datas.delete()
        return redirect('Diary')
    if request.method == "POST":
        return render(request, 'DiaryErase.html', {'datas':datas})
    return render(request, 'DiaryErase.html')