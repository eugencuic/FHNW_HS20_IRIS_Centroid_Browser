from django.contrib import admin

# Register your models here.

from .models import Observation, Ypixels, CentroidCount

admin.site.register(Observation)
admin.site.register(Ypixels)
admin.site.register(CentroidCount)