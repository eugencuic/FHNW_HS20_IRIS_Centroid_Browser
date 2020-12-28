import pytest

from centroid_webapp.views import Plot, detail_plot, plot_empty, plot_png
import plotly.graph_objects as go
from plotly.offline import plot


# testing the plot function
xmax = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
x = [1,2,3,4,5,6]
y = [1,2,3,4,5,6]

def test_main_plot_with_plot():
    result = Plot(x,y,xmax)
    # expecting the function to run and therefore return a html div
    assert "<div>" in result

xmax = []
x = []
y = []

def test_main_plot_empty():
    result = Plot(x,y,xmax)
    # expecting the function to run and therefore return a html div
    assert "<div>" in result