from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.pw_update, name='pw_update'),
    # 이게 위에 있으면 경로가 오면서 다 걸림, delete가 username으로 인식
    # 아니면 profile/<str:username>으로 해야함
    path('<str:username>/', views.profile, name='profile'),
]
