from rest_framework import serializers
from ..models import ConsumoAgua


class CadastroConsumoSerializer(serializers.ModelSerializer):
    sensor_id = serializers.IntegerField(
        required=True,
    )
    consumo = serializers.IntegerField(
        required=True,
    )

    class Meta:
        model =  ConsumoAgua
        fields = ("sensor_id", "consumo",)
