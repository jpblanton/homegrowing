from django.urls import path

from .views import HomePageView, grafana_view
from monitoring.views import GrowthStageHistoryCreate

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("grafana/", grafana_view, name="grafana"),
]
