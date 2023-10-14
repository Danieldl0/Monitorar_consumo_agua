from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from django.views.generic import TemplateView

from .forms.consumo import ConsumoAguaForm
from .forms.sensor import SensorForm
from .models.consumo_agua import ConsumoAgua
from .models.sensor import Sensor


@method_decorator(login_required, name="dispatch")
class ConsumoView(TemplateView):
    template_name = 'visualizar_consumo.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.mes_atual = tz.now().replace(day=1)
        proximo_mes = tz.now().replace(day=28) + timedelta(days=4)
        self.ultimo_dia_mes_atual = (proximo_mes - timedelta(days=proximo_mes.day))

        self.consumos_periodo = ConsumoAgua.objects.filter(
            data_consumo__range=(self.mes_atual, self.ultimo_dia_mes_atual.strftime("%Y-%m-%d")),
            sensor__usuario=request.user
        )

        self.consumos = []

    def get(self, request, *args , **kwargs):
        data_inicio = self.mes_atual
        data_final = self.ultimo_dia_mes_atual
        periodo = [self.mes_atual.strftime("%d/%m/%Y"), self.ultimo_dia_mes_atual.strftime("%d/%m/%Y")]

        if 'data1' in request.GET and 'data2' in request.GET:
            data_inicio = datetime.strptime(request.GET.get('data1'), "%Y-%m-%d")
            data_final = datetime.strptime(request.GET.get('data2'), "%Y-%m-%d")
            if data_inicio and data_final:
                periodo = [data_inicio.strftime("%d/%m/%Y"), data_final.strftime("%d/%m/%Y")]

        while data_inicio <= data_final:
            consumo = self.consumos_periodo.filter(
                data_consumo=data_inicio
            ).aggregate(Sum('consumo', default=0))
            if consumo:
                consumo.update(dict(
                    data_consumo=data_inicio
                ))
                self.consumos.append(consumo)
            data_inicio += timedelta(days=1)

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



class DeletarSensorView(TemplateView):
    template_name='deleta_sensor.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.sensor = get_object_or_404(Sensor, pk=kwargs.get('id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            sensor=self.sensor
        )

        return context

    def post(self, request, *args, **kwargs):
        self.sensor.delete()
        return redirect('cadastro_sensor')