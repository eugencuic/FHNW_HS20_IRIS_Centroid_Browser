import pytest
from centroid_webapp.views import *
import plotly.graph_objects as go
from plotly.offline import plot


# testing the plot function
xmax = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
x = [1,2,3,4,5,6]
y = [1,2,3,4,5,6]

def test_plot():
    result = Plot(xmax,x,y)
    # expecting the function to run and therefore return a html div
    assert "<div>" in result
