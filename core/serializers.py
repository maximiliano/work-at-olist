from datetime import datetime
import re

from rest_framework import serializers
from core.models import CallDetail


class CallDetailSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        call_id = data.get("call_id")
        call_type = data.get("type")
        timestamp = data.get("timestamp")
        source = data.get("source")
        destination = data.get("destination")

        # Validate required fields
        if not call_id:
            raise serializers.ValidationError({
                'call_id': 'This field is required.'
            })

        if not call_type:
            raise serializers.ValidationError({
                'type': 'This field is required.'
            })

        if not timestamp:
            raise serializers.ValidationError({
                'timestamp': 'This field is required.'
            })

        if call_type == "start" and not source:
            raise serializers.ValidationError({
                'source': 'This field is required if call type is start.'
            })

        if call_type == "start" and not destination:
            raise serializers.ValidationError({
                'destination': 'This field is required if call type is start.'
            })

        # Validate field types
        if not isinstance(timestamp, str):
            raise serializers.ValidationError({
                'timestamp': 'timestamp must be a string'
            })

        if not isinstance(call_id, int):
            raise serializers.ValidationError({
                'call_id': 'call_id must be an integer'
            })

        if call_type == "start":
            if not isinstance(source, str):
                raise serializers.ValidationError({
                    'source': 'source must be a string'
                })

            if not isinstance(destination, str):
                raise serializers.ValidationError({
                    'destination': 'destination must be a string'
                })

        # Validate field formats
        if call_type not in ["start", "end"]:
            raise serializers.ValidationError({
                'type':
                    'type must be a string with value "start" or "end".'
            })

        try:
            date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise serializers.ValidationError({
                'timestamp':
                    'timestamp must be in the format: "YYYY-MM-DDThh:mm:ssZ"'
            })

        if call_type == "start":
            if not re.match("^\d{10}$|^\d{11}$", source):
                raise serializers.ValidationError({
                    'source':
                        'source must be a string of 10 or 11 digits'
                })

            if not re.match("^\d{10}$|^\d{11}$", destination):
                raise serializers.ValidationError({
                    'destination':
                        'destination must be a string of 10 or 11 digits'
                })

        return {
            'call_id': call_id,
            'source': source,
            'destination': destination,
            # 'duration': duration,
            # 'price': price,
            # 'reference_period': reference_period,
            'started_at': date,
            # 'ended_at': ended_at,
            # 'is_completed': is_completed,
        }

    def to_representation(self, obj):
        return {}

    def create(self, validated_data):
        return CallDetail.objects.create(**validated_data)
