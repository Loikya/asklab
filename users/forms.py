from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField(required=False)
    avatar_image = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar_image', 'age')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['avatar_image'].label = "Изображение профиля"
        self.fields['age'].label = "Возраст"