from django.contrib import admin

from django.contrib import admin
from .models import Huone, Valo, Tilaus

admin.site.register(Huone)
admin.site.register(Valo)
admin.site.register(Tilaus)
