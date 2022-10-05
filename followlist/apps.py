from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import send_activation_notification
user_registered = Signal()


def user_registered_dispatcher(sender, **kwargs):
    print(kwargs)
    send_activation_notification(kwargs['isinstance'])


user_registered.connect(user_registered_dispatcher)


class FollowlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'followlist'


