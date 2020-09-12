from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jpy_add/', views.jpy_kinri_add, name='jpy_kinri_add'),
]

