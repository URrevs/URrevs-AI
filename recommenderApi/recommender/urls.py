from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('phones/<str:phoneId>/recommend', views.get_similiar_phones, name="similiar_phones"),
    path('reviews/grade', views.get_review_grade, name="review_grade"),
    path('all/<str:userId>/recommend', views.get_reviews, name="reviews"),
]