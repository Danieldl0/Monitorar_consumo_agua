from django import forms

from monitora_consumo_agua.models.sensor import Sensor


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = (
           'nome',  'codigo',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
