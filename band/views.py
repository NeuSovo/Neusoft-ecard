from django.http import JsonResponse, HttpResponse
from band.handle import BandOrderHandle

from utils.auth import usercheck
# Create your views here.


@usercheck()
def bindorder_view(request, action=None, body=None, user=None):
    response = ''
    band = BandOrderHandle(body=body, issue_user=user)

    try:
        method_name = action + '_band'
        result = getattr(band, method_name)
    except AttributeError as e:
        response = HttpResponse()
        response.status_code = 404
        return response

    response = JsonResponse(result())
    return response


def get_order_status(request):
    body = {}
    body['bindex'] = request.GET.get('bindex', 0)
    body['exp'] = request.GET.get('exp', 1)
    band = BandOrderHandle(body=body)
    res = band.ar_band()

    return JsonResponse(res)
