from django.urls import path

from usuario.views import *

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name="cadastro_user"),
    path('login/', LoginView.as_view(), name='login_user'),
]