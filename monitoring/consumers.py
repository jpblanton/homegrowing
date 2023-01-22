import asyncio
import logging

from mqttasgi.consumers import MqttConsumer
from channels.db import database_sync_to_async
import django
from django.conf import settings
from django.db import IntegrityError

from .models import SensorHost, SensorData, SensorMetric, MQTTMessage


logger = logging.getLogger(__name__)


class mqttConsumer(MqttConsumer):
    # Class for creating a consumer of MQTT messages
    # This controls what happens when we receive MQTT messages
    # Which is how most of our sensors communicate with the server
    async def connect(self) -> None:
        subs = [self.subscribe(t, 2) for t in settings.MQTT_TOPICS.values()]
        await asyncio.wait(subs)
        await self.channel_layer.group_add("humidifier.group", self.channel_name)

    async def receive(self, mqtt_message: dict) -> None:
        # should we create a table to log all messages topic/payload/qos?
        # also need to start making all messages qos 2
        topic = mqtt_message["topic"]
        payload = mqtt_message["payload"]
        qos = mqtt_message["qos"]
        message = await database_sync_to_async(MQTTMessage.objects.create)(
            topic=topic, payload=payload, qos=qos
        )
        # consider adding a config setting to contain list of metrics
        # this will probably soon have "lux" as a metric
        # lights become device and sensor: device says if they're on or off
        # while sensor tells us the actual brightness level
        # maybe a celery task that runs when lux is updated
        # checking light level against on/off status of device
        match mqtt_message["topic"].split("/"):
            case [place, device, "temperature" | "humidity" as metric]:
                await self.insert_measure(payload, place, device, metric)
            case [place, device, "error" | "warning" as issue]:
                pass
            case _:
                logger.info(mqtt_message["topic"])
                pass

    # if the dict key is just the topic with a different sep
    # is this any better?
    # nested dict
    async def humidifier_switch(self, event):
        await self.publish(
            settings.MQTT_TOPICS["tent1_humidifier_status"], event["body"]
        )

    async def disconnect(self) -> None:
        # confirm this field
        unsubs = [self.unsubscribe(t) for t in self.subscribed_topics]
        await asyncio.wait(unsubs)

    @database_sync_to_async
    def insert_measure(
        self, payload: str | bytes, place: str, device: str, metric: str
    ) -> None:
        value = round(float(payload), 3)
        host = "_".join([place, device])
        # info level log about host/metric creation
        # debug for each data insert
        host_obj, host_created = SensorHost.objects.get_or_create(host=host)
        metric_obj, metric_created = SensorMetric.objects.get_or_create(metric=metric)
        if not host_created:
            print("host already exists")
        if not metric_created:
            print("metric already exists")
        SensorData.objects.create(host=host_obj, metric=metric_obj, data=value)
