from django.http import JsonResponse
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
