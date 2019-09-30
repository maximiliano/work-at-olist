from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import CallDetail
from core.serializers import CallDetailSerializer


@api_view(['POST'])
def calls(request):
    """
    List calls by subscriber and period, or create/update a call.
    """

    if request.method == 'POST':
        try:
            call = CallDetail.objects.get(call_id=request.data.get('call_id'))
            serializer = CallDetailSerializer(call, data=request.data)
        except CallDetail.DoesNotExist:
            serializer = CallDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
