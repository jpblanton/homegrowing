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


# growth stages
# id, name, lo hum, hi hum, lo temp, hi temp
# should be limited to the growth phases we have

# historical_growth_stages
# every time it switches stage_id gets pushed here
# can I have a flag in growth_stages table like is_current?

# get_current_growth_stage should be a util
