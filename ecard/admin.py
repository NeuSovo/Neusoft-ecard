from django.contrib import admin
from .models import Ecard,Sessions
# Register your models here.
class SessionsAdmin(admin.ModelAdmin):
	list_display = ('rd_session','open_id','time')

class EcardAdmin(admin.ModelAdmin):
	list_display = ('wechat_key','ecard_key')

admin.site.register(Ecard,EcardAdmin)
admin.site.register(Sessions,SessionsAdmin)
