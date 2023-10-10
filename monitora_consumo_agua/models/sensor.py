from django.db import models

# Create your models here.

class Sensor(models.Model):

    usuario = models.ForeignKey(
        to='auth.User',
        on_delete=models.PROTECT,
        related_name='sensores_usuarios',
        null=True
    )
    nome = models.CharField(
        max_length=100,
        null=True
    )
    codigo = models.CharField(
        max_length=40,
        null=True
    )


    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'

    def __str__(self):
        return f'{self.nome}'