import requests
from datetime import datetime

from celery import shared_task, chain, group, chord
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from monitoring.consumers import mqttConsumer
from monitoring.models import (
    GrowthStage,
    GrowthStageHistory,
    SensorData,
    SensorMetric,
    SensorDataView,
)

logger = get_task_logger(__name__)


@shared_task
def climate_monitoring(metric: str, n: int = 5) -> None:
    # get the average then send the result to me to monitor and
    # to another function that will do the adjustments
    temp = chord(
        chain(
            top_n_average.s(metric, n)
            | group(send_update_to_discord.s(metric), adjust_climate.s(metric))
        )
    )(handle_results.s())


@shared_task
def handle_results(lst: list) -> None:
    # not sure if this is the best way, wonder if there's
    # a way to access by name
    code, url = lst[0][0]
    # pattern matching is fun and it'll be easy to build out if I need to use other status codes other ways
    match code:
        case 200 | 204:
            logger.info("successful discord send")
        case _:
            logger.warning(f"webhook request to {url} returned status code {code}")


@shared_task
def top_n_average(metric: str, n: int = 10) -> float:
    metric_pk = SensorMetric.objects.get(metric__exact=metric).pk
    top = SensorData.objects.filter(metric__exact=metric_pk).order_by("-created_at")[:n]
    avg = sum(r.data for r in top) / n
    logger.info(f"Current {metric} average is {avg}")
    # should the recent average be in cache for anything else that might need it?
    cache.set(f"{metric}-avg", avg)
    return avg


@shared_task
def send_update_to_discord(avg: float, metric: str) -> tuple[int, str]:
    webhook_url = getattr(settings, f"{metric.upper()}_DISCORD_WEBHOOK_URL", None)
    data = {"content": f"Current {metric} average is {avg}"}
    logger.info("discord URL: {}; data: {}".format(webhook_url, str(data)))
    response = requests.post(url=webhook_url, json=data)
    return response.status_code, webhook_url


@shared_task
def adjust_climate(avg: float, metric: str):
    # consider adding a return statement
    current_growth_stage = GrowthStageHistory.objects.get(
        pk=cache.get("current_growth_stage_pk")
    ).growth_stage
    channel_layer = get_channel_layer()
    if metric == "humidity":
        if avg < current_growth_stage.min_humidity:
            async_to_sync(channel_layer.group_send)(
                "humidifier.group", {"type": "humidifier.switch", "body": True}
            )
        elif avg > current_growth_stage.max_humidity:
            # send message to turn off humidifer
            async_to_sync(channel_layer.group_send)(
                "humidifier.group", {"type": "humidifier.switch", "body": False}
            )
    elif metric == "temperature":
        # want to add a check here to make sure it's on before sending off signal
        mid_temp = (
            current_growth_stage.min_temperature + current_growth_stage.max_temperature
        ) / 2
        if avg < mid_temp:
            async_to_sync(channel_layer.group_send)(
                "heater.group", {"type": "heater.switch", "body": True}
            )
        elif avg > current_growth_stage.max_temperature:
            async_to_sync(channel_layer.group_send)(
                "heater.group", {"type": "heater.switch", "body": False}
            )
    logger.info("climate adjust function finished")
    # this will possibly return something even if it's
    # an awaitable reference to the mqtt response


@shared_task
def check_lighting():
    current_growth_stage = GrowthStageHistory.objects.get(
        pk=cache.get("current_growth_stage_pk")
    ).growth_stage
    start = current_growth_stage.start_time
    end = current_growth_stage.end_time
    now = datetime.now().time()
    # as long as the lights are on analog timer
    # should consider making sure it's not in that
    # 10/15 minute zone that is slightly off
    if start < now < end:
        day = True
    else:
        day = False
    last_lux = SensorDataView.filter(metric__exact="lux").latest("created_at").data
    channel_layer = get_channel_layer()
    if day and last_lux < 1000:  # probably can make this higher
        # this means light is off and should be on
        # send error MQTT & discord messages
        async_to_sync(channel_layer.group_send)(
            "light.group", {"type": "light.error", "issue": "off during day"}
        )
    elif not day and last_lux > 500:
        # light is on and it should be off
        # send error messages as above
        async_to_sync(channel_layer.group_send)(
            "light.group", {"type": "light.error", "issue": "on at night"}
        )
