from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    bind_level = (
        (0, '未绑定'),
        (1, '已绑定')
    )
    open_id = models.CharField(
        max_length=100,
        primary_key=True,
        null=False)
    is_bind = models.IntegerField(
        default=0,
        choices=bind_level
        )

    reg_date = models.DateTimeField(
        auto_now_add=True
        )
    last_login = models.DateTimeField(
        default=timezone.now
        )

    class Meta:
        ordering = ['-last_login']

    def __str__(self):
        return u'%s' % (self.open_id)

