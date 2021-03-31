from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from django.http import HttpResponse, HttpResponseForbidden
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if request.user == article.user:
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
        # return HttpResponseForbidden()
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)
        

@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('articles:detail', article.pk)
        context = {
            'comment_form': comment_form,
            'article': article,
        }
        return render(request, 'articles/detail.html', context)
    return redirect('accounts:login')
    # return HttpResponse(status=401)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        # return HttpResponseForbidden()
    return redirect('articles:detail', article_pk)
    # return HttpResponse(status=401)

@require_POST
def likes(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)

        # article 관계 테이블에 user가 있을 때
        # 게시물에 좋아요를 누른 모든 유저 리스트에 내가 있는지 없는지
        # if article.like_users.filter(pk=request.user.pk).exists(): 이거 쓰면 쿼리 셋을 다 안봐도됨
        # article in request.user.like_articles.all()해도 됨. 내가 좋아요를 누른 모든 게시물에 이 게시물이 있는지
        if request.user in article.like_users.all():
            # 이미 눌렀으니까 좋아요 취소
            article.like_users.remove(request.user)
            # request.user_like_articles.remove(article)
        else:
            # 좋아요 누름
            article.like_users.add(request.user)
            # request.user_like_articles.add(article)

        return redirect('articles:index')
    return redirect('accounts:login')