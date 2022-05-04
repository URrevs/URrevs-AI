from django.urls import path
from . import views

urlpatterns = [
    path('reviews/grade', views.get_review_grade, name="review_grade"),
]