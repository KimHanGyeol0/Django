from django.urls import path
from . import views

app_nam = 'articles'
urlpatterns = [
    path('index/', views.index, name='index'),
]
