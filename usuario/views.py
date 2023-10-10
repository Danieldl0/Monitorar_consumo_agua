from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from usuario.forms import CadastroUserForm, LoginFormView


class CadastroView(TemplateView):
    template_name = 'cadastro.html'

    def setup(self, request, *args, **kwargs):

        self.form = CadastroUserForm(
            request.POST or None
        )

        return super().setup(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update(dict(
            form=self.form,
        ))

        return context

    def post(self, request):
        if self.form.is_valid():
            self.form.save()
            return redirect('login_user')
        return render(template_name=self.template_name, context=self.get_context_data(), request=request)


class LoginView(TemplateView):
    template_name = 'login.html'

    def setup(self, request, *args, **kwargs):
        self.form = LoginFormView(
            request.POST or None,
        )
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            form=self.form,
        ))
        return context

    def post(self, request):
        if self.form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('consumo_view')

        return render(template_name=self.template_name, context=self.get_context_data(), request=request)


def logout(request):
    # encerrando a seção do usuario logado
    auth.logout(request)
    return redirect(reverse('login_user'))