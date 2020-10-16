from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Home Page")

def centroids(request):
    return HttpResponse("Centroid Analytics")

def subscription(request):
    return HttpResponse("Subscription")