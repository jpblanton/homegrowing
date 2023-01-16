from typing import Any
from django.views.generic import TemplateView
from django.core.cache import cache

from monitoring.models import GrowthStageHistory
from monitoring.models import SensorData


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            context["current_stage"] = GrowthStageHistory.objects.latest()
        except:
            context["current_stage"] = None
        
        context["avg_temp"] = cache.get("temperature-avg", None)
        context["avg_humidity"] = cache.get("humidity-avg", None)
        try:
            context["latest_temp"] = SensorData.objects.filter(metric__metric__exact="temperature")
        except:
            context["latest_temp"] = None
        try:
            context["latest_humidity"] = SensorData.objects.filter(metric__metric__exact="humidity")
        except:
            context["latest_humidity"] = None
        
        return context
