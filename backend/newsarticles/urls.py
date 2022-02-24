from django.urls import path
from newsarticles import views

urlpatterns = [
    path('home/', views.read_articles, name="Home"),
    path('next', views.refreshcontent, name="Loadcontent"),
]