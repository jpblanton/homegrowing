import asyncio

from mqttasgi.consumers import MqttConsumer
from channels.db import database_sync_to_async
import django
from django.conf import settings
from django.db import IntegrityError

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
        # confirm this field
        unsubs = [self.unsubscribe(t) for t in self.subscribed_topics]
        await asyncio.wait(unsubs)

    @database_sync_to_async
    def insert_measure(self, payload, place, device, metric):
        value = round(float(payload), 3)
        host = "_".join([place, device])
        # info level log about host/metric creation
        # debug for each data insert
        try:
            host_obj = SensorHost.objects.create(host=host)
        except IntegrityError:
            # logger.log('already exists')
            print("host already exists")
            host_obj = SensorHost.objects.filter(host=host)[0]
        try:
            metric_obj = SensorMetric.objects.create(metric=metric)
        except IntegrityError:
            print("metric already exists")
            metric_obj = SensorMetric.objects.filter(metric=metric)[0]
        SensorData.objects.create(host=host_obj, metric=metric_obj, data=value)
