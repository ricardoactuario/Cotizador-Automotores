from django.urls import path
from . import views

urlpatterns = [
    path('SegurodeAutomotores/', views.CotizadorA, name='SA'),
]