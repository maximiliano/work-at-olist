import pytest

from rest_framework.test import APIClient

from core.models import CallDetail


@pytest.mark.django_db
def test_post_call_detail_start():
    """Test simple and correct call start registering"""

    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        "destination": "11123456789"
    }

    client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 1


@pytest.mark.django_db
def test_post_call_detail_end():
    """Test simple and correct call start registering"""

    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "end",
        "timestamp": "2016-02-29T12:00:00Z",
    }

    client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 1
