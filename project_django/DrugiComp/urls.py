from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='DrugiComp-home'),
    path('about/', views.about, name='DrugiComp-about'),
    path('statistics/', views.statistics, name='DrugiComp-statistics'),
    path('test/', views.test, name='DrugiComp-test'),
    path('admin_page/', views.admin_page, name='DrugiComp-admin_page'),
    path('add_ds/', views.add_ds, name='DrugiComp-add_ds'),
    path('remove_dsi/', views.remove_dsi, name='DrugiComp-remove_dsi'),
    path('modify_dsi/', views.modify_dsi, name='DrugiComp-modify_dsi'),
    path('view_database/', views.view_database, name='DrugiComp-view_database'),
    path('add_int_foodint/', views.add_int_foodint, name='DrugiComp-add_int_foodint'),
    path('admin_login/', views.admin_login, name='DrugiComp-admin_login'),
]
