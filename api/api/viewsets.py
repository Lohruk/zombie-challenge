from rest_framework.filters import OrderingFilter

from .serializers import ReadSurvivorSerializer, WriteSurvivorSerializer, \
    UpdateCoordinateSerializer, UpdateInfectionSerializer, TradeItemsSerializer, ReadReportSerializer, WriteReportSerializer
from rest_framework.viewsets import ModelViewSet
from api.models import Survivor, Report
from drf_rw_serializers import generics


class SurvivorViewSet(generics.ListCreateAPIView):
    read_serializer_class = ReadSurvivorSerializer
    write_serializer_class = WriteSurvivorSerializer
    queryset = Survivor.objects.filter(infection=False)
    filter_backends = (OrderingFilter,)
    ordering = ['name']


class SurvivorCoordinateViewSet(generics.UpdateAPIView):
    serializer_class = UpdateCoordinateSerializer
    queryset = Survivor.objects.all()
    ordering = ['name']


class UpdateInfectionViewSet(generics.UpdateAPIView):
    serializer_class = UpdateInfectionSerializer
    queryset = Survivor.objects.all()


class ReportViewSet(generics.ListCreateAPIView):
    read_serializer_class = ReadReportSerializer
    write_serializer_class = WriteReportSerializer
    queryset = Report.objects.all()


class TradeViewSet(generics.UpdateAPIView):
    serializer_class = TradeItemsSerializer
    queryset = Survivor.objects.all()
