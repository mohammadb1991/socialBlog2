from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import profilee , Relation


class profileeInline(admin.StackedInline):
    model = profilee
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (profileeInline,)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.register(Relation)