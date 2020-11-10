from django.shortcuts import render
from centroid_webapp.models import *

# TODO: Check calculation of centroid count, it should be 54 because there are 54 distinct centroid
# TODO: See if there is a possbility to extract dates
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_observation = Observation.objects.all().count()
    num_centroids = CentroidCount.objects.all().distinct().count()
    
    
    context = {
        'num_observation': num_observation,
        'num_centroids': num_centroids,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)