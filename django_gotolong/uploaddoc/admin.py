from django.contrib import admin

# Register your models here.

from .models import UploadDocModel

# ...
admin.site.register(UploadDocModel)
