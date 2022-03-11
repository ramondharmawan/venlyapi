from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_test', views.submit_test, name='submit_test'),
]