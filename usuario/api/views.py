from rest_framework.generics import CreateAPIView
from usuario.api.serializer import *
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken


class CadastroView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(dict(
                refresh=str(refresh),
                token=str(refresh.access_token),
            ))
        return Response(serializer.errors)