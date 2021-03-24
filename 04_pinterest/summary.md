# Project Summary

* 2021.03.24 relatonship 추가

### 모델 및 폼 생성

```python
# models.py
class Comment(models.Model):
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
```

* 모델 생성하고 forms.py에서 댓글 입력할 모델폼 생성

```python
# views.py
def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)
```

* 만든 폼을 detail 페이지에 보여줌



### 댓글 생성

```python
# views.py
@require_POST
def comment_create(request, post_pk):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(pk=post_pk)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('posts:detail', post.pk)
    
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)
```

* .save(commit=False)
  * db에 저장은 하지 말고 인스턴스로만 만들어라
  * 모델에 content와 post를 넣어야 되는데 post를 아직 안넣었다
  * 넣고 저장하기 위해서
* 모델이름_set.all()
  * 역참조, 1에서 N을 참조
  * post.comment_set.all()

### 댓글 삭제

* path
  * `path('<int:post_pk>/comments/<int:comment_pk>/delete', views.comment_delete, name='comment_delete'),`
  * 삭제하고 돌아갈 post_pk와 삭제할 댓글의 pk 같이 보내줌

```python
# views.py
@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('posts:detail', post_pk)
```

* 삭제하고 다시 원래 페이지로 돌아감

### 유저 : Post (1:N)

```python
from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

* models.py에서 외래키 만들어서 모델 수정

```python
if form.is_valid():
    post = form.save(commit=False)
    post.user = request.user
    post.save()
```

* views.py에서 user 넣고 저장

```html
{% extends 'base.html' %}
{% block content %}
  <h1>{{ user_info.username }}님의 프로필</h1>
  <div class="row row-cols-1 row-cols-md-3 g-4">
    {% for post in user_info.post_set.all %}
    <div class="col">
      {% include 'posts/_card.html' %}
    </div>
    {% endfor %}
  </div>
{% endblock  %}
```

* 프로필에 이 유저가 만든 게시물 보여주기

```html
{# detail.html #}
<p>작성자 : <a href="{% url 'accounts:profile' post.user.pk %}">{{ post.user.username }}</a></p>
```

* 작성자 profile로 들어가기
* user.pk로 하면 현재 로그인하고 있는(현재 보고 있는 사람)의 pk



### 유저 : 댓글 (1:N)

* 댓글마다 작성자 표시

1. DB와 모델 초기화
2. comment 모델에 유저 추가
3. comment 생성 시 현재 user 같이 저장
4. detail에 출력

```python
class Comment(models.Model):
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

* comment 모델에 유저 외래키 추가

```python
# posts view.py
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
```

* 현재 user 넣고 저장

```html
  <ul>
  {% for comment in post.comment_set.all %}
    <li>{{ comment.content }} 작성자 : {{ comment.user.username }}</li>
    <form action="{% url 'posts:comment_delete' post.pk comment.pk%}" method="POST">
      {% csrf_token %}
      <input type="submit" value="삭제">
    </form>
  {% endfor %}
  </ul>
```

* comment의 user의 username 같이 출력