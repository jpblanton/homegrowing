from django.contrib import admin

from monitoring.models import (
    GrowthStage,
    GrowthStageHistory,
    SensorData,
    SensorHost,
    SensorMetric,
    Device,
)


class GrowthStageAdmin(admin.ModelAdmin):
    pass


class GrowthStageHistoryAdmin(admin.ModelAdmin):
    list_display = ["growth_stage", "created_at"]
    readonly_fields = ["growth_stage", "created_at"]


class SensorDataAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["host", "metric", "data", "created_at"]
    readonly_fields = ["host", "metric", "data", "created_at"]
    ordering = ["-created_at"]
    list_filter = ("host", "metric", "created_at")


class SensorHostAdmin(admin.ModelAdmin):
    pass


class SensorMetricAdmin(admin.ModelAdmin):
    pass


class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "category", "updated_at"]


admin.site.register(SensorMetric, SensorMetricAdmin)
admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(SensorHost, SensorHostAdmin)
admin.site.register(GrowthStage, GrowthStageAdmin)
admin.site.register(GrowthStageHistory, GrowthStageHistoryAdmin)
admin.site.register(Device, DeviceAdmin)
