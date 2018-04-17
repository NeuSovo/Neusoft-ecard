from django.db import models

# Create your models here.

class RoomModel(models.Model):

    class Meta:
        verbose_name = "RoomModel"
        verbose_name_plural = "RoomModels"

    def info(self):
        return {
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
        default = 0
    )


class RoomTest(models.Model):

    class Meta:
        verbose_name = "RoomTest"
        verbose_name_plural = "RoomTests"
    def info(self):
        return {
            'RoomID': self.RoomID,
            'ClassName': self.ClassName,
            'ClassTeacher': self.ClassTeacher,
            'ClassWeek': self.ClassWeek,
            'ClassCount': self.ClassCount,
            'ClassTimeWeek': self.ClassTimeWeek,
            'ClassTimeTime': self.ClassTimeTime
        }
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
        null=True
    )

    ClassWeek = models.CharField(
        max_length=30,
        null=True
    )

    ClassCount = models.IntegerField(default=0)

    ClassGrade = models.TextField(
        default='',
        null=True
    )

    ClassTimeWeek = models.IntegerField(default=0)

    ClassTimeTime = models.CharField(
        default='0',
        max_length=10,
        null=True
    )
