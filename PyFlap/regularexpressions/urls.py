from django.urls import path

from . import views

urlpatterns = [
    path('', views.regex_page, name='regex_page'),
]