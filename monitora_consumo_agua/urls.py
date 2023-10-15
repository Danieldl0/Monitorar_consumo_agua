from django.urls import path

from .views import *


urlpatterns = [
    path('', ConsumoView.as_view(), name='consumo_view'),
    path('cadastro/teste/', CadastrarConsumoView.as_view(), name='cadastro_consumo'),
    path('cadastro/sensor/', CadastrarSensorView.as_view(), name='cadastro_sensor'),
    path('deletar/sensor/<int:id>/', DeletarSensorView.as_view(), name='deletar_sensor'),
]
