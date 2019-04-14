from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django import forms


# Create your models here.

def default_empty():
    return None

class Question(models.Model):

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_questions')
    title = models.CharField(max_length=255, verbose_name="Заголовок вопроса")
    description = models.CharField(max_length=350, verbose_name="Описание вопроса")
    text = RichTextField(verbose_name="Текст вопроса")
    date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'
