from datetime import datetime, timezone

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

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 1
    assert response.status_code == 204

    call = CallDetail.objects.get(call_id=11)
    assert call.source == "11987654321"
    assert call.destination == "11123456789"
    assert call.duration == None
    assert call.price == None
    assert call.reference_period == None
    assert call.started_at == datetime(2016, 2, 29, 12, 0, 0,
                                       tzinfo=timezone.utc)
    assert call.ended_at == None
    assert call.is_completed == False


@pytest.mark.django_db
def test_post_call_detail_end():
    """Test simple and correct call end registering"""

    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "end",
        "timestamp": "2016-02-29T12:00:00Z",
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 1
    assert response.status_code == 204

    call = CallDetail.objects.get(call_id=11)
    assert call.source == None
    assert call.destination == None
    assert call.duration == None
    assert call.price == None
    assert call.reference_period == "02/2016"
    assert call.started_at == None
    assert call.ended_at == datetime(2016, 2, 29, 12, 0, 0,
                                     tzinfo=timezone.utc)
    assert call.is_completed == False


@pytest.mark.django_db
def test_post_call_end_after_start():
    """Test POST call end when the start was already registered"""

    client = APIClient()

    # Create a previous CallDetail with Record Call Start info already present
    CallDetail.objects.create(
        call_id=123, source="11987654321", destination="1187654321",
        started_at=datetime(2019, 9, 30, 8, 30, 15))

    old_call = CallDetail.objects.get(call_id=123)

    # Test existing call records
    assert CallDetail.objects.count() == 1
    assert old_call.source == "11987654321"
    assert old_call.destination == "1187654321"
    assert old_call.duration == None
    assert old_call.price == None
    assert old_call.reference_period == None
    assert old_call.started_at == datetime(2019, 9, 30, 8, 30, 15,
                                           tzinfo=timezone.utc)
    assert old_call.ended_at == None
    assert old_call.is_completed == False

    # Register and test new call records, completing the CallDetail model info
    call_data = {
        "id": 1,
        "call_id": 123,
        "type": "end",
        "timestamp": "2019-09-30T08:40:00Z"
    }

    response = client.post('/calls/', call_data, format='json')
    assert response.status_code == 204
    assert CallDetail.objects.count() == 1

    call = CallDetail.objects.get(call_id=123)
    assert call.source == "11987654321"
    assert call.destination == "1187654321"
    assert call.duration == 585
    # 9 billed minutes
    assert call.price == 117
    assert call.reference_period == "09/2019"
    assert call.started_at == datetime(2019, 9, 30, 8, 30, 15,
                                       tzinfo=timezone.utc)
    assert call.ended_at == datetime(2019, 9, 30, 8, 40, 0,
                                     tzinfo=timezone.utc)
    assert call.is_completed == True


@pytest.mark.django_db
def test_post_call_start_after_end():
    """Test POST call start when the end was already registered"""

    client = APIClient()

    # Create a previous CallDetail with Record Call End info already present
    CallDetail.objects.create(
        call_id=123, ended_at=datetime(2019, 9, 30, 8, 40, 0),
        reference_period="09/2019")

    old_call = CallDetail.objects.get(call_id=123)

    # Test existing call records
    assert CallDetail.objects.count() == 1
    assert old_call.source == None
    assert old_call.destination == None
    assert old_call.duration == None
    assert old_call.price == None
    assert old_call.reference_period == "09/2019"
    assert old_call.started_at == None
    assert old_call.ended_at == datetime(2019, 9, 30, 8, 40, 0,
                                         tzinfo=timezone.utc)
    assert old_call.is_completed == False

    # Register and test new call records, completing the CallDetail model info
    call_data = {
        "id": 1,
        "call_id": 123,
        "type": "start",
        "timestamp": "2019-09-30T08:30:15Z",
        "source": "11987654321",
        "destination": "1187654321"
    }

    response = client.post('/calls/', call_data, format='json')
    assert response.status_code == 204
    assert CallDetail.objects.count() == 1

    call = CallDetail.objects.get(call_id=123)
    assert call.source == "11987654321"
    assert call.destination == "1187654321"
    assert call.duration == 585
    # 9 billed minutes
    assert call.price == 117
    assert call.reference_period == "09/2019"
    assert call.started_at == datetime(2019, 9, 30, 8, 30, 15,
                                       tzinfo=timezone.utc)
    assert call.ended_at == datetime(2019, 9, 30, 8, 40, 0,
                                     tzinfo=timezone.utc)
    assert call.is_completed == True


# Section: Validation Errors =================================================

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
    assert response.status_code == 400


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
    assert response.status_code == 400


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
    assert response.status_code == 400


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
    assert response.status_code == 400


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
    assert response.status_code == 400


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
    assert response.json() == {'call_id': 'call_id must be an integer.'}
    assert response.status_code == 400


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
    assert response.json() == {'timestamp': 'timestamp must be a string.'}
    assert response.status_code == 400


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
    assert response.json() == {'source': 'source must be a string.'}
    assert response.status_code == 400


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
    assert response.json() == {'destination': 'destination must be a string.'}
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_call_detail_wrong_type_format():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "something",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'type': 'type must be a string with value "start" or "end".'}
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_call_detail_wrong_timestamp_format():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016/02/29 12:00:00",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'timestamp': 'timestamp must be in the format: "YYYY-MM-DDThh:mm:ssZ"'}
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_call_detail_wrong_source_format():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'source': 'source must be a string of 10 or 11 digits.'}
    assert response.status_code == 400

    call_data['source'] = "9876ABC54321"
    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'source': 'source must be a string of 10 or 11 digits.'}
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_call_detail_wrong_destination_format():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "11987654321",
        "destination": "+5511123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'destination': 'destination must be a string of 10 or 11 digits.'}
    assert response.status_code == 400

    call_data["destination"] = "(11)12345678"
    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'destination': 'destination must be a string of 10 or 11 digits.'}
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_call_detail_end_ignore_number_format():
    """If call type is end, source and destination are ignored even if wrong"""

    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "end",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "(1)987654321",
        "destination": "+5511123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 1
    assert response.status_code == 204


# Section: Price Calculations ================================================

@pytest.mark.django_db
def test_post_call_detail_reduced_tariff():
    client = APIClient()

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "start",
        "timestamp": "2016-02-29T05:00:00Z",
        "source": "11987654321",
        "destination": "11123456789"
    }

    response = client.post('/calls/', call_data, format='json')
    assert response.status_code == 204

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "end",
        "timestamp": "2016-02-29T05:40:00Z",
    }

    response = client.post('/calls/', call_data, format='json')
    assert response.status_code == 204

    assert CallDetail.objects.count() == 1

    call = CallDetail.objects.get(call_id=11)
    assert call.source == "11987654321"
    assert call.destination == "11123456789"
    assert call.duration == 2400
    assert call.price == 36
    assert call.reference_period == "02/2016"
    assert call.started_at == datetime(2016, 2, 29, 5, 0, 0,
                                       tzinfo=timezone.utc)
    assert call.ended_at == datetime(2016, 2, 29, 5, 40, 0,
                                     tzinfo=timezone.utc)
    assert call.is_completed == True


# Section: Validate Get Telephone Bill Params ================================

@pytest.mark.django_db
def test_get_calls_missing_subscriber():
    client = APIClient()

    response = client.get('/calls/', {}, format="json")
    assert response.status_code == 400

    assert response.json() == {
        'number': 'This field is required.'}


@pytest.mark.django_db
def test_get_calls_wrong_subscriber_format():
    client = APIClient()

    params = {
        'number': "(22)1234567",
        'period': "10/2011"
    }
    response = client.get('/calls/', params, format="json")
    assert response.status_code == 400

    assert response.json() == {
        'number':
            'number must be a string of 10 or 11 digits.'}


@pytest.mark.django_db
def test_get_calls_wrong_period_format():
    client = APIClient()

    params = {
        'number': "2212345678",
        'period': "2011-10"
    }
    response = client.get('/calls/', params, format="json")
    assert response.status_code == 400

    assert response.json() == {
        'period':
            'period must be in the format: "MM/YYYY"'}


@pytest.mark.django_db
@pytest.mark.freeze_time('2011-12-13')
def test_get_calls_wrong_closed_period():
    client = APIClient()

    params = {
        'number': "2212345678",
        'period': "12/2011"
    }
    expected = {'period': 'period must be of a closed (previous) month.'}

    response = client.get('/calls/', params, format="json")
    assert response.status_code == 400
    assert response.json() == expected

    params['period'] = "03/2012"
    response = client.get('/calls/', params, format="json")
    assert response.status_code == 400
    assert response.json() == expected


# Section: Get Telephone Bill ================================================

@pytest.mark.django_db
@pytest.mark.freeze_time('2011-12-13')
def test_get_calls():
    client = APIClient()

    # Subscriber A: 2212345678
    # Subscriber B: 3312345678
    # Subscriber C: 4412345678
    # Subscriber D: 5512345678

    # A -> B
    CallDetail.objects.create(
        call_id=1, source="2212345678", destination="3312345678",
        duration=1240, price=54, reference_period="10/2011",
        started_at=datetime(2011, 10, 13, 21, 57, 13, tzinfo=timezone.utc),
        ended_at=datetime(2011, 10, 13, 22, 17, 53, tzinfo=timezone.utc),
        is_completed=True)
    # 0h20m40s

    # A -> B (not completed call)
    CallDetail.objects.create(
        call_id=1, source="2212345678", destination="3312345678",
        duration=1240, price=54, reference_period="10/2011",
        started_at=datetime(2011, 10, 13, 21, 57, 13, tzinfo=timezone.utc),
        ended_at=None, is_completed=False)
    # 0h20m40s

    # A -> B
    CallDetail.objects.create(
        call_id=2, source="2212345678", destination="3312345678",
        duration=585, price=117, reference_period="11/2011",
        started_at=datetime(2011, 11, 13, 8, 30, 15, tzinfo=timezone.utc),
        ended_at=datetime(2011, 11, 13, 8, 40, 0, tzinfo=timezone.utc),
        is_completed=True)
    # 0h9m45s

    # B -> A
    CallDetail.objects.create(
        call_id=2, source="3312345678", destination="2212345678",
        duration=585, price=117, reference_period="11/2011",
        started_at=datetime(2011, 11, 13, 9, 30, 15, tzinfo=timezone.utc),
        ended_at=datetime(2011, 11, 13, 9, 40, 0, tzinfo=timezone.utc),
        is_completed=True)
    # 0h9m45s

    # A -> C
    CallDetail.objects.create(
        call_id=3, source="2212345678", destination="4412345678",
        duration=59400, price=8676, reference_period="10/2011",
        started_at=datetime(2011, 10, 13, 5, 50, 0, tzinfo=timezone.utc),
        ended_at=datetime(2011, 10, 13, 22, 20, 0, tzinfo=timezone.utc),
        is_completed=True)
    # 16h30m0s

    # C -> D
    CallDetail.objects.create(
        call_id=4, source="4412345678", destination="5512345678",
        duration=2060, price=343, reference_period="10/2011",
        started_at=datetime(2011, 10, 13, 11, 50, 0, tzinfo=timezone.utc),
        ended_at=datetime(2011, 10, 13, 12, 24, 20, tzinfo=timezone.utc),
        is_completed=True)
    # 0h34m20s

    params = {
        'number': "2212345678",
        'period': '10/2011'
    }
    response = client.get('/calls/', params, format="json")
    assert response.status_code == 200

    assert response.json() == {
        'number': '2212345678',
        'period': '10/2011',
        'call_records': [{
            'destination': '4412345678',
            'call_start_date': '2011-10-13',
            'call_start_time': '05:50:00',
            'call_duration': '16h30m0s',
            'call_price': 'R$ 86,76'
        }, {
            'destination': '3312345678',
            'call_start_date': '2011-10-13',
            'call_start_time': '21:57:13',
            'call_duration': '0h20m40s',
            'call_price': 'R$ 0,54'
        }]
    }

    params = {
        'number': "2212345678"
    }
    response = client.get('/calls/', params, format="json")
    assert response.status_code == 200

    assert response.json() == {
        'number': '2212345678',
        'period': '11/2011',
        'call_records': [{
            'destination': '3312345678',
            'call_start_date': '2011-11-13',
            'call_start_time': '08:30:15',
            'call_duration': '0h9m45s',
            'call_price': 'R$ 1,17'
        }]
    }
