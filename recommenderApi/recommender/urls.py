from django.urls import path
from . import views

app_name = 'recommender'
urlpatterns = [
    path('', views.index, name='index'),
    path('all/default/recommend', views.get_anonymous_recommendations, name="anonymous_recommendations"),
    path('all/<str:userId>/recommend', views.get_recommendations, name="recommendations"),
    path('phones/<str:phoneId>/recommend', views.get_similiar_phones, name="similiar_phones"),
    path('reviews/grade', views.get_review_grade, name="review_grade"),
    path('training/start', views.start_training, name="start_training"),
    path('training/services/stop', views.stop_training, name="stop_training"),
    path('training/reset', views.reset_files, name="reset_files"),
]