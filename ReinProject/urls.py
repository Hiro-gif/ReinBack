"""
URL configuration for ReinProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, re_path
import ReinProject.views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^login$', ReinProject.views.MyTokenObtainPairView.as_view()),
    re_path('dashboard', ReinProject.views.Dashboard.as_view(), name='dashboard'),

    re_path('filiais', ReinProject.views.Filiais.as_view(), name='filiais'),
    re_path('func_filial', ReinProject.views.FiliaisFuncionario.as_view(), name='func_filial'),
    re_path('exames', ReinProject.views.Exame.as_view(), name='exames'),
    re_path('valor_exam', ReinProject.views.PrecoExame.as_view(), name='valor_exam'),
    re_path('especie', ReinProject.views.Especie.as_view(), name='especie'),
    re_path('pegar_exame', ReinProject.views.PegarExame.as_view(), name='pegar_exames'),
    re_path('get_specie', ReinProject.views.PegarEspecie.as_view(), name='get_specie'),
    re_path('get_usuario', ReinProject.views.PegarUsuario.as_view(), name='get_usuario'),
    re_path('senha_padrao', ReinProject.views.SenhaPadrao.as_view(), name='senha_padrao'),
    re_path('laudo', ReinProject.views.Laudo.as_view(), name='laudo'),

    re_path('usuarios', ReinProject.views.DashFuncionario.as_view(), name='usuarios'),
    re_path('alterar_senha', ReinProject.views.AlterarSenha.as_view(), name='alterar_senha'),
    re_path('get_perfis', ReinProject.views.PegarPerfis.as_view(), name='get_perfis'),

    re_path('atendimentos_execucao', ReinProject.views.AtendimentoExecucao.as_view(), name='atendimentos_execucao'),
]
