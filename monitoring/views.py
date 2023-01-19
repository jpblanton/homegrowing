import logging

from rest_framework import generics
from django.shortcuts import reverse
from django.views.generic.edit import CreateView

from .forms import GrowthStageHistoryForm

from .models import (
    SensorHost,
    SensorMetric,
    SensorData,
    GrowthStage,
    GrowthStageHistory,
)
from .serializers import (
    SensorHostSerializer,
    SensorMetricSerializer,
    SensorDataSerializer,
    GrowthStageSerializer,
    GrowthStageHistorySerializer,
)

logger = logging.getLogger(__name__)


class SensorHostList(generics.ListAPIView):
    queryset = SensorHost.objects.all()
    serializer_class = SensorHostSerializer


class SensorHostDetail(generics.RetrieveAPIView):
    queryset = SensorHost.objects.all()
    serializer_class = SensorHostSerializer


class SensorMetricList(generics.ListAPIView):
    queryset = SensorMetric.objects.all()
    serializer_class = SensorMetricSerializer


class SensorMetricDetail(generics.RetrieveAPIView):
    queryset = SensorMetric.objects.all()
    serializer_class = SensorMetricSerializer


class SensorDataList(generics.ListAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer


class SensorDataDetail(generics.RetrieveAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer


class GrowthStageList(generics.ListAPIView):
    queryset = GrowthStage.objects.all()
    serializer_class = GrowthStageSerializer


class GrowthStageDetail(generics.RetrieveAPIView):
    queryset = GrowthStage.objects.all()
    serializer_class = GrowthStageSerializer

    def get_object(self):
        logger.info(self.kwargs)
        name = self.kwargs["name"]
        logger.info(name)
        return GrowthStage.objects.all()


class GrowthStageHistoryList(generics.ListAPIView):
    queryset = GrowthStageHistory.objects.all()
    serializer_class = GrowthStageHistorySerializer


class GrowthStageHistoryDetail(generics.RetrieveAPIView):
    queryset = GrowthStageHistory.objects.all()
    serializer_class = GrowthStageHistorySerializer


class GrowthStageHistoryCreate(CreateView):
    model = GrowthStageHistory
    template_name = "growthstagehistorycreate.html"
    form_class = GrowthStageHistoryForm

    def get_success_url(self) -> str:
        return reverse("home")
