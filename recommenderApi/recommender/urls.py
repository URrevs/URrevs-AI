from django.urls import path
from . import views

app_name = 'recommender'
urlpatterns = [
    path('', views.index, name='index'),
    path('all/<str:userId>/recommend', views.get_reviews, name="reviews"),
    path('html/all/<str:userId>/recommend', views.html_recommend, name="htmlreviews"),
    path('phones/<str:phoneId>/recommend', views.get_similiar_phones, name="similiar_phones"),
    path('reviews/grade', views.get_review_grade, name="review_grade")
]