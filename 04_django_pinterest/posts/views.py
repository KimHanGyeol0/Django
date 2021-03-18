from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .forms import PostForm
from .models import Post
# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)

# 이렇게 적어도 되고
@require_http_methods(['GET', 'POST'])
# HTPP verb라고 하는 GET, POST 검사, 들어온 데이터(is_valid) 유효성 검사와 다름

# 이렇게 두 줄 적어도 됨
# @require_POST
# @require_safe
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # 사진 데이터는 POST가 아닌 FILES에 들어있음
        # 순서에 맞춰서 적을 거 아니면 (data=request.POST, files=request.FILSE)
        if form.is_valid():
            post = form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)

def detail(request, pk):
    post = Post.objects.get(pk=pk)

    context = {
        'post': post,
    }
    return render(request, 'posts/detail.html', context)

def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        # request.POST, request.FILES가 최신 데이터, instance가 기존 데이터, 기존 데이터를 최신 데이터로 덮어씌워줘
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post.pk)
    else:
        # 기존 데이터
        form = PostForm(instance=post)

    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)
