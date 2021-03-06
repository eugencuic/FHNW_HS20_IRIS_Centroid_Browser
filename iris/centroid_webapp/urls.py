from django.urls import path
from . import views

# Definition of URL Pattern in order to be able to construct the url in the HTML templates and request data from models via View
urlpatterns = [
    path('', views.index, name='index'),
    path('observations/<int:centroid>&<int:observation>&<int:image_choice>&<int:step>', views.list_view, name='list_view'),
    path('myplot/<int:centroid>&<int:observation>&<int:image_choice>&<int:step>', views.plot_png, name='myplot'),

]

