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
    print("회원가입 됨")
    User = get_user_model()
    print(User.email)
    if request.method == 'POST':
        print("1")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            print("2")
            print(User.objects.filter())
            if User.objects.filter(email=email).count() != 1:
                print("3")
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('Email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                print("3")
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, message, 'whdms1107@gmail.com', [to_email])
                return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    return render(request, 'regform.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    print('으아아')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


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
