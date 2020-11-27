from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('observations/<int:centroid>&<int:observation>', views.list_view, name='list_view'),
]

