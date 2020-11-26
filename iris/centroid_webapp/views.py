from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels

import os

from plotly.offline import plot
import plotly.graph_objects as go

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

def list_view(request, centroid, observation):
    observation_list = CentroidCount.objects.filter(centroid__in=[centroid]).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    plot_graph = examplePlot(centroid, observation)
    
    return render(request, 'centroid_webapp/observation_list.html', context={
                                                                            'observation_list' : observation_list, 
                                                                            'centroid':centroid, 
                                                                            'observation':observation, 
                                                                            'plot_graph':plot_graph
                                                                            })

def examplePlot(centroid, observation):
    # Makes a simple plotly plot, and returns html to be included in template.
    x = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('step', flat=True))
    y = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('count', flat=True))
    y.insert(0, 0)
    y.append(0)
    x.insert(0, 0)
    
    if not list(CentroidCount.objects.filter(id_observation=observation).values_list('step', flat=True)):
        x_max=1
    else:
        x_max = max(list(CentroidCount.objects.filter(id_observation=observation).values_list('step', flat=True)))

    x.insert(len(x),(x_max+1))
    
    scatter = go.Scatter(
                    x=x, 
                    y=y, 
                    mode='lines+markers', 
                    line = dict(shape = 'spline', color = 'rgb(205, 12, 24)', width= 2),
                    marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 4),
                    name='test', 
                    opacity=0.8, 
                    marker_color='green',
                    connectgaps = True
                    )

    layout = go.Layout(
                    title='Appearances for Centroids', 
                    xaxis=dict(
                        range=([0,x_max]),
                        title='Step',
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    
                    yaxis={
                        'title':'occurences'
                        }
                    )
    
    data = [scatter]
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_div