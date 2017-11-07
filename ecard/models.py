from django.db import models
from datetime import datetime,timedelta
# Create your models here.
import django.utils.timezone as timezone
class Ecard(models.Model):
    wechat_key = models.CharField(max_length=100,unique=True,primary_key=True)
    ecard_key = models.CharField(max_length=50,default='NULL')

class Sessions(models.Model):
	rd_session = models.CharField(max_length=100)
	open_id = models.CharField(unique=True, max_length=100)
	sess_key = models.CharField(max_length=100)
	time = models.DateTimeFielddefault = timezone.now()

	class Meta:
	    unique_together = (('id', 'rd_session'),)