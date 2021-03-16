from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm, ArticleModelForm

# Create your views here.
def index(request):
    articles = Article.objects.all()
    # articles = Article.objects.all().order_by('-id')로 하면 역순으로 정렬
    # articles = Article.objects.all().order_by('title')로 하면 title 기준으로 정렬
    context = {
        'articles':articles,
    }
    return render(request, 'articles/index.html',context)

def new(request):
    form = ArticleForm()
    model_form = ArticleModelForm()

    context = {
        'form': form,
        'model_form': model_form,

    }
    return render(request, 'articles/new.html', context)

def create(request):
    # 기본 저장 구조
    # 데이터 가져오기
    # title = request.POST.get('title')
    # content = request.POST.get('content')

    # 데이터 저장
    # article = Article()
    # article.title = title
    # article.content = content
    # article.save()


    # 모델 폼을 이용한 저장
    # 모델 폼에 입력하여 제출하면, POST 방식으로 create에 보내준다. 보내온 종이?(입력한 데이터)를 검증하고 저장
    # 종이는 여기서 만든 model_form = ArticleModelForm(), 데이터를 POST로 적음

    # 모델 폼을 가져오기, 사용자가 넣은 데이터를 입력이된 상태를 인스턴스화, 입력된 폼 덩어리를 가져온다
    # 폼 덩어리로 가져와서 따로 따로 저장할 필요 없음
    model_form = ArticleModelForm(request.POST)
    # 모델 폼 검증, 정확하게 데이터가 들어가 있는지, max_length라던가 필수 인자라던가 not null(DB 제약사항)
    # 폼 보다는 모델 검증 느낌, 검증은 서버에서 함, 위에서 하는 '입력값이 필요합니다'는 html에서 함
    if model_form.is_valid():
        model_form.save()

    return redirect('articles:index')

# new와 create를 하나의 함수로
# 하나의 url로 여러 기능, restful
def new_create(request):
    # 데이터가 들어 있는지
    # 5. POST 방식으로 요청이 들어옴 (잘못된 데이터)
    # 10. POST 방식으로 요청(옳은 데이터, 다시 적은 데이터)
    if request.method == 'POST':
        # 6. 빈종이에 데이터를 입력
        # 1.. 옳은 데이터 입력
        form = ArticleModelForm(request.POST)
        # 7. 유효성 검사
        # 12. 유효성 검사 성공
        if form.is_valid():
            # 저장하고 detail 상세 페이지로 보냄
            # 13. 데이터 저장
            # 14. 상세페이지 이동
            article = form.save()
            return redirect('articles:detail', article.pk)

    # 데이터가 없음, 1. GET 방식으로 데이터 요청
    else:
        # 모델 폼을 주면서 데이터 넣을 수 있도록
        # 데이터 넣고 다시 new_create로 보냄
        # 2. 빈 종이 생성
        form = ArticleModelForm()

    # 3. 빈 종이를 사용자에게 전송
    # 8. 유효성 검사 실패, 유효성 검사를 통과한 기존 데이터만 입력되어 있는 종이를 전송
    context = {
        'form': form,
    }
    # 4. html 파일 랜더링 (빈 종이 포함)
    # 9. html 파일 랜더링 (유효성 검사를 통과한 데이터 포함하는 html을 준다)
    return render(request, 'articles/form.html', context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)

    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)

def update(request, pk):
    # 기존 데이터
    article = Article.objects.get(pk=pk)
    # 최신 데이터가 들어왔는가?
    if request.method == 'POST':
        # 기존의 데이터를 방금 수정해서 POST로 받은 데이터로 수정해준다.
        # 기존 정보를 모르기 때문에 instance에 덮어씌어질 article을 넣어주고, 새로운 데이터로 수정
        form = ArticleModelForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)

    else:
        # 기존 데이터를 인스턴스로 모델폼으로 만듦
        form = ArticleModelForm(instance=article)

    context = {
        'form': form,
    }

    return render(request, 'articles/form.html', context)

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    
    return redirect('articles:detail', article.pk)