from datetime import datetime

from rest_framework import serializers
from core.models import CallDetail


class CallDetailSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        call_id = data.get("call_id")
        call_type = data.get("type")
        timestamp = data.get("timestamp")
        source = data.get("source")
        destination = data.get("destination")

        return {
            'call_id': call_id,
            'source': source,
            'destination': destination,
            # 'duration': duration,
            # 'price': price,
            # 'reference_period': reference_period,
            'started_at': datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ"),
            # 'ended_at': ended_at,
            # 'is_completed': is_completed,
        }

    def to_representation(self, obj):
        return {}

    def create(self, validated_data):
        return CallDetail.objects.create(**validated_data)
