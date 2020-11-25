from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels
from django.views import generic
from centroid_webapp.forms import CentroidForm
import os
from plotly.offline import plot
from plotly.graph_objects import Scatter


# TODO use this function to return list of observations to create list 
# CentroidCount.objects.filter(centroid__in=[...id,id,...]).order_by('id_observation').values_list('id_observation', flat=True).distinct()
# 

def index(request):


    """View function for homepage of site."""

    # Generate counts of some of the main objects
    num_centroids = 52
    num_observations = 3358
    num_timestepoberservations = 2324582
    image_numbers = [i for i in range(1,54)]



    context = {
        'num_centroids': num_centroids,
        'num_observations': num_observations,
        'num_timestepoberservations' : num_timestepoberservations,
        'images_num': image_numbers

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def list_view(request, centroid, observation, image):
    try:
        observation_list = CentroidCount.objects.filter(centroid__in=[centroid]).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    except observation_list.DoesNotExists:
        raise Http404('Observation does not exist')
    
    centroid = centroid
    observation = observation
    image = image

    x_axis_steps = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('step', flat=True))
    y_axis_count = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('count', flat=True))

    plot_div = plot([Scatter(x=x_axis_steps, y=y_axis_count,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')


    return render(request, 'centroid_webapp/observation_list.html', context={'observation_list' : observation_list, 
                                                                            'centroid':centroid, 
                                                                            'observation':observation, 
                                                                            'image':image,
                                                                            'plot_div':plot_div})


