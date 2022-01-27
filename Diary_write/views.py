from django.shortcuts import render, redirect
from .models import Data
import datetime


def main(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return redirect('logout')


def diary_view(request, year=datetime.date.today().year, month=datetime.date.today().month, day=datetime.date.today().day, move=0):
    times = datetime.date(year,month, day)
    if request.user.is_authenticated:
        if move == 1: #뒤로 이동
            if times.month > 1:
                times = datetime.date(times.year, times.month - 1, times.day)
            else:
                times = datetime.date(times.year-1, 12, times.day)

        elif move == 2: #앞으로 이동
            if times.month < 12:
                times = datetime.date(times.year, times.month +1, times.day)
            else:
                times = datetime.date(times.year+1, 1, times.day)
        else:
            times.today()
        datas = Data.objects.filter(id=request.user.id)
        datas_date = []
        datas_cnt = []
        for i in datas:
            datas_date.append(i.diary_date.day)
        for i in datas:
            datas_cnt.append(i.diary_cnt)
        this_month = times.month
        this_year = times.year
        this_month_firstday = datetime.date(times.year, times.month, 1).weekday()
        last_day = month_last_day(this_month, times)  # 마지막 날짜 구하기
        return render(request, 'Diary.html',
                      {'datas_date': datas_date, 'times': times, 'last_day': last_day,
                       'firstday': this_month_firstday, 'this_month': this_month, 'this_year': this_year})
    else:
        return redirect('logout')


def month_last_day(this_month, times):
    if this_month in [1, 3, 5, 7, 8, 10, 12]:
        last_day = 31
    elif this_month == 2:
        if times.year % 4 == 0:
            last_day = 29
        else:
            last_day = 28
    else:
        last_day = 30
    return last_day


def write_view(request, year, month, day):
    if request.user.is_authenticated:
        times = datetime.date(year, month, day)
        if request.method == "POST":
            newData = Data()
            newData.id = request.user.id
            newData.email = request.user.email
            newData.edit_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            newData.write_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            newData.diary_date = datetime.date(year, month, day)
            newData.content = request.POST['content']
            try:
                datas = Data.objects.get(id=request.user.id, diary_date=newData.diary_date)
                return render(request, 'DiaryRead.html', {'datas': datas})
            except Data.DoesNotExist:  # datas로 받아온 다이어라가 없을 때 그냥 저장
                newData.save()
                return redirect('Diary')
        return render(request, 'DiaryWrite.html', {'times': times})
    else:
        return redirect('logout')


def edit_view(request, diary_cnt):
    if request.user.is_authenticated:
        datas = Data.objects.get(diary_cnt=diary_cnt)
        if request.method == "POST":
            return render(request, 'DiaryEdit.html', {'datas': datas})
        elif request.method == "GET":
            content = request.GET['content']
            datas.edit_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            datas.content = content
            datas.save()
            return redirect('Diary')
        return render(request, 'Diary.html')
    else:
        return redirect('logout')


def read_view(request, year, month, day):
    if request.user.is_authenticated:
        datas = Data.objects.get(diary_date__year=year, diary_date__month=month, diary_date__day=day)
        return render(request, 'DiaryRead.html', {'datas': datas})
    else:
        return redirect('logout')


def erase_view(request, diary_cnt):
    if request.user.is_authenticated:
        datas = Data.objects.get(diary_cnt=diary_cnt)
        if 're_ask' in request.POST:
            datas.delete()
            return redirect('Diary')
        if request.method == "POST":
            return render(request, 'DiaryErase.html', {'datas': datas})
    else:
        return redirect('logout')
