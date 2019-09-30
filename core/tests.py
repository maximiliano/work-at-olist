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


@pytest.mark.django_db
def test_post_call_detail_missing_call_id():
    client = APIClient()

    call_data = {
        "id": 1,
        # "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'call_id': 'This field is required.'}


@pytest.mark.django_db
def test_post_call_detail_missing_type():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        # "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'type': 'This field is required.'}


@pytest.mark.django_db
def test_post_call_detail_missing_timestamp():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        # "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'timestamp': 'This field is required.'}


@pytest.mark.django_db
def test_post_call_detail_missing_source():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        # "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'source': 'This field is required if call type is start.'}


@pytest.mark.django_db
def test_post_call_detail_missing_destination():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        # "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'destination': 'This field is required if call type is start.'}


@pytest.mark.django_db
def test_post_call_detail_wrong_call_id_type():
    client = APIClient()

    call_data = {
        "id": 1,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "call_id": "123",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'call_id': 'call_id must be an integer'}


@pytest.mark.django_db
def test_post_call_detail_wrong_timestamp_type():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": 20160930,
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'timestamp': 'timestamp must be a string'}


@pytest.mark.django_db
def test_post_call_detail_wrong_source_type():
    client = APIClient()

    call_data = {
        "id": 1,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "call_id": 11,
        "source": 11987654321,
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'source': 'source must be a string'}


@pytest.mark.django_db
def test_post_call_detail_wrong_destination_type():
    client = APIClient()

    call_data = {
        "id": 1,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "call_id": 11,
        "source": "11987654321",
        "destination": 11123456789
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {'destination': 'destination must be a string'}
