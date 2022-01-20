from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserCreationForm, LoginForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth

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

def logout(request):
    return redirect('index')

def main(request):
    return redirect('index')

def user(request):
    return render(request, 'user.html')

def change_password(request):
  if request.method == "POST":
    user = request.user
    origin_password = request.POST["origin_password"]
    if check_password(origin_password, user.password):
      new_password = request.POST["new_password"]
      confirm_password = request.POST["confirm_password"]
      if new_password == confirm_password:
        user.set_password(new_password)
        user.save()
        messages.success(request, '비밀번호가 변경되었습니다.')
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')
      else:
        messages.error(request, '비밀번호가 같지 않습니다.')
    else:
      messages.error(request, '현재 비밀번호가 올바르지 않습니다.')
    return render(request, 'change_password.html')
  else:
    return render(request, 'change_password.html')


