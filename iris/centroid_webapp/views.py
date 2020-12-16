from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels, Images
import os
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go
from django.conf import settings

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

def list_view(request, centroid, observation):
    ## Initial Querrysets in order to load Plots and Graphics
    observation_list = CentroidCount.objects.filter(centroid__in=[centroid]).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    key_list = Observation.objects.filter(id_observation__in=[observation_list]).order_by('id_observation').values_list('observation', flat=True)
        
    ## Exception Management for initial load of Page
    try:
        step_list = CentroidCount.objects.filter(id_observation__in=[observation], centroid=centroid).values_list('step', flat=True)
    except:
        step_list = []

    try:
        key_observation = (Observation.objects.get(id_observation__in=[observation])).observation
    except Observation.DoesNotExist:
        key_observation = '20140101_000431_3840257196'

    try:
        hek_url = (Observation.objects.get(id_observation__in=[observation])).hek_url
    except Observation.DoesNotExist:
        hek_url = 'https://www.lmsal.com/hek/'

    ## Static variables of plots
    qs_Observation = Observation.objects.filter(observation=key_observation).values_list('observation', 'x_pixels', 'y_pixels')
    centroid_df = pd.DataFrame.from_records(qs_Observation.values('observation', 'x_pixels', 'y_pixels'))

    # number of actual pixels in SJI
    nx = centroid_df['x_pixels'][0]
    ny = centroid_df['y_pixels'][0]

    # Data for Plots
    x_values = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('step', flat=True))
    y_values = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('count', flat=True))
    x_max = list(CentroidCount.objects.filter(id_observation=observation).values_list('step', flat=True))

    # Loading Plots
    plot_graph = Plot(x_max, x_values, y_values)


    if observation == 0:
        plot_image_1330 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
        plot_image_1400 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
        plot_image_2796 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'
        plot_image_2832 = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'

    else: 
        plot_image_1330 = plot_1400(observation, centroid, key_observation, nx, ny, step_list)
        plot_image_1400 = plot_1400(observation, centroid, key_observation, nx, ny, step_list)
        plot_image_2796 = plot_1400(observation, centroid, key_observation, nx, ny, step_list)
        plot_image_2832 = plot_1400(observation, centroid, key_observation, nx, ny, step_list)

    return render(request, 'centroid_webapp/observation_list.html', context={
                                                                            'observation_list' : observation_list, 
                                                                            'centroid':centroid, 
                                                                            'observation':observation, 
                                                                            'plot_graph':plot_graph,
                                                                            'plot_image_1330':plot_image_1330,
                                                                            'plot_image_1400':plot_image_1400,
                                                                            'plot_image_2796':plot_image_2796,
                                                                            'plot_image_2832':plot_image_2832,
                                                                            'key_observation':key_observation,
                                                                            'hek_url':hek_url,
                                                                            })

def Plot(x_max, x, y):
    # Exception Management for initial load
    if not x_max:
        x_max=1

    ###### PLOT START ######
    scatter = go.Scatter(
                    x=x, 
                    y=y, 
                    mode='markers',
                    marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 12),
                    name='test', 
                    opacity=0.8, 
                    marker_color='black',
                    connectgaps = True
                    )

    bar = go.Bar(
                x=x,
                y=y,
                width=0.5,
                marker=dict(
                    color='black'
                ),
    )

    layout = go.Layout(
                    title='Number of appearances for Centroids in Observation', 
                    width=1200,
                    height=500,
                    xaxis=dict(
                        range=([0,x_max]),
                        title='Step',
                        tick0=0,
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    
                    yaxis=dict(
                        title= 'Occurences',
                        dtick=1,
                        tick0=0 
                        ),
                    showlegend=False,
                    )
    
    data = [scatter, bar]
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, include_plotlyjs=False, output_type='div')

    ###### PLOT END ######

    return plot_div


def plot_1400(observation, centroid, key_observation, nx, ny, step_list):

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    data = []
    fig = go.Figure(data=data, layout=layout)

    traces = {}
    for step in step_list:
        # Find ID of Image
        qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels','l_1400')
        find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels','l_1400'))
        id_1400 = find_id.l_1400[0]

        #Get Image DataFrame
        qs_Images = Images.objects.filter(id_image=id_1400).values_list('id_image', 'path', 'slit_pos')
        find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))
        path = str(find_image.path[0])

        #Get centroid array 
        centroids_array = np.array(find_id['ypixels'][0])

        # Which Centroid is activated
        activations = (centroids_array==centroid)

        # number of pixels on the raster slit
        n = len(activations)

        # Load image
        #path_to_file = os.path.join(settings.STATIC_URL,  '/iris_images/{}').format(path)   #full path to text.

        path_to_file = os.path.join(settings.BASE_DIR, 'centroid_webapp/iris_images/{}').format(path)

        # Get Image shape
        img_array = io.imread(path_to_file)

        # Set dimensions of image
        height, width, rgb = img_array.shape

        # scale everything to the JPG
        real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
        x = np.array([real_slit_pos] * n)
        y = np.array(img_array.shape[1] / ny * np.arange(n))

        # Encode Image for into Plotly readable format
        encoded_image = base64.b64encode(open(path_to_file, 'rb').read())

        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='markers',
                x=x[activations[::1]],
                y=y[activations[::1]],
                marker=dict(size=4, color='#00ffcd'),

                ))

        fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_image.decode()),
                sizing="stretch", opacity=0.9, layer='above')
            )  


        xlim = [0, width]
        ylim = [0, height]
        fig.update_layout( 
                    xaxis=dict(range=[xlim[0],xlim[1]], fixedrange=True,),
                    yaxis=dict(range=[ylim[0],ylim[1]], fixedrange=True,),
                    images=[dict(source='data:image/png;base64,{}'.format(encoded_image.decode()))]
                )


    fig.data[0].visible=True

    steps=[]
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
        )

        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(active=1, pad={"t": 5}, steps=steps )]

    #TODO Check how to integrate bellow lines into loop

    fig.update_layout(
                    images= [dict(
                        xref="paper", yref="paper",
                        x=0, y=1, sizex=1, sizey=1, xanchor="left", yanchor="top", layer="below",
                        )],
                        xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False, xaxis_visible=False, yaxis_visible=False,
                        width=325, height=375, autosize=False,
                        sliders=sliders,
                        template="plotly_white",
                        margin=dict(l=10, r=10, t=5, b=5),
                    )
    data = list(traces.values())
    plot_1400 = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_1400


##################################################################################################################

def plot_1330(observation, centroid, key_observation, nx, ny, step_list):

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    data = []
    fig = go.Figure(data=data, layout=layout)

    traces = {}
    for step in step_list:
        # Find ID of Image
        qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels','l_1330')
        find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels','l_1330'))
        id_1330 = find_id.l_1330[0]

        #Get Image DataFrame
        qs_Images = Images.objects.filter(id_image=id_1330).values_list('id_image', 'path', 'slit_pos')
        find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))

        #Get centroid array 
        centroids_array = np.array(find_id['ypixels'][0])

        # Which Centroid is activated
        activations = (centroids_array==centroid)

        # number of pixels on the raster slit
        n = len(activations)

        # Load image
        #TODO Change path with {{observation key}}
        module_dir = os.path.dirname(__file__)  #current dir
        path_to_file = os.path.join(module_dir, 'static/iris_images/yes.jpg')   #full path to text.

        # Get Image shape
        img_array = io.imread(path_to_file)

        # Set dimensions of image
        height, width, rgb = img_array.shape

        # scale everything to the JPG
        real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
        x = np.array([real_slit_pos] * n)
        y = np.array(img_array.shape[1] / ny * np.arange(n))

        # Encode Image for into Plotly readable format
        encoded_image = base64.b64encode(open(path_to_file, 'rb').read())

        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='markers',
                x=x[activations[::1]],
                y=y[activations[::1]],
                marker=dict(size=2, color='#00ffcd'),

                ))

        fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_image.decode()),
                sizing="stretch", opacity=0.9, layer='above')
            )  

    fig.data[0].visible=True

    steps=[]
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
        )

        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(active=1, pad={"t": 5}, steps=steps )]

    #TODO Check how to integrate bellow lines into loop
    xlim = [0, width]
    ylim = [0, height]
    fig.update_layout(
                    images= [dict(
                        xref="paper", yref="paper",
                        x=0, y=1, sizex=1, sizey=1, xanchor="left", yanchor="top", layer="below",
                        )],
                        xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False, xaxis_visible=False, yaxis_visible=False,
                        width=325, height=375, autosize=False,
                        sliders=sliders,
                        template="plotly_white",
                        xaxis=dict(range=[xlim[0],xlim[1]], fixedrange=True,),
                        yaxis=dict(range=[ylim[0],ylim[1]], fixedrange=True,),
                        margin=dict(l=10, r=10, t=5, b=5),
                    )
    data = list(traces.values())
    plot_1330 = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_1330

def plot_2796(observation, centroid, key_observation, nx, ny, step_list):

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    data = []
    fig = go.Figure(data=data, layout=layout)

    traces = {}
    for step in step_list:
        # Find ID of Image
        qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels','l_1400')
        find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels','l_2796'))
        id_2796 = find_id.l_2796[0]

        #Get Image DataFrame
        qs_Images = Images.objects.filter(id_image=id_2796).values_list('id_image', 'path', 'slit_pos')
        find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))

        #Get centroid array 
        centroids_array = np.array(find_id['ypixels'][0])

        # Which Centroid is activated
        activations = (centroids_array==centroid)

        # number of pixels on the raster slit
        n = len(activations)

        # Load image
        #TODO Change path with {{observation key}}
        module_dir = os.path.dirname(__file__)  #current dir
        path_to_file = os.path.join(module_dir, 'static/iris_images/yes.jpg')   #full path to text.

        # Get Image shape
        img_array = io.imread(path_to_file)

        # Set dimensions of image
        height, width, rgb = img_array.shape

        # scale everything to the JPG
        real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
        x = np.array([real_slit_pos] * n)
        y = np.array(img_array.shape[1] / ny * np.arange(n))

        # Encode Image for into Plotly readable format
        encoded_image = base64.b64encode(open(path_to_file, 'rb').read())

        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='markers',
                x=x[activations[::1]],
                y=y[activations[::1]],
                marker=dict(size=2, color='#00ffcd'),

                ))

        fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_image.decode()),
                sizing="stretch", opacity=0.9, layer='above')
            )  

    fig.data[0].visible=True

    steps=[]
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
        )

        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(active=1, pad={"t": 5}, steps=steps )]

    #TODO Check how to integrate bellow lines into loop
    xlim = [0, width]
    ylim = [0, height]
    fig.update_layout(
                    images= [dict(
                        xref="paper", yref="paper",
                        x=0, y=1, sizex=1, sizey=1, xanchor="left", yanchor="top", layer="below",
                        )],
                        xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False, xaxis_visible=False, yaxis_visible=False,
                        width=325, height=375, autosize=False,
                        sliders=sliders,
                        template="plotly_white",
                        xaxis=dict(range=[xlim[0],xlim[1]], fixedrange=True,),
                        yaxis=dict(range=[ylim[0],ylim[1]], fixedrange=True,),
                        margin=dict(l=10, r=10, t=5, b=5),
                    )
    data = list(traces.values())
    plot_2796 = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_2796

def plot_2832(observation, centroid, key_observation, nx, ny, step_list):

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    data = []
    fig = go.Figure(data=data, layout=layout)

    traces = {}
    for step in step_list:
        # Find ID of Image
        qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels','l_1400')
        find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels','l_2832'))
        id_2832 = find_id.l_2832[0]

        #Get Image DataFrame
        qs_Images = Images.objects.filter(id_image=id_2832).values_list('id_image', 'path', 'slit_pos')
        find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))

        #Get centroid array 
        centroids_array = np.array(find_id['ypixels'][0])

        # Which Centroid is activated
        activations = (centroids_array==centroid)

        # number of pixels on the raster slit
        n = len(activations)

        # Load image
        #TODO Change path with {{observation key}}
        module_dir = os.path.dirname(__file__)  #current dir
        path_to_file = os.path.join(module_dir, 'static/iris_images/yes.jpg')   #full path to text.

        # Get Image shape
        img_array = io.imread(path_to_file)

        # Set dimensions of image
        height, width, rgb = img_array.shape

        # scale everything to the JPG
        real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
        x = np.array([real_slit_pos] * n)
        y = np.array(img_array.shape[1] / ny * np.arange(n))

        # Encode Image for into Plotly readable format
        encoded_image = base64.b64encode(open(path_to_file, 'rb').read())

        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='markers',
                x=x[activations[::1]],
                y=y[activations[::1]],
                marker=dict(size=2, color='#00ffcd'),

                ))

        fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_image.decode()),
                sizing="stretch", opacity=0.9, layer='above')
            )  

    fig.data[0].visible=True

    steps=[]
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
        )

        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(active=1, pad={"t": 5}, steps=steps )]

    #TODO Check how to integrate bellow lines into loop
    xlim = [0, width]
    ylim = [0, height]
    fig.update_layout(
                    images= [dict(
                        xref="paper", yref="paper",
                        x=0, y=1, sizex=1, sizey=1, xanchor="left", yanchor="top", layer="below",
                        )],
                        xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False, xaxis_visible=False, yaxis_visible=False,
                        width=325, height=375, autosize=False,
                        sliders=sliders,
                        template="plotly_white",
                        xaxis=dict(range=[xlim[0],xlim[1]], fixedrange=True,),
                        yaxis=dict(range=[ylim[0],ylim[1]], fixedrange=True,),
                        margin=dict(l=10, r=10, t=5, b=5),
                    )
    data = list(traces.values())
    plot_1400 = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_2832