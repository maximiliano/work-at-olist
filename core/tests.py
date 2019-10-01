from datetime import datetime, timezone

import pytest
from rest_framework.test import APIClient

from core.models import CallDetail
from core.utils import format_duration, get_price


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

    client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 1

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

    client.post('/calls/', call_data, format='json')
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

    client.post('/calls/', call_data, format='json')
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
        'source': 'source must be a string of 10 or 11 digits'}

    call_data['source'] = "9876ABC54321"
    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'source': 'source must be a string of 10 or 11 digits'}


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
        'destination': 'destination must be a string of 10 or 11 digits'}

    call_data["destination"] = "(11)12345678"
    response = client.post('/calls/', call_data, format='json')
    assert CallDetail.objects.count() == 0
    assert response.json() == {
        'destination': 'destination must be a string of 10 or 11 digits'}


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
    assert response.json() == {}


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

    client.post('/calls/', call_data, format='json')

    call_data = {
        "id": 1,
        "call_id": 11,
        "type": "end",
        "timestamp": "2016-02-29T05:40:00Z",
    }

    client.post('/calls/', call_data, format='json')

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


def test_get_price():
    """Test get price method in several situations"""

    # Same day tests

    # Call in Reduced tariff time by morning
    start_date = datetime(2011, 12, 13, 4, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 5, 10, 0, tzinfo=timezone.utc)
    assert get_price(start_date, end_date) == 36

    # Call in Reduced tariff time by night
    start_date = datetime(2011, 12, 13, 22, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 22, 10, 0, tzinfo=timezone.utc)
    assert get_price(start_date, end_date) == 36

    # Call Standard time call with 10 minutes duration
    start_date = datetime(2011, 12, 13, 15, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 15, 10, 0, tzinfo=timezone.utc)
    # 10 minutes * 0,09 + 0,36
    assert get_price(start_date, end_date) == 126

    # Call Standard time call with 4 minutes and 40 seconds duration
    start_date = datetime(2011, 12, 13, 15, 5, 20, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 15, 10, 0, tzinfo=timezone.utc)
    # 4 minutes * 0,09 + 0,36
    assert get_price(start_date, end_date) == 72

    # Call starting in Reduced tariff time and ending in Standard time
    start_date = datetime(2011, 12, 13, 5, 57, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 6, 3, 30, tzinfo=timezone.utc)
    # 3 minutes * R$ 0,09 + 0,36
    assert get_price(start_date, end_date) == 63

    # Call starting in Standard time and ending in Reduced tariff time
    start_date = datetime(2011, 12, 13, 21, 57, 13, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 22, 17, 53, tzinfo=timezone.utc)
    # 2 minutes * R$ 0,09 + 0,36
    assert get_price(start_date, end_date) == 54

    # Call starting in Reduced t. by morning and ending in Reduced t. by night
    start_date = datetime(2011, 12, 13, 5, 50, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 13, 22, 20, 0, tzinfo=timezone.utc)
    # 960 minutes * R$ 0,09 + 0,36
    assert get_price(start_date, end_date) == 8676

    # Different day tests

    # Call starting in Reduced t. night and ending in the next day Reduced t.
    start_date = datetime(2011, 12, 13, 23, 15, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 14, 3, 45, 0, tzinfo=timezone.utc)
    assert get_price(start_date, end_date) == 36

    # Call starting in Reduced t. night and ending in the next day Standard t.
    start_date = datetime(2011, 12, 13, 23, 15, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 14, 6, 45, 0, tzinfo=timezone.utc)
    # 45 minutes * R$ 0,09 + 0,36
    assert get_price(start_date, end_date) == 441

    # Call starting in Standard t. night and ending in the next day Reduced t.
    start_date = datetime(2011, 12, 13, 21, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 14, 5, 45, 0, tzinfo=timezone.utc)
    # 60 minutes * R$ 0,09 + 0,36
    assert get_price(start_date, end_date) == 576

    # Call starting in Standard t. night and ending in the next day Standard t.
    start_date = datetime(2011, 12, 13, 21, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2011, 12, 14, 7, 0, 0, tzinfo=timezone.utc)
    # 120 minutes * R$ 0,09 + 0,36
    assert get_price(start_date, end_date) == 1116


def test_format_duration():
    assert format_duration(0) == "0h0m0s"
    assert format_duration(30) == "0h0m30s"
    assert format_duration(60) == "0h1m0s"
    assert format_duration(85) == "0h1m25s"
    assert format_duration(600) == "0h10m0s"
    assert format_duration(9200) == "2h33m20s"
