from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^empty$',views.get_empty_class),
    url(r'^rubc$',views.rub_class),
    url(r'^rubt$',views.rub_teachter),
    ]