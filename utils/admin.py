from django.contrib import admin

# Register your models here.
from utils.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('open_id', 'is_bind', 'reg_date', 'last_login')

admin.site.register(User, UserAdmin)