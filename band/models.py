import random
from datetime import datetime,timedelta
from django.db import models
from utils.models import User
from band.exceptions import UpdateStatusError
from band.apps import OrderStatusConfig as OSC
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
    
    ## 
    # 订单状态只能从上递减至0，严格层级控制
    #  当且仅当状态为3时才可跳至-1
    #  3 -> 2 -> 1 -> 0
    #  ↓
    # -1
    # =========================
    # -1 状态发起者 create_user
    #  0 状态发起者 create_user
    #  1 状态发起者 receive_user
    #  2 状态发起者 receive_user
    #  3 状态发起者 create_user
    # 
    order_status_choices = (
        (OSC.Cancel, '已取消'),
        (OSC.Done, '已完成'),
        (OSC.ToConfirm, '待确认'),
        (OSC.Received, '已领取'),
        (OSC.UnReceive, '待领取'),
    )

    def update_order_status(self, to_status=None, issue_user=None):
        if (to_status or issue_user) and (not isinstance(issue_user, User)):
            raise UpdateStatusError(self.order_status, to_status, issue_user)

        if to_status == OSC.Received:
            if self.order_status != OSC.UnReceive:
                raise UpdateStatusError(self.order_status, to_status)

            if issue_user == self.create_user:
                # raise UpdateStatusError(self.order_status, to_status, issue_user)
                pass
            self.receive_user = issue_user
            self.receive_time = datetime.now()

        if to_status == OSC.ToConfirm:
            if self.order_status != OSC.Received:
                raise UpdateStatusError(self.order_status, to_status)

            if issue_user == self.receive_user:
                pass
            else:
                raise UpdateStatusError(self.order_status, to_status, issue_user)

        if to_status == OSC.Done:
            if self.order_status != OSC.ToConfirm:
                raise UpdateStatusError(self.order_status, to_status)

            if issue_user == self.create_user:
                self.done_time = datetime.now()
            else:
                raise UpdateStatusError(self.order_status, to_status, issue_user)

        if to_status == OSC.Cancel:
            if self.order_status != OSC.UnReceive:
                raise UpdateStatusError(self.order_status, to_status)
                
            if issue_user != self.create_user:
                raise UpdateStatusError(self.order_status, to_status, issue_user)

            if datetime.now() - self.create_time > self.max_cancel_time:
                return {'message': 'Expire Max Cancel Time'}

        self.order_status = to_status
        self.save()
        return {'message': 'ok'}

    def simple_info(self):
        return {'order_id': str(self.order_id),
                'order_type': self.order_type,
                'order_status': self.order_status,
                'create_user': str(self.create_user.name),
                'avatar_links': str(self.create_user.link),
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
