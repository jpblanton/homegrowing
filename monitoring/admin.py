from django.contrib import admin

from monitoring.models import (
    GrowthStage,
    GrowthStageHistory,
    SensorData,
    SensorHost,
    SensorMetric,
    Device,
)

admin.site.register(SensorMetric)
admin.site.register(SensorData)
admin.site.register(SensorHost)
admin.site.register(GrowthStage)
admin.site.register(GrowthStageHistory)
admin.site.register(Device)
