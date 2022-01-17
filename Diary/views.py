from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password

User = get_user_model()


def signup(request):
    if request.method == "POST":  # POST 방식일때
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 새로 만들어진 User의 DB를 저장.
            messages.success(request, '회원가입이 정상적으로 되었습니다.')  # 회원가입 되었을때
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def signOut(request):
    if request.method == "POST":
        pw = request.POST["pw"]
        user = request.user
        if check_password(pw, user.password):
            request.user.delete()
            messages.success(request, '탈퇴가 정상적으로 되었습니다.')
        else:
            messages.error(request, '탈퇴가 정상적으로 되지 않았습니다.')
        return redirect('index')
    else:
        return render(request, 'signOut.html')


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            user = authenticate(
                email=email,
                password=password
            )
            if user is not None:
                login(request, user)
                return render(request, 'main.html')
            else:
                messages.error(request, '없는 회원정보 입니다.')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'index.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_view')


def user(request):
    return render(request, 'user.html')
