
from .Backup import Backup
from .Origin import Origin

from .destination.BaseDestination  import BaseDestination
from .destination.LocalDestination import LocalDestination
from .destination.SFTPDestination  import SFTPDestination
from .destination.APIDestination   import APIDestination


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

