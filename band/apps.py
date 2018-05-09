from django.apps import AppConfig


class BandConfig(AppConfig):
    name = 'band'

class OrderStatusConfig:
    UnReceive  = 3
    Received = 2
    ToConfirm = 1
    Done = 0
    Cancel = -1

    @staticmethod
    def CodeToName(code):
        enum = ['Cancel', 'Done', 'ToConfirm', 'Received', 'UnReceive']
        try:
            return enum[int(code)+1]
        except IndexError:
            return 'undefined'
