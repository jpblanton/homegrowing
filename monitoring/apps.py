from django.apps import AppConfig
from django.core.cache import cache


class MonitoringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monitoring"

    def ready(self):
        # cache.set("growth_stage_changed", False, None)
        # from .models import GrowthStageHistory

        # current_growth_stage = GrowthStageHistory.objects.latest("created_at")
        # cache.set("current_growth_stage_pk", current_growth_stage.pk, None)
        pass
