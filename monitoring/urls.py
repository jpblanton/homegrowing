from django.urls import path

from .views import (
    SensorHostList,
    SensorHostDetail,
    SensorMetricList,
    SensorMetricDetail,
    SensorDataList,
    SensorDataDetail,
    GrowthStageList,
    GrowthStageDetail,
    GrowthStageHistoryList,
    GrowthStageHistoryDetail,
)


urlpatterns = [
    path("sensorhosts/", SensorHostList.as_view(), name="sensor_host_list"),
    path(
        "sensorhosts/<int:pk>/", SensorHostDetail.as_view(), name="sensor_host_detail"
    ),
    path("sensormetrics/", SensorMetricList.as_view(), name="sensor_metric_list"),
    path(
        "sensormetrics/<int:pk>/",
        SensorMetricDetail.as_view(),
        name="sensor_metric_detail",
    ),
    path("sensordata/", SensorDataList.as_view(), name="sensor_data_list"),
    path("sensordata/<int:pk>", SensorDataDetail.as_view(), name="sensor_data_detail"),
    path("growthstages/", GrowthStageList.as_view(), name="growth_stage_list"),
    path(
        "growthstages/<str:name>",
        GrowthStageDetail.as_view(),
        name="growth_stage_detail",
    ),
    path(
        "growthstagehistories/",
        GrowthStageHistoryList.as_view(),
        name="growth_stage_history_list",
    ),
    path(
        "growthstagehistories/<int:pk>",
        GrowthStageHistoryDetail.as_view(),
        name="growth_stage_history_detail",
    ),
]
