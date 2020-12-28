import pytest

from centroid_webapp.views import *
import plotly.graph_objects as go
from plotly.offline import plot


# testing the plot function
xmax = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
x = [1,2,3,4,5,6]
y = [1,2,3,4,5,6]

def test_plot():
    result = Plot(x,y,xmax)
    # expecting the function to run and therefore return a html div
    assert "<div>" in result

xmax = []
x = []
y = []

def test_plot():
    result = Plot(x,y,xmax)
    # expecting the function to run and therefore return a html div
    assert "<div>" in result

observation = 'test'
step = 33
image_choice = 1330
def test_detail_plot():
    result = detail_plot(observation, centroid, nx, ny, image_choice, step)
    assert "<div>" in result