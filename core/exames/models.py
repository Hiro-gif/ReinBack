import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


import datetime
import core.funcionario

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

class Exame(models.Model):
    """
    :Nome da classe/função: Exame
    :descrição: Classe de exames possiveis
    :Criação: Thiago Jungles Caron - 19/03/2025
    :Edições:
    """
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    nm_descritivo = models.CharField(max_length=50, null=True)
    status = models.BooleanField(null=True, default=True)
    valor_padrao = models.FloatField(null=True)


    class Meta:
        db_table = u'"public\".\"exame"'


class ExameExecucao(models.Model):
    """
    :Nome da classe/função: ExameExecucao
    :descrição: Classe de exames executados ou em execucao
    :Criação: Thiago Jungles Caron - 19/03/2025
    :Edições:
    """
    data_execucao = models.IntegerField(null=True)
    work = models.CharField(max_length=100, null=True)
    doper = models.BigIntegerField(null=True)
    paciente = models.CharField(max_length=100, null=True)
    tutor = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True, default=True)
    valor = models.FloatField(null=True)
    exame = models.ForeignKey('exames.Exame', on_delete=models.DO_NOTHING, null=True)
    laudo = models.ForeignKey('exames.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='laudo')
    especie = models.ForeignKey('exames.Tipo', on_delete=models.DO_NOTHING, null=True,related_name='especie')
    filial = models.ForeignKey('funcionario.Filial', on_delete=models.DO_NOTHING, null=True, related_name='especie')


    class Meta:
        db_table = u'"public\".\"exame_execucao"'

class Tipo(models.Model):
    """
    :Nome da classe/função: Tipo
    :descrição: Classe de tipo de dados ou estados de diferentes informações da plataforma
    :Criação: Thiago Jungles Caron - 19/03/2025
    :Edições:
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100, null=True)
    codigo_externo = models.CharField(max_length=100, null=True)
    informacao = models.CharField(max_length=100, null=True)
    tipo = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True, default=True)


    class Meta:
        db_table = u'"public\".\"tipo"'
