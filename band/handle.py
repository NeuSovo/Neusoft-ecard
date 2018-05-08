# -*- coding: utf-8 -*-
import logging
from band.models import BandOrder
from utils.exceptions import UpdateStatusError

app = logging.getLogger('app.custom')
class BandOrderHandle:
    def __init__(self, body, issue_user):
        self.order_id = body.get('order_id', None)
        self.issue_user = issue_user
        self.body = body

    def new_band(self):
        self.order_id = BandOrder().gen_orderid()
        new_band = BandOrder(order_id=self.order_id,
                             create_user=self.issue_user,
                             order_type=self.body.get('order_type', 0),
                             order_address=self.body.get('address', '无'),
                             order_name=self.body.get('order_name', '无'),
                             order_phone=self.body.get('order_phone','0'),
                             order_price=self.body.get('order_price', 0),
                             order_tip=self.body.get('order_tip',0),
                             content=self.body.get('content','无'))

        new_band.save()
        return {'message': 'ok',
                'order_id': self.order_id}

    def receive_band(self):
        band_o = BandOrder().get_order(self.order_id)
        if not band_o:
            return {'message': 'order_id Error'}

        try:
            band_o.update_order_status(2, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return {'message': 'ok', 'receive_time': band_o.receive_time}

    def confirm_band(self):
       band_o = BandOrder().get_order(self.order_id)
       if not band_o:
           return {'message': 'order_id Error'}

       try:
           band_o.update_order_status(1, self.issue_user)
       except UpdateStatusError as e:
           app.warn(str(e))
           return {'message': str(e)}
       return {'message': 'ok'}

    def done_band(self):
        band_o = BandOrder().get_order(self.order_id)
        if not band_o:
            return {'message': 'order_id Error'}

        try:
            band_o.update_order_status(0, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return {'message': 'ok', 'receive_time': band_o.done_time}

    def cancel_band(self):
        band_o = BandOrder().get_order(self.order_id)
        if not band_o:
            return {'message': 'order_id Error'}

        try:
            band_o.update_order_status(-1, self.issue_user)
        except UpdateStatusError as e:
            app.warn(str(e))
            return {'message': str(e)}
        return {'message': 'ok'}

    """
        个人下的单。 20
        所有待领取的单。 分页

        个人领取的单。20
    """

    # 个人下的单。
    def pp_band(self):
        info = []
        bindex = int(self.body.get('bindex', 0))
        band_pool = BandOrder.objects.filter(create_user=self.issue_user)[bindex:bindex + 20]
        for order in band_pool.iterator():
            info.append(order.complete_info())

        return {'message': 'ok', 'info': info, 'bindex': bindex + 20}

    # 个人领取的单。
    def pr_band(self):
        info = []
        bindex = int(self.body.get('bindex', 0))
        band_pool = BandOrder.objects.filter(receive_user=self.issue_user)[bindex:bindex + 20]
        for order in band_pool.iterator():
            info.append(order.complete_info())

        return {'message': 'ok', 'info': info, 'bindex': bindex + 20}

    # 所有待领取的单。 分页
    def ar_band(self):
       info = []
       bindex = int(self.body.get('bindex', 0))
       band_pool = BandOrder.objects.filter(order_status=3)[bindex:bindex + 20]
       for order in band_pool.iterator():
           info.append(order.simple_info())

       return {'message': 'ok', 'info': info, 'bindex': bindex + 20}
