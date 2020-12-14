import pytest

from django.urls import reverse
from centroid_webapp.models import *
from centroid_webapp.views import *

def test_always_passes():
    assert True

#@pytest.mark.django_db
# check for status code 200 and title
def test_index_view(client):
    url = reverse("index")
    request = client.get(url)
    response = index(request)
    content = response.content.decode(response.charset)
    assert response.status_code == 200
    assert "2324582" in content
