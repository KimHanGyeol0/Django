from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    # 업데이트할 게시물을 보여주는 화면
    path('<int:pk>/edit/', views.edit, name='edit'),
    # 수정 화면
    path('<int:pk>/upadate/', views.update, name='update'),
]
