from datetime import datetime, timezone
import re

from rest_framework import serializers
from core.models import CallDetail
from core.utils import get_price, format_duration


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
            date = date.replace(tzinfo=timezone.utc)
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

        validated_data = {
            'call_id': call_id,
        }

        if call_type == "start":
            validated_data['source'] = source
            validated_data['destination'] = destination
            validated_data['started_at'] = date
        elif call_type == "end":
            validated_data['ended_at'] = date
            validated_data['reference_period'] = date.strftime("%m/%Y")

        return validated_data

    def to_representation(self, obj):
        return {
            'destination': obj.destination,
            'call_start_date': obj.started_at.strftime('%Y-%m-%d'),
            'call_start_time': obj.started_at.strftime('%H:%M:%S'),
            'call_duration': format_duration(obj.duration),
            'call_price': 'R$ {:.2f}'.format(obj.price / 100).replace('.', ',')
        }

    def create(self, validated_data):
        return CallDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if self.initial_data["type"] == "start":
            instance.source = validated_data['source']
            instance.destination = validated_data['destination']
            instance.started_at = validated_data['started_at']

            # If instance already saved the "end" portion of the call,
            # mark it as complete and calculate duration
            if (instance.ended_at):
                instance.is_completed = True
                instance.duration = (
                    instance.ended_at - instance.started_at).seconds

        elif self.initial_data["type"] == "end":
            instance.ended_at = validated_data['ended_at']
            instance.reference_period = validated_data['reference_period']

            # If instance already saved the "start" portion of the call,
            # mark it as complete and calculate duration
            if (instance.started_at):
                instance.is_completed = True
                instance.duration = (
                    instance.ended_at - instance.started_at).seconds

        instance.price = get_price(instance.started_at, instance.ended_at)

        instance.save()
        return instance
