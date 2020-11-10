from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels
from django.views import generic

def index(request):
    """View function for homepage of site."""

    # Generate counts of some of the main objects
    num_centroids = CentroidCount.objects.order_by('centroid').values('centroid').distinct().count()
    num_observations = Ypixels.objects.all().count()
    
    context = {
        'num_centroids': num_centroids,
        'num_observations': num_observations,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class CentroidListView(generic.ListView):
    # Generic class-based view for a list of observations
    model = CentroidCount
    paginate_by = 10
    context_object_name = 'centroid_list'


class CentroidDetailView(generic.DetailView):
    # Generic class-based detail view for a observation
    model = CentroidCount
    context_object_name = 'centroid-detail'

    def centroid_detail_view(request, primary_key):
        try:
            centroid = CentroidCount.objects.get(pk=primary_key)
        except Centroid.DoesNotExists:
            raise Http404('Observation does not exist')

        return render(request, 'centroids/centroid_detail.html', context={'centroid' : centroid})