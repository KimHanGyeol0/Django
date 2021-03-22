from django.shortcuts import render

# Create your views here.
def index(request):
    lunch = [
        '짜장면',
        '탕수육',
        '짬뽕',
    ]
    context = {
        'lunch' : lunch,
    }
    return render(request, 'index.html', context)

def ping(request):
    return render(request, 'ping.html')

def pong(request):
    user_id = request.GET.get('id')
    user_pw = request.GET.get('pw')
    context = {
        'user_id': user_id
    }
    return render(request, 'pong.html', context)

def detail(request, num):
    articles = [
        '게시물 1',
        '게시물 2',
        '게시물 3',
    ]
    result = articles[num-1]
    context = {
        'result': result
    }
    return render(request, 'detail.html', context)