from django.urls import path

from .views import HomePageView
from monitoring.views import GrowthStageHistoryCreate

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]
