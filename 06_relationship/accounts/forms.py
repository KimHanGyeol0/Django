from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        # 현재의 유저를 가져오겠다. 대체된 유제모델을 가져오겠다.
        model = get_user_model()
        # 원래 있던 필드 + 추가하고 싶은 필드(유저 모델에 있는 필드를 써야 한다.)
        fields = UserCreationForm.Meta.fields + ('email',)