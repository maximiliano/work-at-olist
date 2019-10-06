from datetime import date, datetime, timedelta
import re

from django.utils.datastructures import MultiValueDictKeyError

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
        try:
            number = request.query_params['number']
        except MultiValueDictKeyError:
            error = {'number': 'This field is required.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        period = request.query_params.get('period')
        if not period:
            last_month = (datetime.now().replace(day=1) - timedelta(days=1))
            period = last_month.strftime("%m/%Y")

        if not re.match("^\d{10}$|^\d{11}$", number):
            return Response({
                'number':
                    ('number '
                     'must be a string of 10 or 11 digits')},
                status=status.HTTP_400_BAD_REQUEST)

        if not re.match("^\d{2}/\d{4}$", period):
            return Response({
                'period': 'period must be in the format: "MM/YYYY"'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate if period is a closed period (previous month)
        current_month = date.today().replace(day=1)
        period_date = datetime.strptime(period, "%m/%Y").date()
        if period_date >= current_month:
            return Response({
                'period': 'period must be of a closed (previous) month'
            }, status=status.HTTP_400_BAD_REQUEST)

        calls = CallDetail.objects.filter(
            source=number
        ).filter(
            reference_period=period
        ).filter(
            is_completed=True).order_by('started_at')

        serializer = CallDetailSerializer(calls, many=True)
        return Response(
            {
                'number': number,
                'period': period,
                'call_records': serializer.data
            },
            status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            call = CallDetail.objects.get(call_id=request.data.get('call_id'))
            serializer = CallDetailSerializer(call, data=request.data)
        except CallDetail.DoesNotExist:
            serializer = CallDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
