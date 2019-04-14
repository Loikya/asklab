from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    avatar_image = models.ImageField(default="default.svg", blank=True)
    age = models.IntegerField(null=True, blank=True)
    liked_by = models.ManyToManyField('questions.Question', related_name='liked_by', blank=True, null=True, default=None)
    disliked_by = models.ManyToManyField('questions.Question', related_name='disliked_by', blank=True, null=True, default=None)
    liked_by_answ = models.ManyToManyField('answers.Answer', related_name='liked_by_answ', blank=True, null=True, default=None)
    disliked_by_answ = models.ManyToManyField('answers.Answer', related_name='disliked_by_answ', blank=True, null=True, default=None)

    def __str__(self):
      return self.user.username


@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        UserProfileInfo.objects.create(user=instance)
    instance.profile.save()