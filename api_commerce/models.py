from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


# Create your models here.


class Note(models.Model):
    note_name = models.CharField(max_length=100)
    note_description = models.CharField(max_length=250)
    note_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.note_name}  ---- {self.note_user.username}"

    class Meta:
        verbose_name_plural = 'Note'


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)