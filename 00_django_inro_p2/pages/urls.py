from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('DTL/', views.DTL, name='DTL'),
    path('question/', views.question, name='question'),
    path('answer/', views.answer, name='answer'),
    path('lotto/', views.lotto, name='lotto'),
    path('dinner/<str:menu>/<int:people>/', views.dinner, name='dinner'),
    path('lotto2/', views.lotto2, name='lotto2'),
    path('lotto_automatic/', views.lotto_automatic, name='lotto_automatic'),
    path('lotto_manual/', views.lotto_manual, name='lotto_manual'),
    path('lotto_buy/', views.lotto_buy, name='lotto_buy'),
]

# {% url pages:index %}
# 이렇게 명시해줄 것임