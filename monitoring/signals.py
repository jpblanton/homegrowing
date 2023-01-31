from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Device

@receiver(post_save, sender=Device)
def send_status(sender, instance, created, **kwargs):
    # async_to_sync(client.send)
    # settings['MQTT_TOPICS'][instance.name + '_status']
    pass
