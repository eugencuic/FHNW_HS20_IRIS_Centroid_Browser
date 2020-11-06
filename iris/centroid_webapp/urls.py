from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('centroids/', views.CentroidsListView.as_view(), name='centroids'),
]