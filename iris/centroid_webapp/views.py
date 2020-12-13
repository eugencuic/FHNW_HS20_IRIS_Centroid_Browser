from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels, Images
import os
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go
from django.conf import settings

from PIL import Image
import base64

from skimage import io

def index(request):
    """View function for homepage of site."""

    # Generate counts of some of the main objects
    num_centroids = 52
    num_observations = 3358
    num_timestepoberservations = 2324582
    image_numbers = [i for i in range(1,54) if i !=52]

    context = {
        'num_centroids': num_centroids,
        'num_observations': num_observations,
        'num_timestepoberservations' : num_timestepoberservations,
        'images_num': image_numbers
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def list_view(request, centroid, observation, step=263):
    observation_list = CentroidCount.objects.filter(centroid__in=[centroid]).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    plot_graph = Plot(centroid, observation)
    plot_image_1400 = plot_1400()
    key_observation = (Observation.objects.get(id_observation__in=[observation])).observation



    #TODO Change to other format
    path_1330 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
    path_1400 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
    path_2796 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
    path_2832 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'

    return render(request, 'centroid_webapp/observation_list.html', context={
                                                                            'observation_list' : observation_list, 
                                                                            'centroid':centroid, 
                                                                            'observation':observation, 
                                                                            'plot_graph':plot_graph,
                                                                            'plot_image_1400':plot_image_1400,
                                                                            'key_observation':key_observation,
                                                                            'path_1330':path_1330,
                                                                            'path_1400':path_1400,
                                                                            'path_2796':path_2796,
                                                                            'path_2832':path_2832,
                                                                            })

def Plot(centroid, observation):
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
                    line = dict(shape = 'hvh', color = 'rgb(205, 12, 24)', width= 2),
                    marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 6),
                    name='test', 
                    opacity=0.8, 
                    marker_color='green',
                    connectgaps = True
                    )

    layout = go.Layout(
                    title='Appearances for Centroids', 
                    width=1200,
                    height=500,
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



def plot_1400():
    #TODO Write funciton to figure out image name

    # Load image
    #TODO Delete block once relative path is defined
    module_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(settings.STATIC_SAT_IMG, 'yes.jpg')

    # Get Image shape
    img_array = io.imread(path_to_file)
    # Set dimensions of image
    height, width, dept = img_array.shape

    #Find ID of DF of Centroid
    #TODO replace obsevation with variable
    qs = Observation.objects.filter(observation='20140910_112825_3860259453').values_list('observation', 'x_pixels', 'y_pixels')
    centroid_df = pd.DataFrame.from_records(qs.values('observation', 'x_pixels', 'y_pixels'))


    #Find ID of image
    #TODO Replace with variables
    qs = Ypixels.objects.filter(id_observation=2081, step=2350).values_list('id_ypixels', 'id_observation', 'step', 'ypixels', 'l_1330','l_1400', 'l_2796', 'l_2832')
    find_id = pd.DataFrame.from_records(qs.values('id_ypixels', 'id_observation', 'step', 'ypixels', 'l_1330','l_1400', 'l_2796', 'l_2832'))
    id_1400 = find_id.l_1400

    #Get all Data of observation 
    centroids_array = np.array(find_id['ypixels'][0])


    qs = Images.objects.filter(id_image=id_1400).values_list('id_image', 'path', 'slit_pos')
    find_image = pd.DataFrame.from_records(qs.values('id_image', 'path', 'slit_pos'))


    # Which Centroid is activated
    #TODO Change to variable centroid
    activations = (centroids_array==21)

    # number of actual pixels in SJI
    nx, ny = centroid_df['x_pixels'][0], centroid_df['y_pixels'][0]
    # number of pixels on the raster slit
    n = len(activations)

    # scale everything to the JPG
    real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
    x_pos = np.array([real_slit_pos] * n)
    y_pos = np.array(img_array.shape[1] / ny * np.arange(n))



    encoded_image = base64.b64encode(open(path_to_file, 'rb').read())
    img = 'data:image/;base64,{}'.format(encoded_image)

    layout = go.Layout()

    data = []
    fig = go.Figure(data=data, layout=layout)

    traces = {}
    for step in [1,2,3]:
        fig.add_trace(go.Scatter(
                visible=False,
                x=x_pos[activations[::-1]]+step*-30,
                y=y_pos[activations[::-1]],
                ))  

    fig.data[0].visible=True

    steps=[]
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                {"title": "Slider switched to step: " + str(i)}],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=1,
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps
    )]
    xlim = [0, width]
    ylim = [0, height]
    fig.update_layout(
                    images= [dict(
                        source='data:image/png;base64,{}'.format(encoded_image.decode()),
                        xref="paper", yref="paper",
                        x=0, y=1,
                        sizex=1, sizey=1,
                        xanchor="left",
                        yanchor="top",
                        #sizing="stretch",
                        layer="below",
                        )],
                        xaxis_showgrid=False, 
                        yaxis_showgrid=False,
                        xaxis_zeroline=False, 
                        yaxis_zeroline=False,
                        xaxis_visible=True,
                        yaxis_visible=True,
                        width=width,
                        height=height,
                        sliders=sliders,
                        #template="plotly_white"
                        xaxis=dict(range=[xlim[0],xlim[1]]),
                        yaxis=dict(range=[ylim[0],ylim[1]]
                        )
                    )
    data = list(traces.values())
    fig = go.Figure(data=data, layout=layout)

    plot_1400 = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_1400



'''

    try:
        img = ((Ypixels.objects.get(id_observation=observation, step=step)).l_1330).path
        path_1330 = os.path.join('https://www.cs.technik.fhnw.ch/iris/sji_png/images/', img)
    except Ypixels.DoesNotExist:
        path_1330 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'

    try:
        img = ((Ypixels.objects.get(id_observation=observation, step=step)).l_1400).path
        path_1400 = os.path.join('https://www.cs.technik.fhnw.ch/iris/sji_png/images/', img)
    except Ypixels.DoesNotExist:
        path_1400 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'

    try:
        img = ((Ypixels.objects.get(id_observation=observation, step=step)).l_2796).path
        path_2796 = os.path.join('https://www.cs.technik.fhnw.ch/iris/sji_png/images/', img)
    except Ypixels.DoesNotExist:
        path_2796 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
    try:
        img = ((Ypixels.objects.get(id_observation=observation, step=step)).l_2832).path
        path_2832 = os.path.join('https://www.cs.technik.fhnw.ch/iris/sji_png/images/', img)
    except Ypixels.DoesNotExist:
        path_2832 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
'''

