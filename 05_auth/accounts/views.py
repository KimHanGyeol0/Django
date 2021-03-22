from django.shortcuts import render, redirect
from django.contrib.auth import login as au_login
from django.contrib.auth import logout as au_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm, UserChangeForm
from . forms import CustomUserChangeForm

# Create your views here.
# 세션을 create
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # 개발자 도구에서 사용자 이름은 name=username, 비밀번호는 name=password로 들어옴
        # 얘는 첫 번째가 request, 두 번째 request.POST
        # 원래 모델폼에서는 첫 번째 request.POST, 두 번째 기존 데이터로 받았음
        # 얘는 모델폼이 아님, 폼이다.
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 세션 create
            # login(request, form.get_user())
            # view 함수와 이름이 같으면 안됨 = > 별칭으로 하던가
            au_login(request, form.get_user())
            # form.get_user()는 user_cache 반환
            # user = form.get_user()
            # au_login(request, user)
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    # 들어온 요청 삭제
    au_logout(request)
    return redirect('articles:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        # 얘는 모델폼이래
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 유저가 만들어짐, 로그인 바로 됐으면 좋겠는데?
            # save하면 반환값이 return user이다
            user = form.save()
            # 세션 만들어서 로그인 자동으로 시켜줌
            au_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        # 얘도 모델 폼
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)