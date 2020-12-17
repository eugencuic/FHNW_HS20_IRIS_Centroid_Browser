from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels, Images
import os
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go
from django.conf import settings
#import base64
from skimage import io
import io as ioo
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

#from io import BytesIO
#import matplotlib
#matplotlib.use("Agg")
#import matplotlib.pyplot as plt

def index(request):
    """View function for homepage of site."""

    # Generate counts of some of the main objects
    num_centroids = 52
    num_observations = 3358
    num_timestepoberservations = 2324582
    image_numbers = [i for i in range(1,53)]

    context = {
        'num_centroids': num_centroids,
        'num_observations': num_observations,
        'num_timestepoberservations' : num_timestepoberservations,
        'images_num': image_numbers
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def list_view(request, centroid, observation, image_choice, step):


    ## Initial Querrysets in order to load Plots and Graphics
    observation_list = CentroidCount.objects.filter(centroid=centroid).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    key_list = Observation.objects.filter(id_observation__in=[observation_list]).values_list('observation', flat=True)
    zipped_list = zip(observation_list, key_list)

    if observation == 0:
        key_observation = 'n/a'
        hek_url = 'https://www.lmsal.com/hek/'
        plot_graph = "<div>please choose an observation</div>"

        context={
                'zipped_list':zipped_list,
                'centroid':centroid, 
                'observation':observation,
                'image_choice':image_choice, 
                'step':step,
                'plot_graph':plot_graph,
                'key_observation':key_observation,
                'hek_url':hek_url,
                }

    else:
        # Data for Plots
        x_values = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('step', flat=True))
        y_values = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('count', flat=True))
        x_max = list(CentroidCount.objects.filter(id_observation=observation).values_list('step', flat=True))

        # Reusing x_values for step list as it is the same data
        step_list = x_values

        # Loading Plots
        plot_graph = Plot(x_values, y_values, x_max)
            

        ## Exception Management for initial load of Page
        key_observation = (Observation.objects.get(id_observation__in=[observation])).observation
        hek_url = (Observation.objects.get(id_observation__in=[observation])).hek_url
            
        qs_Observation = Observation.objects.filter(observation=key_observation).values_list('observation', 'x_pixels', 'y_pixels')
        centroid_df = pd.DataFrame.from_records(qs_Observation.values('observation', 'x_pixels', 'y_pixels'))
        # number of actual pixels in SJI
        nx = centroid_df['x_pixels'][0]
        ny = centroid_df['y_pixels'][0]

        #plot_image = detail_plot(observation, centroid, key_observation, nx, ny, step_list, image_choice, step)

        context={
                                                                            'zipped_list':zipped_list,
                                                                            'centroid':centroid, 
                                                                            'observation':observation,
                                                                            'image_choice':image_choice, 
                                                                            'step':step,
                                                                            'plot_graph':plot_graph,
                                                                            'key_observation':key_observation,
                                                                            'hek_url':hek_url,
                                                                            }


    return render(request, 'centroid_webapp/observation_list.html', context=context)


def Plot(x, y, x_max):
    if not x_max:
        x_max=1

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
                width=0.1,
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
                        title='Occurences',
                        tick0=0,
                        dtick=1,
                    ),
                    showlegend=False,
                    )
    
    data = [scatter, bar]
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_div


def detail_plot(observation, centroid, key_observation, nx, ny, step_list, image_choice, step):

    if image_choice == 0:
        return "<div></div>"

    # Find ID of Image
    qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels',('l_'+str(image_choice)))
    find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels',('l_'+str(image_choice))))

    id = qs_Ypixels[0][1]
    if not id:
        return "<div>There is no data available for this image type</div>"

    #Get Image DataFrame
    qs_Images = Images.objects.filter(id_image=id).values_list('id_image', 'path', 'slit_pos')
    find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))
    path = str(find_image.path[0])      

    # Load image
    path_to_file = os.path.join(settings.BASE_DIR, 'centroid_webapp/iris_images/{}').format(path)
    
    # Get Image shape
    img_array = io.imread(path_to_file)

    #Get centroid array 
    centroids_array = np.array(find_id['ypixels'][0])

    # Which Centroid is activated
    activations = (centroids_array==centroid)

    # number of pixels on the raster slit
    n = len(activations)

    # plot image
    plt.imshow(img_array, origin="upper" )

    # scale everything to the JPG
    real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
    x = np.array([real_slit_pos] * n)
    y = np.array(img_array.shape[0] / ny * np.arange(n))


    plt.scatter( x[activations[::-1]], y[activations[::-1]], c="yellow", s=2 )
    plt.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plot = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    
    return plot

def detail_plot_neu(observation, centroid, nx, ny, image_choice, step):

    if image_choice == 0:
        return "<div></div>"

    # Find ID of Image
    qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels',('l_'+str(image_choice)))
    find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels',('l_'+str(image_choice))))

    id = qs_Ypixels[0][1]
    if not id:
        return "<div>There is no data available for this image type</div>"

    #Get Image DataFrame
    qs_Images = Images.objects.filter(id_image=id).values_list('id_image', 'path', 'slit_pos')
    find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))
    path = str(find_image.path[0])      

    # Load image
    path_to_file = os.path.join(settings.BASE_DIR, 'centroid_webapp/iris_images/{}').format(path)
    
    # Get Image shape
    img_array = io.imread(path_to_file)

    #Get centroid array 
    centroids_array = np.array(find_id['ypixels'][0])

    # Which Centroid is activated
    activations = (centroids_array==centroid)

    # number of pixels on the raster slit
    n = len(activations)



    #xs = plot.imshow(img_array, origin="upper" )

    # plot image
    #plt.imshow(img_array, origin="upper" )

    # scale everything to the JPG
    real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
    x = np.array([real_slit_pos] * n)
    y = np.array(img_array.shape[0] / ny * np.arange(n))


    #plt.scatter( x[activations[::-1]], y[activations[::-1]], c="yellow", s=2 )

    #fig.scatter( x[activations[::-1]], y[activations[::-1]], c="yellow", s=2 )

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = [1,2,3,4,5,6,6,7]
    ys = [1,2,3,4,5,9,8,7]
    axis.plot(xs, ys)

    #plt.axis('off')

    return fig

def plot_png(request):
    key_observation = (Observation.objects.get(id_observation=15)).observation
    qs_Observation = Observation.objects.filter(observation=key_observation).values_list('observation', 'x_pixels', 'y_pixels')
    centroid_df = pd.DataFrame.from_records(qs_Observation.values('observation', 'x_pixels', 'y_pixels'))
    # number of actual pixels in SJI
    nx = centroid_df['x_pixels'][0]
    ny = centroid_df['y_pixels'][0]

    #fig = create_figure()
    fig = detail_plot_neu(15, 5, nx, ny, 1400, 75)
    output = ioo.BytesIO()
    FigureCanvas(fig).print_png(output)
    return HttpResponse(output.getvalue(), content_type='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig