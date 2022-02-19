from django.shortcuts import render, redirect
from .models import Data
import calendar
import datetime


class Week:
    def __init__(self, year, month, request):
        self.last_day = datetime.date(year, month, get_lastday(year, month))
        self.diary_cnt = get_week_no(datetime.date(year, month, self.last_day.day))
        self.week_cnt = []
        for _ in range(self.diary_cnt):
            self.week_cnt.append(0)
        cnt = Data.objects.filter(id=request.user.id, month_check__year=year, month_check__month=month)
        for i in cnt:
            self.week_cnt[i.week_date - 1] += 1
    def add_weekcnt(self, num):
        self.week_cnt[num - 1] += 1

    def get_weekcnt(self):
        return self.week_cnt


def main(request):
    book_year = datetime.date.today().year
    if request.user.is_authenticated:
        week_class = []
        books = Data.objects.filter(id=request.user.id, diary_date__year=book_year)
        if request.method == 'POST':
            post_data = request.POST['book_year'].split('_')
            book_year = int(post_data[0])
            if post_data[1] == 'right':
                book_year += 1
            else:  # 날짜를 왼쪽[달 감소]
                book_year -= 1
        for i in range(1, 13):
            week_class.append(Week(book_year, i, request))
        return render(request, 'main.html', {'book_year': book_year, 'books': books,
                                             'datas': week_class})
    else:
        return redirect('logout')


def get_date(y, m, d):
    s = f'{y:04d}-{m:02d}-{d:02d}'
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def get_week_no(date):
    target = get_date(date.year, date.month, date.day)
    firstday = target.replace(day=1)
    if firstday.weekday() == 6:
        origin = firstday
    elif firstday.weekday() < 3:
        origin = firstday - datetime.timedelta(days=firstday.weekday() + 1)
    else:
        origin = firstday + datetime.timedelta(days=6 - firstday.weekday())
    return (target - origin).days // 7 + 1


def diary_view(request):
    times = datetime.date.today()  # 현재 날짜 정보 저장
    today = times  # 날짜 정보 저장
    if request.user.is_authenticated:  # 로그인 이 되어 있는지 확인
        if request.method == 'POST':  # request 메소드 가 post 형식 일때
            post_data = request.POST['cal_btn'].split('_')
            # form 안에 있는 name="cal_btn" 의 value 값을 가져온 후, '_' 기준 으로 split 한다.
            post_data[1], post_data[2] = int(post_data[1]), int(
                post_data[2])  # 0, 1, 2 배열중 1, 2 배열을 정수 형태로 변환 한다. 이유 : 년, 월 이기 때문에 정수 값이 필요
            if post_data[0] == 'right':  # 날짜를 오른쪽[달 증가]
                if post_data[2] < 12:  # 현재 표시된 월이 12월 보다 낮을때
                    times = datetime.date(post_data[1], post_data[2] + 1, 1)
                    # times 변수에 표시된 년도, 표시된 월 + 1 , 1 일을 datetime 형태로 저장 한다.
                else:
                    times = datetime.date(post_data[1] + 1, 1, 1)
            else:  # 날짜를 왼쪽[달 감소]
                if post_data[2] > 1:  # 표시된 월이 1월 보다 클 경우
                    times = datetime.date(post_data[1], post_data[2] - 1, 1)
                    if times.month == today.month and times.year == today.year:  # 증가된 날짜의 연,월이 today 날짜와 동일 할경우
                        times = datetime.date(times.year, times.month, today.day)  # day 를 오늘 날짜로 변경 한다.
                else:
                    times = datetime.date(post_data[1] - 1, 12, 1)  # 표시된 월이 1월 보다 작을 경우
        datas = Data.objects.filter(id=request.user.id, diary_date__year=times.year, diary_date__month=times.month)
        first_day = datetime.date(times.year, times.month, 1).weekday() + 1
        last_day = get_lastday(times.year, times.month)  # 마지막 날짜 구하기
        datas_date = [0 for _ in range(last_day)]
        for i in range(len(datas)):
            datas_date[i] = datas[i].diary_date.day
        return render(request, 'Diary.html',
                      {'datas_date': datas_date, 'times': times, 'today': today,
                       'firstday': first_day, 'datas': datas})
    else:
        return redirect('logout')


def get_lastday(year, month):
    return calendar.monthrange(year, month)[1]


def test_write(request):
    for year in range(2020,2023):
        for i in range(1, 13):
            for j in range(1, calendar.monthrange(year, i)[1]):
                times = datetime.date(year, i, j)
                print(times)
                newData = Data()
                newData.id = request.user.id
                newData.email = request.user.email
                newData.edit_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                newData.write_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                newData.diary_date = datetime.date(times.year, times.month, times.day)
                if get_week_no(datetime.date(times.year, times.month, times.day)) == 0:
                    if times.month == 1:
                        newData.month_check = datetime.date(times.year - 1, 12, get_lastday(times.year - 1, 12))
                        newData.week_date = get_week_no(datetime.date(times.year - 1, 12, newData.month_check.day))
                    else:
                        newData.month_check = datetime.date(times.year, times.month - 1, get_lastday(times.year, times.month - 1))
                        newData.week_date = get_week_no(datetime.date(times.year, times.month - 1, newData.month_check.day))
                else:
                    newData.month_check = datetime.date(times.year, times.month, get_lastday(times.year, times.month))
                    newData.week_date = get_week_no(datetime.date(times.year, times.month, times.day))

                newData.content = str(year)+"년"+str(i)+"월"+str(j)+"일"
                try:
                    datas = Data.objects.get(id=request.user.id, diary_date=datetime.date(times.year, times.month, times.day))
                    # return redirect('Diary')
                except Data.DoesNotExist:  # datas로 받아온 다이어라가 없을 때 그냥 저장
                    newData.save()
                    # return redirect('Diary')
    return redirect('main')


def write_view(request):
    if request.user.is_authenticated:
        get_data = list(map(int, request.GET['cal_date'].split('_')))
        times = datetime.date(get_data[0], get_data[1], get_data[2])
        if request.method == "POST":
            newData = Data()
            newData.id = request.user.id
            newData.email = request.user.email
            newData.edit_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            newData.write_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            newData.diary_date = datetime.date(times.year, times.month, times.day)
            if get_week_no(datetime.date(times.year, times.month, times.day)) == 0:
                if times.month == 1:
                    newData.month_check = datetime.date(times.year - 1, 12, get_lastday(times.year - 1, 12))
                    newData.week_date = get_week_no(datetime.date(times.year - 1, 12, newData.month_check.day))
                else:
                    newData.month_check = datetime.date(times.year, times.month - 1,
                                                        get_lastday(times.year, times.month - 1))
                    newData.week_date = get_week_no(datetime.date(times.year, times.month - 1, newData.month_check.day))
            else:
                newData.month_check = datetime.date(times.year, times.month, get_lastday(times.year, times.month))
                newData.week_date = get_week_no(datetime.date(times.year, times.month, times.day))

            newData.content = request.POST['content']
            try:
                datas = Data.objects.get(id=request.user.id,
                                         diary_date=datetime.date(times.year, times.month, times.day))
                return render(request, 'DiaryRead.html', {'datas': datas})
            except Data.DoesNotExist:  # datas로 받아온 다이어라가 없을 때 그냥 저장
                newData.save()
                return redirect('Diary')
        else:
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


def read_view(request):
    if request.user.is_authenticated:
        get_data = list(map(int, request.GET['cal_date'].split('_')))
        datas = Data.objects.get(id=request.user.id, diary_date__year=get_data[0], diary_date__month=get_data[1],
                                 diary_date__day=get_data[2])
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


def decorate_note(request):
    return render(request, 'decorate_note.html')
