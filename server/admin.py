from django.contrib import admin

# Register your models here.
from .models import (Backup, Origin)
from .models.destination.LocalDestination import LocalDestination
from .models.destination.SFTPDestination import SFTPDestination

admin.site.register(Backup)
admin.site.register(Origin)
admin.site.register(LocalDestination)
admin.site.register(SFTPDestination)