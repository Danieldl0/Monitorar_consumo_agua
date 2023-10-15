from django.urls import path

from .views import *

urlpatterns = [
    path('cadastro/', CadastroConsumoView.as_view(), name="cadastro_consumo_api"),
]