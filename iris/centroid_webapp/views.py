from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels, Images
import os
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go
from skimage import io
import io as ioo
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

    ## Initial Querrysets in order to load Plots and Graphics and Lists
    observation_list = CentroidCount.objects.filter(centroid=centroid).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    key_list = Observation.objects.filter(id_observation__in=[observation_list]).values_list('observation', flat=True)
    zipped_list = zip(observation_list, key_list)



    # Exception Management to capture cases where no data is available
    if observation == 0:
        key_observation = 'n/a'
        hek_url = 'https://www.lmsal.com/hek/'
        plot_graph = "<div>please choose an observation</div>"

        # Reduced context data for HTML template. Load only what is needed and available
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
        # Data for Plots. x_values are the steps of the obsevation where the centroid appears and x_values the count. 
        x_values = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('step', flat=True))
        y_values = list(CentroidCount.objects.filter(id_observation=observation).filter(centroid=centroid).values_list('count', flat=True))

        # x_max is used as defintion of the length of the xaxis 
        x_max = list(CentroidCount.objects.filter(id_observation=observation).values_list('step', flat=True))

        # Reusing x_values for step list as it is the same data
        step_list = x_values

        # Loading Plots
        plot_graph = Plot(x_values, y_values, x_max)
            

        # key_observation is the KEY that reasearcher are using to identiy the images and observations 
        key_observation = (Observation.objects.get(id_observation__in=[observation])).observation

        # The hek URL is used to point the researcher to more details to the website of Heliophysics Events Knowledgebase Coverage Registry
        # for the respective observation that is chosen right now
        hek_url = (Observation.objects.get(id_observation__in=[observation])).hek_url

        # Full context variables that can be loaded once an observation is chosen
        context={
                                                                            'zipped_list':zipped_list,
                                                                            'centroid':centroid, 
                                                                            'observation':observation,
                                                                            'image_choice':image_choice, 
                                                                            'step':step,
                                                                            'plot_graph':plot_graph,
                                                                            'key_observation':key_observation,
                                                                            'hek_url':hek_url,
                                                                            'step_list':step_list,
                                                                            }


    return render(request, 'centroid_webapp/observation_list.html', context=context)

def Plot(x, y, x_max):
    # Exception management for x-axis length. If there is no observation then the x-axis is set to 0 in order to load an empty plot
    if not x_max:
        x_max=1

    # Scatter plot to display the step where the centroid occured and how many times it did with the count on the y axis
    scatter = go.Scatter(
                    x=x, 
                    y=y, 
                    mode='markers',
                    marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 12),
                    opacity=0.8, 
                    marker_color='black',
                    connectgaps = True,
                    name = 'Step: ', 
                    )

    # The bar plot is used to connect the bottom line with the dot of the scatter plot
    bar = go.Bar(
                x=x,
                y=y,
                width=0.1,
                marker=dict(
                    color='black'
                ),
    )

    # Some layout settings like, size, x-axis range, colors of plot, and titles
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
    
    # Load both traces of plot as data proceed to the Figure to create the plot
    data = [scatter, bar]
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(hovermode='x unified')

    # Create an <div> of the plot in order to be able to display it in the HTML Template
    plot_div = plot(fig, include_plotlyjs=False, output_type='div')

    return plot_div

def detail_plot(observation, centroid, nx, ny, image_choice, step):

    # Find ID of Image
    qs_Ypixels = Ypixels.objects.filter(id_observation=observation, step=step).values_list('ypixels',('l_'+str(image_choice)))
    find_id = pd.DataFrame.from_records(qs_Ypixels.values('ypixels',('l_'+str(image_choice))))

    # Exception management to send out empty plot if there is no image ID to load
    id = qs_Ypixels[0][1]
    if not id:
        return plot_empty()

    #Get Image DataFrame
    qs_Images = Images.objects.filter(id_image=id).values_list('id_image', 'path', 'slit_pos')
    find_image = pd.DataFrame.from_records(qs_Images.values('id_image', 'path', 'slit_pos'))
    path = str(find_image.path[0])      

    # Load image
    path_to_file = ('https://www.cs.technik.fhnw.ch/iris/sji_png/images//{}').format(path)
    
    # Get Image shape
    img_array = io.imread(path_to_file)

    #Get centroid array 
    centroids_array = np.array(find_id['ypixels'][0])

    # Which Centroid is activated
    activations = (centroids_array==centroid)

    # number of pixels on the raster slit
    n = len(activations)

    # scale everything to the JPG
    real_slit_pos = find_image['slit_pos'][0] * img_array.shape[1] / nx
    x = np.array([real_slit_pos] * n)
    y = np.array(img_array.shape[0] / ny * np.arange(n))

    fig = Figure(facecolor='#ebeff5')
    axis = fig.add_subplot(1, 1, 1)
    axis.imshow(img_array, origin="upper")

    axis.scatter( x[activations[::-1]], y[activations[::-1]], c="#04d9ff", s=10  )
    axis.axis('off')
    axis.plot()

    return fig

# An emptly plot that is used as return if there is no data
def plot_empty():
    fig = Figure()
    fig = Figure(facecolor='#ebeff5')
    output = ioo.BytesIO()
    FigureCanvas(fig).print_png(output)

    return HttpResponse(output.getvalue(), content_type='image/png')

def plot_png(request, centroid, observation, image_choice, step):

    # Exception Management if no image type is chosen to load an empty plot
    if image_choice == 0:
        return plot_empty()

    # Load data to create a detailed plot. Data is not loaded up front instead it is loaded just in time
    key_observation = (Observation.objects.get(id_observation=observation)).observation
    qs_Observation = Observation.objects.filter(observation=key_observation).values_list('observation', 'x_pixels', 'y_pixels')
    
    # Transform Querryset into Pandas Dataframe 
    centroid_df = pd.DataFrame.from_records(qs_Observation.values('observation', 'x_pixels', 'y_pixels'))

    # number of actual pixels in SJI
    nx = centroid_df['x_pixels'][0]
    ny = centroid_df['y_pixels'][0]

    fig = detail_plot(observation, centroid, nx, ny, image_choice, step)

    # Transform the plot into a PNG File in order to store it for the HTML Template
    output = ioo.BytesIO()
    try: 
        FigureCanvas(fig).print_png(output)
        return HttpResponse(output.getvalue(), content_type='image/png')
    except: 
        fig = Figure()
        fig = Figure(facecolor='#ebeff5')
        output = ioo.BytesIO()
        FigureCanvas(fig).print_png(output)

        return HttpResponse(output.getvalue(), content_type='image/png')