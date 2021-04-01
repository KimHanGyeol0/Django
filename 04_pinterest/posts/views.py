from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .forms import PostForm, CommentForm
from .models import Post, Comment, Hashtag
from django.contrib.auth.decorators import login_required
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
@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # 사진 데이터는 POST가 아닌 FILES에 들어있음
        # 순서에 맞춰서 적을 거 아니면 (data=request.POST, files=request.FILSE)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for word in post.content.split():
                if word.startswith('#'):
                    # unique=True 때문에 있으면 가져오고, 없으면 생성 get_or_create
                    # (<Hashtag: Hashtag object (2)>, False) 가 반환
                    hashtag, created = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag)

            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
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

@require_POST
def comment_create(request, post_pk):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(pk=post_pk)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect('posts:detail', post.pk)
    
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)


@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('posts:detail', post_pk)

def like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        # 이미 좋아요를 누름
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
        # 아직 좋아요 안누름
        else:
            post.like_users.add(request.user)
        
        return redirect('posts:detail', post.pk)
    return redirect('acconts:login')

def hashtag(request, hashtag_pk):
    tag = get_object_or_404(Hashtag, pk=hashtag_pk)
    context = {
        'tag': tag,
    }

    return render(request, 'posts/hashtag.html', context)