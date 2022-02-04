from django.shortcuts import render, redirect
from .models import Data
import datetime


def main(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return redirect('logout')


def diary_view(request):
    times = datetime.date.today()
    today = times
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_data = request.POST['cal_btn'].split('_')
            post_data[1], post_data[2] = int(post_data[1]), int(post_data[2])
            if post_data[0] == 'right':
                if post_data[2] < 12:
                    times = datetime.date(post_data[1], post_data[2] + 1, 1)
                else:
                    times = datetime.date(post_data[1] + 1, 1, 1)
            else:
                if post_data[2] > 1:
                    times = datetime.date(post_data[1], post_data[2] - 1, 1)
                    if times.month == today.month and times.year == today.year:
                        times = datetime.date(times.year, times.month, today.day)
                else:
                    times = datetime.date(post_data[1] - 1, 12, 1)
        datas = Data.objects.filter(id=request.user.id, diary_date__year=times.year, diary_date__month=times.month)
        first_day = datetime.date(times.year, times.month, 1).weekday()
        last_day = month_last_day(times.month, times)  # 마지막 날짜 구하기
        datas_date = [0 for _ in range(last_day)]
        for i in range(len(datas)):
            datas_date[i] = datas[i].diary_date.day
        return render(request, 'Diary.html',
                      {'datas_date': datas_date, 'times': times, 'today':today,
                       'firstday': first_day,'datas': datas})
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
        datas = Data.objects.get(id=request.user.id, diary_date__year=year, diary_date__month=month, diary_date__day=day)
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
