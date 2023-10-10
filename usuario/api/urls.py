from django.urls import path

from usuario.api.views import *

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name="cadastro_api_user"),
    path('login/', LoginView.as_view(), name="login_api_user"),
]