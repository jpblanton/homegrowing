from urllib import response
import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from monitoring.models import GrowthStage, GrowthStageHistory, SensorData, SensorMetric
from django.core.cache import cache
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task
def top_n_average(metric: str, n: int = 5) -> float:
    metric_pk = SensorMetric.objects.get(metric__exact=metric).pk
    top = SensorData.objects.filter(metric__exact=metric_pk).order_by("-created_at")[:n]
    avg = sum(r.data for r in top) / n
    webhook_url = getattr(settings, f"{metric.upper()}_DISCORD_WEBHOOK_URL", None)
    data = {"content": f"Current {metric} average is {avg}"}
    response = requests.post(url=webhook_url, json=data)
    # pattern matching is fun and it'll be easy to build out if I need to use other status codes other ways
    match response.status_code:
        case 200 | 204:
            pass
        case _:
            logger.warning(
                f"webhook request to {webhook_url} returned status code {response.status_code}"
            )
    logger.info(f"Current {metric} average is {avg}")
    current_growth_stage = GrowthStage.objects.get(
        pk=cache.get("current_growth_stage_pk")
    )
    if metric == "humidity":
        if avg < current_growth_stage.min_humidity:
            # send message to turn on humidifier
            pass
        elif avg > current_growth_stage.max_humidity:
            # send message to turn off humidifer
            pass
    elif metric == "temperature":
        if avg < current_growth_stage.min_temperature:
            # turn on fans? idk
            pass
        elif avg > current_growth_stage.max_temperature:
            # turn off fans? idk
            pass
    return avg
