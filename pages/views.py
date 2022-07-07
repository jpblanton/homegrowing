from typing import Any
from django.views.generic import TemplateView

from monitoring.models import GrowthStageHistory


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_stage"] = GrowthStageHistory.objects.latest()
        return context
