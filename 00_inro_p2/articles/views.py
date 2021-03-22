from django.shortcuts import render

# Create your views here.
# templates 폴더 안에 articles 폴더 생성 후에 index.html생성
# aticles 폴더 안의 index를 찾겠다.

def index(request):
    return render(request, 'articles/index.html')
