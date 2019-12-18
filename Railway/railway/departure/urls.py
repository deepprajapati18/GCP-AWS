from django.urls import path
from . import views

urlpatterns = [
    path('set', views.settime, name='settime'),
    path('info', views.ticketinfo, name='ticketinfo'),
    path('depart', views.depart, name='depart'),
]