# forms.py
from django import forms
from .models import Answer

class AnswerAddForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)

    def __init__(self, *args, **kwargs):
        super(AnswerAddForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Введите текст ответа"