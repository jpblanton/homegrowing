from celery import shared_task
from celery.utils.log import get_task_logger
from monitoring.models import SensorData, SensorMetric
from config.pub import publish_data


logger = get_task_logger(__name__)


@shared_task
def top_n_average(metric, n=5):
    metric_pk = SensorMetric.objects.get(metric__exact=metric).pk
    top = SensorData.objects.filter(metric__exact=metric_pk).order_by("-created_at")[:n]
    avg = sum(r.data for r in top) / n
    logger.info("Current average is {}".format(avg))
    # this will publish to the humidifier controller either on or off
    publish_data(avg, "testing")
    return avg
