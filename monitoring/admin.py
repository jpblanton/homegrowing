from django.contrib import admin

from monitoring.models import SensorData, SensorHost, SensorMetric

admin.site.register(SensorMetric)
admin.site.register(SensorData)
admin.site.register(SensorHost)
