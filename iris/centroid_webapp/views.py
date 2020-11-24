from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels
from django.views import generic
from centroid_webapp.forms import CentroidForm
import os

# TODO use this function to return list of observations to create list 
# CentroidCount.objects.filter(centroid__in=[...id,id,...]).order_by('id_observation').values_list('id_observation', flat=True).distinct()
# 

def index(request):


    """View function for homepage of site."""

    # Generate counts of some of the main objects
    num_centroids = 52
    num_observations = 3358
    num_timestepoberservations = 2324582

    context = {
        'num_centroids': num_centroids,
        'num_observations': num_observations,
        'num_timestepoberservations' : num_timestepoberservations,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class CentroidListView(generic.ListView):
    # Generic class-based view for a list of observations
    model = CentroidCount
    paginate_by = 10
    context_object_name = 'centroid_list'

'''
class CentroidDetailView(generic.DetailView):
    # Generic class-based detail view for a observation
    model = CentroidCount
    context_object_name = 'centroid-detail'
    # TODO: Check following function if it is necessary anymore
    def centroid_detail_view(request, primary_key):
        try:
            centroid = CentroidCount.objects.get(pk=primary_key)
        except Centroid.DoesNotExists:
            raise Http404('Observation does not exist')

        return render(request, 'centroids/centroid_detail.html', context={'centroid' : centroid})


def get_centroids(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'your-name.html', {'form': form})
    '''