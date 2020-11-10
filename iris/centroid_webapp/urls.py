from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.CentroidListView.as_view(), name='centroids'),
    path('<int:pk>', views.CentroidDetailView.as_view(), name='centroid-detail'),
]
