"""neusoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecard.views import card_view
from utils.views import login_view,register_view, profile_view
from course.views import room_view
from band.views import bindorder_view, get_order_status
urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/reg', register_view),
    path('auth/login', login_view),

    path('user/profile/<str:action>', profile_view),
    path('user/card/<str:action>', card_view),

    path('user/course/<str:action>', room_view),# er: empty_room

    path('user/band/a', get_order_status),
    path('user/band/<str:action>', bindorder_view), # new, receive, confirm. get, all
]
