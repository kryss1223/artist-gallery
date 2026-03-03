from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path("", views.home, name="home"),
    path("artworks/", views.artworks_list, name="artworks_list"),
    path("artworks/<slug:slug>/", views.artwork_detail, name="artwork_detail"),
    path("series/", views.series_list, name="series_list"),
    path("series/<slug:slug>/", views.series_detail, name="series_detail"),
]