def get_price(start_date, end_date):
    """
    Calculate price of a call based on start and end times

    The call price depends on fixed charges, duration, time of the day.
    There is no fractioned charge, it applies to each completed 60 seconds.

    There are two tariff times:

    1. Standard time call - between 6h00 and 22h00 (excluding):
        - Standing charge: R$ 0,36
        - Call charge/minute: R$ 0,09
    2. Reduced tariff time call - between 22h00 and 6h00 (excluding):
        - Standing charge: R$ 0,36
        - Call charge/minute: R$ 0,00
    """

    # Calculations if the call started and ended in the same day
    if start_date.day == end_date.day:
        reduced_tariff = (
            start_date.hour >= 22 and end_date.hour >= 22 or
            start_date.hour < 6 and end_date.hour < 6)

        if reduced_tariff:
            # Charge only Standing charge
            return 36

        if start_date.hour < 6:
            start_date = start_date.replace(hour=6, minute=0, second=0)
        if end_date.hour >= 22:
            end_date = end_date.replace(hour=22, minute=0, second=0)

        billed_minutes = (end_date - start_date).seconds // 60

        return billed_minutes * 9 + 36

    # Calculations if the call ended in a following day
    if end_date.day == start_date.day + 1:
        if start_date.hour >= 22 and end_date.hour < 6:
            # Charge only Standing charge
            return 36

        billed_minutes = 0

        # Day 1 minutes
        if start_date.hour >= 6 and start_date.hour < 22:
            proxy_end_date = start_date.replace(hour=22, minute=0, second=0)
            billed_minutes += (proxy_end_date - start_date).seconds // 60

        # Day 2 minutes
        if end_date.hour >= 6 and end_date.hour < 22:
            proxy_start_date = start_date.replace(hour=6, minute=0, second=0)
            billed_minutes += (end_date - proxy_start_date).seconds // 60

        return billed_minutes * 9 + 36

    return 36
