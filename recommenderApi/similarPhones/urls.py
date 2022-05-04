from django.urls import path
from . import views

urlpatterns = [
    path('phones/<str:phoneId>/recommend', views.get_similiar_phones, name="similiar_phones"),
]