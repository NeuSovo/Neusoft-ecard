import random
from datetime import datetime,timedelta
from django.db import models
from utils.models import User
from utils.exceptions import UpdateStatusError
# Create your models here.

class BandOrder(models.Model):

    class Meta:
        verbose_name = "帮带订单"
        verbose_name_plural = "帮带订单"
        ordering = ['-create_time']

    max_cancel_time = timedelta(minutes=15)

    order_type_choices = (
        (0, '快递'),
        (1, '商品/餐饮')
    )

    ## 订单状态只能从上递减至0，严格层级控制
    #  当且仅当状态为3时才可跳至-1
    # -1 状态发起者 发起User
    #  0 状态发起者 发起User
    #  1 状态发起者 领取User
    #  2 状态发起者 领取User
    #  3 状态发起者 发起User
    # 
    order_status_choices = (
        (-1, '已取消'),
        (0, '已完成'),
        (1, '待确认'),
        (2, '已领取'),
        (3, '待领取'),
    )

    def update_order_status(self, status=None, issue_user=None):
        if (status or issue_user) and (not isinstance(issue_user, User)):
            raise UpdateStatusError(self.order_status, status, issue_user)

        if status == 2:
            if self.order_status != 3:
                raise UpdateStatusError(self.order_status, status)

            if issue_user == self.create_user:
                # raise UpdateStatusError(self.order_status, status, issue_user)
                pass
            self.receive_user = issue_user
            self.receive_time = datetime.now()

        if status == 1:
            if self.order_status != 2:
                raise UpdateStatusError(self.order_status, status)

            if issue_user == self.receive_user:
                pass
            else:
                raise UpdateStatusError(self.order_status, status, issue_user)

        if status == 0:
            if self.order_status != 1:
                raise UpdateStatusError(self.order_status, status)

            if issue_user == self.create_user:
                self.done_time = datetime.now()
            else:
                raise UpdateStatusError(self.order_status, status, issue_user)

        if status == -1:
            if self.order_status != 3:
                raise UpdateStatusError(self.order_status, status)

            if datetime.now() - self.create_time > self.max_cancel_time:
                return {'message': 'Expire Max Cancel Time'}

        self.order_status = status
        self.save()
        return {'message': 'ok'}

    def simple_info(self):
        return {'order_id': str(self.order_id),
                'order_type': self.order_type,
                'order_status': self.order_status,
                'create_user': str(self.create_user),
                'create_time': str(self.create_time),
                'order_price': str(self.order_price),
                'order_tip': self.order_tip,
                'order_address': self.order_address,
                }

    def complete_info(self):
        return dict({
                'order_name': self.order_name,
                'order_phone': self.order_phone,
                'content': self.content
            },**self.simple_info())

    order_id = models.BigIntegerField(
        primary_key=True
    )

    create_time = models.DateTimeField(
        auto_now_add=True
    )

    order_type = models.IntegerField(
        default=0,
        choices=order_type_choices
    )

    order_status = models.IntegerField(
        default=3,
        choices=order_status_choices
    )

    create_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='create_user'
    )

    order_address = models.CharField(
        max_length=155,
    )

    order_name = models.CharField(
        max_length=30,
    )

    order_phone = models.CharField(
        max_length=12,
    )

    receive_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='receive_user'
    )

    receive_time = models.DateTimeField(
        null=True,
        blank=True
    )

    done_time = models.DateTimeField(
        null=True,
        blank=True
    )

    order_price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    order_tip = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    content = models.TextField(
        blank=True,
        null=True
    )


    @staticmethod
    def gen_orderid():
        order_id = datetime.now().strftime("%Y%m%d%H%M%S") + \
            str(random.randint(1000, 9999))

        return order_id

    @staticmethod
    def get_order(order_id):
        try:
            order = BandOrder.objects.get(order_id=order_id)
        except Models.DoesNotExist:
            order = None
        return order
