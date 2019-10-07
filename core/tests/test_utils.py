from datetime import datetime, timezone
from core.utils import format_duration, get_price


def test_get_price_same_day_call():
    """Test get_price function for calls that ends in the same day"""

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


def test_get_price_with_reduced_tariff():
    """Test get price method for calls that ends in another day"""

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
    """Test format_duration function for various duration"""

    assert format_duration(0) == "0h0m0s"
    assert format_duration(30) == "0h0m30s"
    assert format_duration(60) == "0h1m0s"
    assert format_duration(85) == "0h1m25s"
    assert format_duration(600) == "0h10m0s"
    assert format_duration(9200) == "2h33m20s"
