from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Visit)
admin.site.register(BiasSetDefinition)
admin.site.register(BiasDefinition)
admin.site.register(Source)