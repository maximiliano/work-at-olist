from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import CallDetail
from core.serializers import CallDetailSerializer


@api_view(['GET', 'POST'])
def calls(request):
    """
    List calls by subscriber and period, or create/update a call.
    """

    if request.method == 'GET':
        number = request.query_params['subscriber_telephone_number']
        reference_period = request.query_params.get('reference_period')

        if not reference_period:
            last_month = (datetime.now().replace(day=1) - timedelta(days=1))
            reference_period = last_month.strftime("%m/%Y")

        calls = CallDetail.objects.filter(
            source=number
        ).filter(
            reference_period=reference_period
        ).filter(
            is_completed=True).order_by('started_at')

        serializer = CallDetailSerializer(calls, many=True)
        return Response({
            'subscriber_telephone_number': number,
            'reference_period': reference_period,
            'call_records': serializer.data
        })

    if request.method == 'POST':
        try:
            call = CallDetail.objects.get(call_id=request.data.get('call_id'))
            serializer = CallDetailSerializer(call, data=request.data)
        except CallDetail.DoesNotExist:
            serializer = CallDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
