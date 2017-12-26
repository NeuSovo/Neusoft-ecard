from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^bind$',views.Bind),
    url(r'^balance$',views.getBalance),
    url(r'^detail$',views.getDetail),
    ]