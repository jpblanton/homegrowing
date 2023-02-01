from typing import Any
import logging

from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from monitoring.models import GrowthStageHistory
from monitoring.models import SensorData, Device
from monitoring.forms import GrowthStageHistoryForm

logger = logging.getLogger(__name__)


def grafana_view(request):
    # 127.0.1.1 works but only on wsl
    # hoping localhost holds for both
    response = redirect("http://localhost:3000")
    return response


class FanTriggerView(TemplateView):
    template_name = "fans.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["fans"] = Device.objects.filter(category="fan")
        context["keys"] = "+".join(context.keys())
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    # 1/30/23: with the hx-include it sends a dict of the fans
    # but only includes them if they're 'on'
    # hopefully we can improve that but for now that's the way it works
    def post(self, request):
        device_name = request.headers.get(
            "Hx-Trigger-Name", "Error: Missing Trigger Name"
        )
        power = None
        match len(request.POST):
            case 1:
                power = True
            case 0:
                power = False
            case _:
                # this means something is wrong
                logger.exception(vars(request))
                power = None
                return redirect("fans")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "fan.group",
            {"type": "fan.switch", "body": {"device": device_name, "value": power}},
        )
        return redirect("fans")


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
            current_stage = GrowthStageHistory.objects.latest()
            context["current_stage"] = current_stage
        except:
            context["current_stage"] = None

        context["fans"] = Device.objects.filter(category="fan")
        context["avg_temp"] = cache.get("temperature-avg", None)
        context["avg_humidity"] = cache.get("humidity-avg", None)
        try:
            context["avg_temp"] = round(context["avg_temp"], 3)
            context["avg_humidity"] = round(context["avg_humidity"], 3)
        except TypeError:
            context["temp_ok"] = False
            context["humidity_ok"] = False
            pass
        else:
            context["temp_ok"] = (
                current_stage.growth_stage.min_temperature
                < context["avg_temp"]
                < current_stage.growth_stage.max_temperature
            )
            context["humidity_ok"] = (
                current_stage.growth_stage.min_humidity
                < context["avg_humidity"]
                < current_stage.growth_stage.max_humidity
            )
        try:
            context["latest_temp"] = (
                SensorData.objects.filter(metric__metric__exact="temperature")
                .order_by("created_at")
                .last()
            )
            context["latest_humidity"] = (
                SensorData.objects.filter(metric__metric__exact="humidity")
                .order_by("created_at")
                .last()
            )
        except SensorData.DoesNotExist:
            context["latest_temp"] = None
            context["latest_humidity"] = None

        return context
