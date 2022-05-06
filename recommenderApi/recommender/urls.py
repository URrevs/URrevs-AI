from django.urls import path
from . import views

app_name = 'recommender'
urlpatterns = [
    path('', views.index, name="index"),
    path('all/<str:userId>/recommend', views.get_reviews, name="reviews"),
    path('html/all/<str:userId>/recommend', views.html_recommend, name="htmlreviews"),
]