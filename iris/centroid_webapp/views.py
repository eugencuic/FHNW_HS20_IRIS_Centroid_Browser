from django.shortcuts import render
from django.views import generic
from .models import Observation, CentroidCount

def index(request):
    num_observations = Observation.objects.all().count()
    #Placeholder with a dictionary, containint the data to insert into the placeholders
    context = {
        'num_observations' : num_observations,
    }
    return render (request, 'index.html', context=context)

#TODO make this as filter and not static
class CentroidListView(generic.ListView):
    model = CentroidCount
    context_object_name = 'centroid_filter_list'
    queryset = CentroidCount.objects.filter(centroid__cointains='23') [:5]
    #TODO: Check if this is the correct path for the template
    template_name = 'centroids/centroids_filterd_list.html'