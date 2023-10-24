from django.db import models

# Create your models here.

class ConsumoAgua(models.Model):

    sensor = models.ForeignKey(
        to='monitora_consumo_agua.Sensor',
        on_delete=models.PROTECT,
        related_name='consumos_sensores',
        null=True
    )
    consumo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    data_consumo = models.DateField(
        #auto_now_add=True,
        null=True
    )

    class Meta:
        verbose_name = 'Consumo de Água'
        verbose_name_plural = 'Consumos de Água'
