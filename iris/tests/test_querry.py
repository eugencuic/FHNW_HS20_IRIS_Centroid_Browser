import pytest
from centroid_webapp.models import CentroidCount


centroid = 44
@pytest.mark.django_db
def test_centroid_query():
    result = CentroidCount.objects.filter(centroid=centroid).order_by('id_observation').values_list('id_observation', flat=True).distinct()
    # expecting to have no dulbicate observation showing up in template
    assert len(result) == len(set(result))


