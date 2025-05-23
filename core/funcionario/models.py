import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class FuncionarioManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class Funcionario(AbstractBaseUser):
    username = models.CharField(unique=True,primary_key=True)
    email = models.CharField(max_length=100, null=True)
    cpf = models.BigIntegerField()
    nome = models.CharField(max_length=100, null=True)
    sobrenome = models.CharField(max_length=100, null=True)
    data_nascimento = models.CharField(max_length=100,null=True)
    imagem = models.CharField(max_length=200, null=True)
    perfil = models.ForeignKey('funcionario.Perfis', on_delete=models.DO_NOTHING, null=True)
    codigo_recuperacao = models.BigIntegerField(null=True)
    status = models.BooleanField(default=True, null=True)
    senha_padrao = models.CharField(max_length=40, null=True)

    objects = FuncionarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # 'email' ou outros campos necessários

    # def save(self, *args, **kwargs):
    #     self.username = self.matricula  # Garante que username sempre seja igual a matricula
    #     super(Funcionario, self).save(*args, **kwargs)

    class Meta:
        db_table = '"public"."funcionario"'

class Perfis(models.Model):
    """
    :Nome da classe/função: Perfis
    :descrição: Classe de Perfis
    :Criação: Thiago Jungles Caron - 06/04/2024
    :Edições:
    """
    nome = models.CharField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=50, null=True)
    status = models.BooleanField(null=True, default=True)
    valor = models.FloatField(null=True)
    nivel = models.IntegerField(null=True)


    class Meta:
        db_table = u'"public\".\"perfis"'

class Filial(models.Model):
    """
        :Nome da classe/função: Filial
        :descrição: Classe de filiais do sistema
        :Criação: Thiago Jungles Caron - 19/03/2025
        :Edições:
        """
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    nm_descritivo = models.CharField(max_length=50, null=True)
    status = models.BooleanField(null=True, default=True)

    class Meta:
        db_table = u'"public\".\"filial"'

class FilialFuncionario(models.Model):
    """
        :Nome da classe/função: FilialFuncionario
        :descrição: Classe de filiais que um determinado funcionario tem acesso
        :Criação: Thiago Jungles Caron - 19/03/2025
        :Edições:
        """
    id = models.IntegerField(primary_key=True)
    filial =  models.ForeignKey('funcionario.Filial', on_delete=models.DO_NOTHING, null=True)
    funcionario = models.ForeignKey('funcionario.Funcionario', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = u'"public\".\"filial_funcionario"'