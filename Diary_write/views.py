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
        Mydata = datas.get(id=1) #찾은 정보 당연히 하나겠지만.. 일단은 이렇게 해놓고 나중에 더 좋게 수정하기
        if datas.exists(): #비어 있지 않으면 수정
            return render(request, 'DiaryEdit.html', {"Mydata":Mydata})
        else: #비었으면 write
            return render(request, 'DiaryWrite.html', {"Mydata":Mydata})
    return render(request, 'Diary.html')


@csrf_protect
def write_view(request, Mydata):
    if request.method == "POST":
        newData = data()
        newData.email = request.user.email
        newData.date = Mydata.date #여기서 문제임.. date 직접적으로 넣으면 들어감
        newData.content = request.POST['content']
        newData.save()
        return redirect('index')
    else:
        return render(request, 'DiaryWrite.html')


def edit_view(request, Mydata): #수정한 거 저장해야함
        print(Mydata.date)
        return render(request, 'DiaryEdit.html')


# def erase_view(request):
#     return render(request, 'DiaryWrite.html')
#
#

# def read_view(request):
#     return render(request, 'DiaryWrite.html')