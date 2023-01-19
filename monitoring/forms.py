from django import forms
from .models import GrowthStageHistory


class GrowthStageHistoryForm(forms.ModelForm):
    class Meta:
        model = GrowthStageHistory
        fields = "__all__"
        labels = {
            "growth_stage": ("Update growth stage"),
        }
