import uuid
import string
from datetime import datetime

from django.db import models
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class SensorData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey("SensorHost", models.DO_NOTHING)
    metric = models.ForeignKey("SensorMetric", models.DO_NOTHING)
    data = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{}|{}|{}".format(self.host, self.metric, self.data)

    # class Meta:
    #    get_latest_by = "created_at"


class SensorHost(models.Model):
    # want to have the whole host, room_device, as well as fields for both
    # not perfectly normalized but whatever
    # override save?
    host = models.CharField(unique=True, max_length=64)
    # room = models.CharField(max_length=64)
    # device = models.CharField(max_length=64)

    # might need super(SensorHost, self) based on
    # https://stackoverflow.com/questions/30586994/django-model-save-computed-value-in-a-model-field

    # def save(self, *args, **kwargs):
    #    self.room, self.device = self.host.split("_")
    #    super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.host


class SensorMetric(models.Model):
    metric = models.CharField(unique=True, max_length=255)

    def __str__(self) -> str:
        return self.metric


class GrowthStage(models.Model):
    name = models.CharField(unique=True, max_length=64)
    min_humidity = models.FloatField()
    max_humidity = models.FloatField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    light_hours = models.PositiveIntegerField(validators=[MaxValueValidator(24)])
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    # important to note this will only work in the admin form
    def clean(self) -> None:
        dt_start = datetime.combine(datetime.today(), self.start_time)
        dt_end = datetime.combine(datetime.today(), self.end_time)
        timediff = dt_end - dt_start
        # constant for seconds in an hour?
        hourdiff = timediff.seconds / 3600
        if hourdiff != self.light_hours:
            raise ValidationError(
                "Start and end times must match duration in light_hours. Calculated duration is {} hours".format(
                    hourdiff
                )
            )


class GrowthStageHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    growth_stage = models.ForeignKey("GrowthStage", models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.growth_stage.name

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        cache.set("growth_stage_changed", True, None)  # don't think we need this tbh
        cache.set("current_growth_stage_pk", self.pk, None)

    class Meta:
        get_latest_by = "created_at"


class MQTTMessage(models.Model):
    topic = models.CharField(max_length=128)
    payload = models.TextField()
    qos = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payload


class Device(models.Model):
    # should add a type column for easier filtering
    # make it optional so it's something I can tweak
    # we'll probably have it default to the name
    # with numbers stripped but it should be editable
    name = models.CharField(max_length=128, unique=True)
    status = models.CharField(max_length=64)
    category = models.CharField(max_length=64, null=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if self.category == "":
            self.category = self.name.split("_")[-1].rstrip(string.digits)
        super().save(*args, **kwargs)


class SensorDataView(models.Model):
    data_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    data = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "monitoring_sensordata_view"
