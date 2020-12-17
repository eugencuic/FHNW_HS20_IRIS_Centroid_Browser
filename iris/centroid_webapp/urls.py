from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myplot/', views.plot_png, name='myplot'),
    path('observations/<int:centroid>&<int:observation>&<int:image_choice>&<int:step>', views.list_view, name='list_view'),

]

