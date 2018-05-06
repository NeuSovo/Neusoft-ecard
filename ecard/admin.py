from django.contrib import admin

# Register your models here.

from ecard.models import *



class EcardProfileAdmin(admin.ModelAdmin):
    list_display = ('open_id', 'ecard_key', 'name', 'subject', 'grade')



admin.site.register(EcardProfile, EcardProfileAdmin)
