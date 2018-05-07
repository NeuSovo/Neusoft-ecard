from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from utils.models import User
# Create your models here.

class EcardProfile(models.Model):
    class Meta:
        verbose_name = "卡片信息"
        verbose_name_plural = "卡片信息"

    open_id = models.OneToOneField(
                User,
                on_delete=models.CASCADE,
                primary_key=True
            )
    ecard_key  = models.CharField(
        max_length=30,
        default='NULL'
        )
    name = models.CharField(
    	max_length=100,
    	default='NULL'
    	)
    subject = models.CharField(
    	max_length=100,
    	default='NULL')
    grade = models.CharField(
		max_length=30,
		default='NULL')


class EcardDetail(models.Model):
    ecard_key = models.CharField(
        max_length=30,
        )
    detail_id = models.IntegerField(
        verbose_name='交易id'
        )
    fssj = models.DateTimeField(
        verbose_name='发生时间'
        )
    czlx = models.CharField(
        max_length=100,
        verbose_name='操作类型'
        )
    skdw = models.CharField(
        max_length=100,
        verbose_name='收款单位'
        )
    skck = models.CharField(
        max_length=100,
        verbose_name='收款窗口'
        )
    jye = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='交易额'
        )
    knye = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='卡内余额'
        )
    jzsj = models.DateTimeField(
        verbose_name='记账时间'
        )
