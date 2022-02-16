from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .forms import UserCreationForm, LoginForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.core.mail import send_mail

User = get_user_model()


def signups(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).count() == 0:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = '[감사노트] 계정 활성화 이메일'
                message = render_to_string('Email.html', {
                    'user': user,
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, message, 'whdms1107@gmail.com', [to_email])
                messages.success(request, '입력한 아이디의 메일을 통해 인증을 해주세요.')  # 회원가입 되었을때
                return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '인증을 완료했습니다. 로그인해주세요.')
        return redirect('index')
    else:
        return HttpResponse('링크가 잘못되었습니다.')


def signOut(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('logout')


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
                return redirect('main')
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
    return redirect('index')


def main(request):
    return redirect('index')



def change_password(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('logout')


def userprofile(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'user_profile.html')
    else:
        return redirect('logout')


def change_phonenum(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            new_phonenum = request.POST["new_phonenum"]
            user.phone_num = new_phonenum
            user.save()
            messages.success(request, '전화번호가 변경되었습니다')
            return redirect('index')
        else:
            return render(request, 'change_phonenum.html')
    else:
        return redirect('logout')
