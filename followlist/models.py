from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class SimpleUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    email = models.EmailField(unique=True)
    first_name = None
    last_name = None
    last_login = None
    date_joined = None

    class Meta(AbstractUser.Meta):
        pass


class TypeList(models.Model):
    name_type = models.CharField(max_length=16)

    def __str__(self):
        return self.name_type


class List(models.Model):
    name_list = models.CharField(max_length=100)
    is_private = models.BooleanField(default=True)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    original_id = models.IntegerField(null=True, default=-1)
    type = models.ForeignKey(TypeList, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name_list


class Points(models.Model):
    name_point = models.CharField(max_length=100)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.name_point


class Goal(models.Model):
    name_goal = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_goal


def save_list_dispatcher(sender, **kwargs):
    if kwargs['created']:
        pass

post_save.connect(save_list_dispatcher, sender=List)

