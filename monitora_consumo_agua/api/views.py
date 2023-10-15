from rest_framework.generics import CreateAPIView
from .serializers import CadastroConsumoSerializer
from rest_framework.response import Response


class CadastroConsumoView(CreateAPIView):
    serializer_class = CadastroConsumoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)