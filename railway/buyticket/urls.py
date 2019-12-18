from django.urls import path
from . import views

urlpatterns = [
    path('', views.buyticket, name='buyticket'),
    path('refund', views.refund_info, name='refund_info'),
]