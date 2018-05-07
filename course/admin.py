from django.contrib import admin
from course.models import RoomTest
# Register your models here.

class FloorFilter(admin.SimpleListFilter):
    title = u'楼宇'
    parameter_name = 'floor'

    def lookups(self, request=None, model_admin=None):
        return (
            ('A1', u'A1'),
            ('A2', u'A2'),
            ('A3', u'A3'),
            ('A5', u'A5'),
            ('A6', u'A6'),
            ('A7', u'A7'),
            ('健美操教室', u'健美操教室'),
            ('体育馆', u'体育馆'),
            ('三期运动场',u'三期运动场'),
            ('三期网球场',u'三期网球场')
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(RoomID__startswith=self.value())
        else:
            return queryset.all()


class RoomAdmin(admin.ModelAdmin):
    '''
        Admin View for Room
    '''
    list_display = ('RoomID','ClassName', 'ClassTeacher', 'ClassWeek', 'ClassTimeWeek', 'ClassTimeTime')
    list_filter = (FloorFilter, 'ClassTimeWeek', 'ClassTimeTime',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('ClassTeacher', 'ClassName', 'ClassGrade')

admin.site.register(RoomTest, RoomAdmin)