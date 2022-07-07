from rest_framework import serializers

from .models import (
    SensorHost,
    SensorMetric,
    SensorData,
    GrowthStage,
    GrowthStageHistory,
)


class SensorHostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "host")
        model = SensorHost


class SensorMetricSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "metric")
        model = SensorMetric


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "host", "metric", "data", "created_at")
        model = SensorData


class GrowthStageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "min_humidity",
            "max_humidity",
            "min_temperature",
            "max_temperature",
        )
        model = GrowthStage


class GrowthStageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "growth_stage", "created_at")
        model = GrowthStageHistory
