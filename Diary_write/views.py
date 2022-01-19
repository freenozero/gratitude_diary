from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Data
import datetime
from django.db import models
# Create your views here.

def main(request):
    return render(request, 'main.html')


def Diary_view(request):
    if request.method == "POST":
        datas = Data.objects.filter(id=request.user.id)
        print(datas)
        if datas.exists():
            mydata = datas.get(id=1)
            return render(request, 'DiaryEdit.html',{"mydata":mydata})
        else:
            return redirect('DiaryWrite')
    return render(request, 'Diary.html')


@csrf_protect
def write_view(request):
    if request.method == "POST":
        newData = Data()
        newData.id = request.user.id
        newData.email = request.user.email
        newData.edit_date = datetime.date.today()
        newData.diary_date = request.POST.get('inputDate', False)
        print(newData.diary_date)
        newData.content = request.POST['content']
        newData.save()
        return render(request, 'DiaryWrite.html', {'newdata':newData})
    else:
        return render(request, 'DiaryWrite.html')


def edit_view(request,Mydata): #수정될 내용도 저장해야함
        return render(request, 'DiaryEdit.html')


# def erase_view(request):
#     return render(request, 'DiaryWrite.html')
#
#

# def read_view(request):
#     return render(request, 'DiaryWrite.html')