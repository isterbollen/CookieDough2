from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='DrugiComp-home'),
    path('about/', views.about, name='DrugiComp-about'),
    path('statistics/', views.statistics, name='DrugiComp-statistics'),
]
