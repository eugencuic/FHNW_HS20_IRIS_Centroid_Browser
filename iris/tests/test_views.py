import pytest

from django.urls import reverse
from centroid_webapp.models import *
from centroid_webapp.views import *


# check for status code 200 and value
def test_index_view(client):
    url = reverse("index")
    request = client.get(url)
    response = index(request)
    content = response.content.decode(response.charset)
    assert response.status_code == 200
    assert "2324582" in content
'''
@pytest.mark.django_db
def test_detail_view(client):
    request = client.get('/centroid_webapp/observations/1&0&0&0')
    response = list_view(request)
    content = response.content.decode(response.charset)
    assert response.status_code == 200

'''