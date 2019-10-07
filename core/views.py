from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import CallDetail
from core.serializers import CallDetailSerializer, MonthlyBillSerializer


@api_view(['GET', 'POST'])
def calls(request):
    """
    List calls by subscriber and period, or create/update a call.
    """

    if request.method == 'GET':
        # BillRequestSerializer
        serializer = MonthlyBillSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        number = serializer.data['number']
        period = serializer.data['period']
        calls = CallDetail.objects.filter(
            source=number
        ).filter(
            reference_period=period
        ).filter(
            is_completed=True).order_by('started_at')

        serializer = MonthlyBillSerializer(calls, many=True)
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
