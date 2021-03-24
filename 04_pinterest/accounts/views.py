from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # 폼에 만드는 것은 ID, PW인데 db에서 생성되는 것은 session이다
        # 만들어진 것이 동일하지 않기 때문에 모델폼이 아니라 폼이다.
        # 회원가입은 유저를 생성, 로그인은 세션을 생성
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/form.html', context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def profile(request, pk):
    User = get_user_model()
    user_info = User.objects.get(pk=pk)
    context = {
        'user_info': user_info,
    }
    return render(request, 'accounts/profile.html', context)
