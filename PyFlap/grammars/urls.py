from django.urls import path

from . import views

urlpatterns = [
    path('', views.grammars_page, name='grammars_page'),
    path('delete_rule/<int:id>', views.delete_rule, name="delete_rule"),
    path('delete_all_rules/', views.delete_all_rules, name="delete_all_rules"),
    
]