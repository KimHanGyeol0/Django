from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# 우리가 사용하고 있는 모델(장고가 이미 만든거) 이름이 User
# 위치 모르면 git에 타고 들어가고, 내가 지금까지 만든 앱과 구조가 같음

from django.contrib.auth.models import User
# flash messages
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/forms.html', context)
"""
폼은 데이터 입력하기 쉽도록 빈종이 만들어주는 것(파이썬으로 title, content 만들어주고 html form태그에 사용) + 검증 수단
빈종이와 쓰여진 데이터는 모델과 같아야한다.

정말 삭제하시겠습니까 물어 보는 것은 modal이 적절
삭제되었습니다 는 flash message로
"""

def login(request):
    # 로그인 되어 있으면 바로 index 페이지로
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, '이미 로그인 하셨습니다.')
        return redirect('accounts:index')
    if request.method == 'POST':
        # 모델 폼 아니고 그냥 폼
        # 유저 데이터를 가지고 세션을 생성하기 때문에, 사용하는 것과 만드는게 달라서 그냥 폼으로
        
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # flash messages
            messages.add_message(request, messages.INFO, '로그인 되었습니다.')
            return redirect('accounts:index')
        messages.add_message(request, messages.WARNING, '로그인에 실패하였습니다. ID와 PW를 확인해주세요.')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/forms.html', context)

def index(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'accounts/index.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user_info': user,
    }
    return render(request, 'accounts/profile.html', context)

def delete(request):
    request.user.delete()
    return redirect('accounts:index')

def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '수정완료되었습니다.')
            return redirect('accounts:profile', request.user.username)
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/forms.html', context)

def pw_update(request):
    if request.method == 'POST':
        # 폼마다 앞 뒤 넣어야되는 순서가 다 달라
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # refresh, password 변경하고도 세션 유지하기 위해서, 안하면 로그인 풀림
            update_session_auth_hash(request, form.user)
            messages.info(request, '비밀번호가 성공적으로 변경되었습니다!')
            return redirect('accounts:profile', request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/forms.html', context)