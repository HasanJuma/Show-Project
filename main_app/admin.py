from django.contrib import admin
from .models import Show, Rating, Comment


# Register your models here.
admin.site.register(Show)
admin.site.register(Rating)
admin.site.register(Comment)