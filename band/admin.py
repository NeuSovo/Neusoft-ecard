from django.contrib import admin
from band.models import BandOrder
# Register your models here.


class BandOrderAdmin(admin.ModelAdmin):
    '''
        Admin View for BandOrder
    '''
    list_display = ('create_time', 'order_type', 'order_status', 'create_user', 'receive_time', 'order_tip', 'done_time')
    list_filter = ('order_type', 'order_status')
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('order_id', 'create_time', 'create_user')
    # search_fields = ('',)

admin.site.register(BandOrder, BandOrderAdmin)