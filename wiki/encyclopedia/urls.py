from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new_page/", views.new_page, name="new_page"),
    path("wiki/save_entry/", views.save_entry, name="save_entry"),
    path("wiki/<str:title>/", views.wiki_page, name="wiki_page"),
    path("wiki/random_page", views.random_page, name="random_page"),


]
