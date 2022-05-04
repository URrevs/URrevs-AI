from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('all/<str:userId>/recommend', views.get_reviews, name="reviews"),
]