from django.urls import path

from . import views

urlpatterns = [
    path('', views.grammars_page, name='grammars_page'),
]