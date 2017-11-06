from django.db import models
from datetime import datetime,timedelta
# Create your models here.
import django.utils.timezone as timezone
class Ecard(models.Model):
    wechat_key = models.CharField(max_length=100,unique=True,primary_key=True)
    ecard_key = models.CharField(max_length=50,default='NULL')

class Sessions(models.Model):
	rd_session = models.CharField(max_length=100,primary_key=True,unique=True)
	open_id = models.CharField(max_length=100,unique=True)
	sess_key = models.CharField(max_length=100)
	time =models.DateTimeField(default = timezone.now)