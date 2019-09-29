from django.db import models


class CallDetail(models.Model):
    # Call Id from telephone central
    call_id = models.IntegerField()
    # Phone number that started the call
    source = models.CharField(max_length=11, null=True)
    # Phone number that received the call
    destination = models.CharField(max_length=11, null=True)

    # Duration is stored in seconds for easier formatting
    duration = models.IntegerField(null=True)
    # Price is stored in cents for more acurate currency handling
    price = models.IntegerField(null=True)

    # month/year format: MM/YYYY, defined by the time the call ended
    reference_period = models.CharField(max_length=7, null=True)
    # Call start datetime in UTC
    started_at = models.DateTimeField(null=True)
    # Call end datetime in UTC
    ended_at = models.DateTimeField(null=True)

    # Field to tell if start and end records where filled in the db record
    is_completed = models.BooleanField(default=False)
