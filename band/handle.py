# -*- coding: utf-8 -*-
import logging
from band.models import BandOrder
from band.exceptions import UpdateStatusError
from band.apps import OrderStatusConfig as OSC
from datetime import timedelta, datetime
app = logging.getLogger('app.custom')


class BandOrderHandle:
    def __init__(self, body, issue_user):
        self.order_id = body.get('order_id', None)
        self.band_o = BandOrder().get_order(self.order_id)
        self.issue_user = issue_user
        self.body = body

    def new_band(self):
        self.order_id = BandOrder().gen_orderid()
        new_band = BandOrder(order_id=self.order_id,
                             create_user=self.issue_user,
                             order_type=self.body.get('order_type', 0),
                             order_address=self.body.get('order_address', ''),
                             order_name=self.body.get('order_name', ''),
                             order_phone=self.body.get('order_phone', '0'),
                             order_price=self.body.get('order_price', 0),
                             order_tip=self.body.get('order_tip', 0),
                             content=self.body.get('content', ''))

        new_band.save()
        return {'message': 'ok',
                'order_id': self.order_id,
                'expire_time': self.extend_band()}

    def extend_band(self, exprie_hours=2, max_extend_minutes=30):
        """
        expire_time_hours default = 2
        based on datetimenow+timedelta(expire_time_hours)
        """
        if self.band_o:
            self.band_o.expire_time = datetime.now() + timedelta(hours=exprie_hours)
            self.band_o.save()
            return self.band_o.expire_time
        else:
            if int(self.band_o.expire_time - datetime.now()) < timedelta(minutes=max_extend_minutes):
                self.band_o.expire_time = datetime.now() + timedelta(hours=exprie_hours)
            else:
                return {'message': '还没到最低续期时间，再等等吧'}

        self.band_o.save()
        return {'message': 'ok',
                'expire_time': self.band_o.expire_time}

    def receive_band(self):
        self.band_o = BandOrder().get_order(self.order_id)
        if not self.band_o:
            return {'message': '订单号错误'}

        try:
            self.band_o.update_order_status(OSC.Received, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return {'message': 'ok', 'receive_time': self.band_o.receive_time}

    def confirm_band(self):
        self.band_o = BandOrder().get_order(self.order_id)
        if not self.band_o:
            return {'message': '订单号错误'}

        try:
            self.band_o.update_order_status(OSC.ToConfirm, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return {'message': 'ok'}

    def done_band(self):
        self.band_o = BandOrder().get_order(self.order_id)
        if not self.band_o:
            return {'message': '订单号错误'}

        try:
            self.band_o.update_order_status(OSC.Done, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return {'message': 'ok', 'receive_time': self.band_o.done_time}

    def cancel_band(self):
        self.band_o = BandOrder().get_order(self.order_id)
        if not self.band_o:
            return {'message': '订单号错误'}

        try:
            info = self.band_o.update_order_status(OSC.Cancel, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return info
    """
        个人下的单。 20
        所有待领取的单。 分页

        个人领取的单。20
    """

    # 个人下的单。
    def pp_band(self):
        info = []
        bindex = int(self.body.get('bindex', 0))
        band_pool = BandOrder.objects.filter(create_user=self.issue_user)[
            bindex:bindex + 20]
        for order in band_pool.iterator():
            info.append(order.complete_info())

        return {'message': 'ok', 'info': info, 'bindex': len(band_pool)}

    # 个人领取的单。
    def pr_band(self):
        info = []
        bindex = int(self.body.get('bindex', 0))
        band_pool = BandOrder.objects.filter(receive_user=self.issue_user)[
            bindex:bindex + 20]
        for order in band_pool.iterator():
            info.append(order.complete_info())

        return {'message': 'ok', 'info': info, 'bindex': len(band_pool)}

    # 所有待领取的单。 分页
    def ar_band(self):
        info = []
        bindex = int(self.body.get('bindex', 0))
        band_pool = BandOrder.objects.filter(order_status=OSC.UnReceive, expire_time__lte=datetime.now())[
            bindex:bindex + 20]
        for order in band_pool.iterator():
            info.append(order.simple_info())

        return {'message': 'ok', 'info': info, 'bindex': len(band_pool)}
