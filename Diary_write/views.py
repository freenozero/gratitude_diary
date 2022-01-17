from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from Diary_write.models import data
# Create your views here.

def main(request):
    return render(request, 'main.html')


def Diary_view(request):
    if request.method == "POST":
        date = request.POST.get('inputDate', False)
        email = request.user.email
        datas = (data.objects.filter(date=date) & data.objects.filter(email=email)) #동일한 date, email 찾기
        if datas.exists():
            Mydata=datas.get(id=1)
            return render(request, 'DiaryEdit.html',{"Mydata":Mydata})
        else:
            return redirect('DiaryWrite')
    return render(request, 'Diary.html')


@csrf_protect
def write_view(request):
    if request.method == "POST":
        newData = data()
        newData.email = request.user.email
        newData.date = '2022-01-20'
        newData.content = request.POST['content']
        newData.save()
        return redirect('Diary')
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