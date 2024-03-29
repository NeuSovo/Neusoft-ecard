from django.db import models

# Create your models here.


class RoomModel(models.Model):

    class Meta:
        verbose_name = "RoomModel"
        verbose_name_plural = "RoomModels"

    def info(self):
        result = {
            'RoomID': self.RoomID,
            'RoomTime': self.RoomTime,
            'RoomWeek': self.RoomWeek,
            'ClassName': self.ClassName,
            'ClassTeacher': self.ClassTeacher,
            'ClassTime': self.ClassTime,
            'RoomCount': self.RoomCount
        }

    RoomFloor = models.CharField(
        max_length=10
    )
    RoomID = models.CharField(
        max_length=30
    )
    RoomTime = models.IntegerField(
        default=0
    )
    RoomWeek = models.IntegerField(
        default=0
    )
    ClassName = models.CharField(
        max_length=155,
    )
    ClassTeacher = models.CharField(
        max_length=155,
    )
    ClassTime = models.CharField(
        max_length=100,
    )
    RoomCount = models.IntegerField(
        default=0
    )


class RoomTest(models.Model):
    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = "课程信息"
        ordering = ['id']

    def info(self, has_grade=False):
        result = {
            'RoomID': self.RoomID,
            'ClassName': self.ClassName,
            'ClassTeacher': self.ClassTeacher,
            'ClassWeek': self.ClassWeek,
            'ClassCount': self.ClassCount,
            'ClassTimeWeek': self.ClassTimeWeek,
            'ClassTimeTime': self.ClassTimeTime
        }
        if has_grade:
            result['ClassGrade'] = self.ClassGrade
        return result

    ClassTimeTime_choices = (
        ('1', '1-2节'),
        ('2', '3-4节'),
        ('3', '5-6节'),
        ('4', '7-8节'),
        ('5', '9-10节'),
        ('5', '9-11节'),
        ('1-2', '1-4节'),
        ('1-2-3-4', '1-8节'),
        ('3-4', '5-7节'),
        ('3-4', '5-8节'),
        ('1-2-3-4', '1-8节'),
        ('1-2-3-4-5', '1-10节'),
        ('1-2-3-4-5', '1-11节'),
    )

    ClassTimeWeek_choices = (
        (1, '周一'),
        (2, '周二'),
        (3, '周三'),
        (4, '周四'),
        (5, '周五'),
        (6, '周六'),
        (7, '周日'),
    )

    RoomID = models.CharField(
        max_length=30,
        null=True
    )

    ClassName = models.CharField(
        max_length=155,
        null=True
    )

    ClassTeacher = models.CharField(
        max_length=120,
        null=True,
        default='0'
    )

    ClassWeek = models.CharField(
        max_length=30,
        null=True
    )

    ClassCount = models.IntegerField(default=0)

    ClassGrade = models.TextField(
        default='0',
        null=True
    )

    ClassTimeWeek = models.IntegerField(
        default=0, choices=ClassTimeWeek_choices)

    ClassTimeTime = models.CharField(
        default='0',
        max_length=10,
        choices=ClassTimeTime_choices,
        null=True
    )
