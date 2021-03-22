from django.shortcuts import render, redirect
from .models import Article

# Create your views here.

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    article = Article.objects.create(title=title, content=content)
    context = {
        'article': article,
    }
    # return render(request, 'articles/create.html', context)
    return redirect('articles:index')
    # 새로 만들고 게시물 목록으로 보내줌
    # articles의 index로 가주세요
    # articles의 index로 다시 요청을 보냄. urls - views - index

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)

def delete(request, pk):

    article = Article.objects.get(pk=pk)
    
    article.delete()

    return redirect('articles:index')
    
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/edit.html', context)

def update(request, pk):
    # 기존 데이터
    article = Article.objects.get(pk=pk)

    # 수정한 데이터
    title = request.POST.get('title')
    content = request.POST.get('content')

    # 수정하고 저장
    article.title = title
    article.content = content
    article.save()

    return redirect('articles:detail', article.pk)