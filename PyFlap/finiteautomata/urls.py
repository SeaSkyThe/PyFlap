from django.urls import path

from . import views


urlpatterns = [
    path('', views.fa_page, name='fa_page'),
]