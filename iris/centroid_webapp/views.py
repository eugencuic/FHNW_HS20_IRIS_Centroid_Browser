from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from centroid_webapp.models import CentroidCount, Observation, Ypixels
from django.views import generic
from centroid_webapp.forms import CentroidForm

def index(request):
    """View function for homepage of site."""

    # Generate counts of some of the main objects
    num_centroids = CentroidCount.objects.order_by('centroid').values('centroid').distinct().count()
    num_observations = Observation.objects.all().count()
    num_timestepoberservations = Ypixels.objects.all().count()

    
    context = {
        'num_centroids': num_centroids,
        'num_observations': num_observations,
        'num_timestepoberservations' : num_timestepoberservations,
    }

    context['form'] = CentroidForm

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

'''
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