from django.shortcuts import render, redirect
from django.contrib.auth.models import UserManager, User
from django.contrib.auth import login, authenticate


def signup(request):
    if request.method == "POST": #POST 방식일때
        if request.POST['password'] == request.POST['confirm']: #입력한 패스워드가 일치할 경우
            user = User.objects.create_user(username=request.POST["username"],
                                            password=request.POST["password"],
                                            email=request.POST["email"])
            # user.user_pwd = request.POST["password"] #모델 만든 후 해야함..
            # user.phone_number = request.POST["phone_num"]
            # user.user_id = request.POST["id"]
            user.save() #새로 만들어진 User의 DB를 저장.
            return redirect('/')
        return render(request, 'signup.html' ,{"message":"회원가입이 완료됨"})
    return render(request, 'signup.html')


def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            # 로그인 성공
            login(request, username)
            return render(request, 'user.html', {'username': username, 'password': password})
        else:
            # 로그인 실패시 notUser 문자 반환
            return render(request, 'index.html', {'notUser': True})
    return render(request, 'index.html')


# def index(request):
#     return render(request, 'index.html')
#
# def login(request):
#     return render(request, 'login.html')


def user(request):
    return render(request, 'user.html')
