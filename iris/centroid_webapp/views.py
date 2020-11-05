from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'centroid_webapp/home.html')

def centroids(request):
    return render(request, 'centroid_webapp/centroids.html')

def selected_observations(request, obs_id):
    return HttpResponse(obs_id)

# TODO: Delete as this is only for exercise purpose
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

    return render(request, 'name.html', {'form': form})