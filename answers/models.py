from django.db import models
from django.conf import  settings
from ckeditor.fields import RichTextField

# Create your models here.


class Answer(models.Model):

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', related_name='answers', on_delete=models.CASCADE)
    text = RichTextField(verbose_name="Текст ответа")
    date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:50]

    class Meta:
        ordering = ['-date']