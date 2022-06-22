import asyncio

from mqttasgi.consumers import MqttConsumer
from channels.db import database_sync_to_async
import django
from django.conf import settings

from .models import SensorHost, SensorData, SensorMetric


class mqttConsumer(MqttConsumer):
    async def connect(self):
        subs = [self.subscribe(t, 2) for t in settings.MQTT_TOPIC_SUBS]
        await asyncio.wait(subs)

    async def receive(self, mqtt_message):
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

    async def disconnect(self):
        await self.unsubscribe("my/testing/topic")

    @database_sync_to_async
    def insert_metric(self, payload, place, device, metric):
        value = round(float(payload), 3)
        host = "_".join([place, device])
        SensorHost.create(host)
        SensorMetric.create(metric)
