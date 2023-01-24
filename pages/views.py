from typing import Any
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.core.cache import cache

from monitoring.models import GrowthStageHistory
from monitoring.models import SensorData
from monitoring.forms import GrowthStageHistoryForm


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request):
        form = GrowthStageHistoryForm()
        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = GrowthStageHistoryForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=True)
            return redirect("home")

    def get_success_url(self) -> str:
        return reverse("home")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            context["current_stage"] = GrowthStageHistory.objects.latest()
        except:
            context["current_stage"] = None

        context["avg_temp"] = cache.get("temperature-avg", None)
        context["avg_humidity"] = cache.get("humidity-avg", None)
        try:
            context["latest_temp"] = SensorData.objects.filter(
                metric__metric__exact="temperature"
            )[-1].data
        except:
            context["latest_temp"] = None
        try:
            context["latest_humidity"] = SensorData.objects.filter(
                metric__metric__exact="humidity"
            )[-1].data
        except:
            context["latest_humidity"] = None

        return context
