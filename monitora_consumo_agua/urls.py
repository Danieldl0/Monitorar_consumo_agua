from django.urls import path

from .views import *


urlpatterns = [
    path('consumo/', ConsumoView.as_view(), name='consumo_view'),
    path('cadastro/', CadastrarConsumoView.as_view(), name='cadastro_consumo'),
    path('cadastro/sensor', CadastrarSensorView.as_view(), name='cadastro_sensor'),
]
