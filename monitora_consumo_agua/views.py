from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms.consumo import ConsumoAguaForm
from .forms.sensor import SensorForm
from .models.consumo_agua import ConsumoAgua
from .models.sensor import Sensor


class ConsumoView(TemplateView):
    template_name = 'visualizar_consumo.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.consumos = ConsumoAgua.objects.all()

    def get(self, request, *args , **kwargs):
        periodo = ['10/10/2023', '20/10/2023']

        return render(request, self.template_name, dict(
            periodo=periodo,
            consumos=self.consumos
        ))


class CadastrarConsumoView(TemplateView):
    template_name = 'cadastro_consumo.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = ConsumoAguaForm(request.POST or None)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(dict(
            form=self.form
        ))

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name, dict(
            form=self.form
        ))

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()

            return render(request, 'visualizar_consumo.html', dict(
                teste='com sucesso'
            ))
        return render(request, self.template_name , dict(
                form=self.form
            ))

@method_decorator(login_required, name="dispatch")
class CadastrarSensorView(TemplateView):
    template_name = 'cadastro_sensor.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form = SensorForm(request.POST or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(dict(
            form=self.form
        ))

    def get(self, request, *args, **kwargs):
        sensores = Sensor.objects.filter(
            usuario=request.user
        )
        
        return render(request, self.template_name, dict(
            form=self.form,
            sensores=sensores
        ))

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            instance = self.form.save()
            instance.usuario = request.user
            instance.save()
            return render(request, self.template_name , dict(
                form=SensorForm(),
                sensores=Sensor.objects.filter(
                    usuario=request.user
                )
            ))

        return render(request, self.template_name , dict(
                form=self.form,
                sensores=Sensor.objects.filter(
                            usuario=request.user
                        )
            ))