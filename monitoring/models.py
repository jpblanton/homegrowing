from django.db import models


class SensorData(models.Model):
    host = models.ForeignKey("SensorHost", models.DO_NOTHING)
    metric = models.ForeignKey("SensorMetric", models.DO_NOTHING)
    data = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return "{}|{}|{}".format(self.host, self.metric, self.data)


class SensorHost(models.Model):
    host = models.CharField(unique=True, max_length=64)

    def __str__(self) -> str:
        return self.host


class SensorMetric(models.Model):
    metric = models.CharField(unique=True, max_length=255)

    def __str__(self) -> str:
        return self.metric
