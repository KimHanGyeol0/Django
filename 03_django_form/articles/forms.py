from django import forms
from .models import Article
# article을 저장하기 위한 새로운 폼
# 모델 구조와 비슷, forms가 가지고 있는 Form, models가 가지고 있는 Model
class ArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
    # yesorno = forms.BooleanField()
    # due_date = forms.DateTimeField()


# 모델폼, models의 모델을 바로 폼으로 만들어줌
class ArticleModelForm(forms.ModelForm):
    # 여기에서 model = Article하면 input으로 보기 때문에 meta 클래스에서 작업
    # Meta data : 데이터의 데이터, 어떠한 목적을 가지고 만들어진 데이터
    # title = form.CharField()이게 원래 생략되어 있음.
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력해주세요',
                'rows': 10,
            }
        )
    )
    # 이렇게 수정 가능
    class Meta():
        # 괄호 안해도 됨, Article 모델 자체
        # Article 모델 정보를 줄테니 알아서 만들어봐라
        model = Article
        fields = '__all__'

        # title만 폼 생성
        # fields = ['title']

        # title을 제외한 나머지
        # exclude = ['title']
