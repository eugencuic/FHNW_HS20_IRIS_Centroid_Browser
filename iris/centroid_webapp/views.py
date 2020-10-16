from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'centroid_webapp/home.html')

def centroids(request):
    return render(request, 'centroid_webapp/centroids.html')

def subscription(request):
    return render(request, 'centroid_webapp/subscription.html')


