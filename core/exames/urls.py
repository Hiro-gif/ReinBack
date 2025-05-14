from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

import ReinProject.views
import core.funcionario.views

urlpatterns = [
        re_path('funcionario', ReinProject.views.Cliente.as_view(), name='funcionario'),
        re_path('alterar/senha', ReinProject.views.AlterarsenhaView.as_view(), name='alterar_senha'),
        re_path('reset/senha', ReinProject.views.ResetSenhaView.as_view(), name='reset_senha'),
        re_path('verificar/codigo', ReinProject.views.VerficarCodigo.as_view(), name='reset_senha'),
]
