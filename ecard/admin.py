from django.contrib import admin

# Register your models here.

from ecard.models import *


class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    verbose_name = '用户信息'
    can_delete = True


class UserAdmin(admin.ModelAdmin):
	list_display = ('open_id', 'is_bind', 'last_login')

	inlines = (UserProfileAdmin,)


class EcardDetailAdmin(admin.ModelAdmin):
	list_display = ('detail_id','fssj','czlx','skdw','skck','jye')


admin.site.register(EcardDetail, EcardDetailAdmin)
admin.site.register(User, UserAdmin)
