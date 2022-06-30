import asyncio

from mqttasgi.consumers import MqttConsumer
from channels.db import database_sync_to_async
import django
from django.conf import settings
from django.db import IntegrityError

from .models import SensorHost, SensorData, SensorMetric


class mqttConsumer(MqttConsumer):
    async def connect(self) -> None:
        subs = [self.subscribe(t, 2) for t in settings.MQTT_TOPIC_SUBS]
        await asyncio.wait(subs)
        await self.channel_layer.group_add("humidifier.group", self.channel_name)

    async def receive(self, mqtt_message: dict) -> None:
        topic = mqtt_message["topic"]
        payload = mqtt_message["payload"]
        qos = mqtt_message["qos"]
        print("Received a message at topic:", topic)
        print("With payload", payload)
        print("And QOS:", qos)
        match mqtt_message["topic"].split("/"):
            case [place, device, "temperature" | "humidity" as metric]:
                await self.insert_measure(payload, place, device, metric)
        print("inserted")

    async def humidifier_switch(self, event):
        await self.publish("tent1/humidifier/status", event["body"])

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
