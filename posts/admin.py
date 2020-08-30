from django.contrib import admin
from .models import post,Comment,Voted

admin.site.register(post)
admin.site.register(Comment)
admin.site.register(Voted)

# Register your models here.
