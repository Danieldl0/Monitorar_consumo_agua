from django import forms

from monitora_consumo_agua.models.consumo_agua import ConsumoAgua


class ConsumoAguaForm(forms.ModelForm):
    class Meta:
        model = ConsumoAgua
        fields = (
            'sensor', 'consumo', 'data_consumo',
        )