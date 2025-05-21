from django.http import JsonResponse

import BO.funcionario.funcionario
import BO.exame.exame

from rest_framework.views import APIView
from BO.autenticacao.autenticacao import validar_perfil
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
import datetime

from rest_framework_simplejwt.views import TokenObtainPairView
from BO.funcionario.funcionario import MyTokenObtainPairSerializer  # Certifique-se de importar corretamente seu serializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ResetSenhaView(APIView):
    def post(self,*args, **kwargs):
        email = self.request.data.get('email')
        status, mensagem, cliente = BO.funcionario.funcionario.Cliente().resetar_senha(email=email)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class ValidarPerfil(APIView):

    def get(self, *args, **kwargs):

        status, descricao = validar_perfil(user=self.request.user,nivel_necessario=2)
        return JsonResponse({'status': status, 'descricao': descricao})

class Funcionario(APIView):

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        status, mensagem, cliente = BO.funcionario.funcionario.Cliente().get_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem, 'funcionario': cliente})

    def post(self, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        nome = self.request.data.get('nome')
        sobrenome = self.request.data.get('sobrenome')
        email = self.request.data.get('email')
        cpf = self.request.data.get('cpf')
        data_nasc = self.request.data.get('dataNascimento')

        status, mensagem = BO.funcionario.funcionario.Cliente(username=username, password=password).cadastrar_cliente(nome=nome,
                                                                                                              sobrenome=sobrenome,
                                                                                                              email=email,
                                                                                                              cpf=cpf,
                                                                                                              data_nasc=data_nasc)

        return JsonResponse({'status': status, 'descricao':mensagem})

    def put(self, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        nome = self.request.data.get('nome')
        sobrenome = self.request.data.get('sobrenome')
        email = self.request.data.get('email')
        cpf = self.request.data.get('cpf')
        data_nasc = self.request.data.get('data_nascimento')

        status, mensagem = BO.funcionario.funcionario.Cliente(username=username, password=password).editar_cliente(nome=nome,
                                                                                                           sobrenome=sobrenome,
                                                                                                           email=email,
                                                                                                           cpf=cpf,
                                                                                                           data_nasc=data_nasc)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def delete(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        status, mensagem = BO.funcionario.funcionario.Cliente().deletar_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class PegarPerfis(APIView):

    def get(self, *args, **kwargs):
        dados, status, mensagem = BO.funcionario.funcionario.Funcionario().get_perfis()
        return JsonResponse({'status': status, 'mensagem': mensagem, 'dados': dados})

class AlterarSenha(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def put(self, *args, **kwargs):
        senha = self.request.data.get('senha')
        matricula = self.request.data.get('matricula')
        status, mensagem = BO.funcionario.funcionario.Funcionario().alterar_senha(matricula=matricula, senha=senha)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class DashFuncionario(APIView):

    def get(self, *args, **kwargs):
        id = self.request.GET.get('id')
        status, mensagem, cliente = BO.funcionario.funcionario.Funcionario().get_todos_usuarios()
        return JsonResponse({'status': status, 'mensagem': mensagem, 'funcionario': cliente})

    def post(self,request, *args, **kwargs):
        lista_filiais = self.request.data.get('filiais')
        nome = self.request.data.get('nome')
        sobrenome = self.request.data.get('sobrenome')
        email = self.request.data.get('email')
        cpf = self.request.data.get('cpf')
        perfil_id = self.request.data.get('perfil_id')
        data_nasc = self.request.data.get('data_nascimento')

        status, mensagem = BO.funcionario.funcionario.Funcionario().cadastrar_funcionario(nome=nome,
                                                                                          sobrenome=sobrenome,
                                                                                          perfil=perfil_id,
                                                                                          email=email,
                                                                                          cpf=cpf,
                                                                                          data_nasc=data_nasc,
                                                                                          lista_filiais=lista_filiais)

        return JsonResponse({'status': status, 'descricao':mensagem})

    def put(self, *args, **kwargs):
        username = self.request.data.get('id')
        nome = self.request.data.get('nome')
        sobrenome = self.request.data.get('sobrenome')
        email = self.request.data.get('email')
        cpf = self.request.data.get('cpf')
        perfil_id = self.request.data.get('perfil_id')
        data_nasc = self.request.data.get('data_nascimento')
        lista_filiais = self.request.data.get('filiais')

        status, mensagem = BO.funcionario.funcionario.Funcionario().editar_funcionario(username=username,
                                                                                       nome=nome,
                                                                                       sobrenome=sobrenome,
                                                                                       perfil=perfil_id,
                                                                                       email=email,
                                                                                       cpf=cpf,
                                                                                       data_nasc=data_nasc,
                                                                                       lista_filiais=lista_filiais)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def delete(self, *args, **kwargs):
        username = self.request.query_params.get('id')
        status, mensagem = BO.funcionario.funcionario.Funcionario().deletar_funcionario(username=username)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class Login(APIView):
    def get(self, *args, **kwargs):
        return

    def post(self, *args, **kwargs):
        user = self.request.data.get('username')
        password = self.request.data.get('password')

        status, descricao, token_jwt = BO.funcionario.funcionario.Cliente(username=user, password=password).logar()

        return JsonResponse({'status': status,'descricao': descricao,'token': token_jwt})


class EditarUsuarioAdmin(APIView):
    def put(self, *args, **kwargs):
        if self.request.user.perfil.nivel == 0:
            username = self.request.data.get('username')
            password = self.request.data.get('password')
            nome = self.request.data.get('nome')
            sobrenome = self.request.data.get('sobrenome')
            email = self.request.data.get('email')
            cpf = self.request.data.get('cpf')
            data_nasc = self.request.data.get('data_nasc')
            perfil = self.request.data.get('perfil_id')

            status, mensagem = BO.funcionario.funcionario.Cliente(username=username, password=password).editar_cliente(nome=nome,
                                                                                                               sobrenome=sobrenome,
                                                                                                               email=email,
                                                                                                               cpf=cpf,
                                                                                                               data_nasc=data_nasc,
                                                                                                               perfil=perfil)
        else:
            status, mensagem = False, 'essa conta não tem nivel de acesso o suficiente para editar'
        return JsonResponse({'status': status, 'mensagem': mensagem})

class PegarExame(APIView):
    def get(self, *args, **kwargs):
        id = self.request.GET.get('id')
        dados, status, mensagem = BO.exame.exame.Exame().get_tipo_exame(id=id)
        return JsonResponse({'dados': dados, 'status': status, 'mensagem': mensagem})

class PegarEspecie(APIView):
    def get(self, *args, **kwargs):
        id = self.request.GET.get('id')
        dados, status, mensagem = BO.exame.exame.Exame().get_tipo_especie(id=id)
        return JsonResponse({'dados': dados, 'status': status, 'mensagem': mensagem})

class PegarUsuario(APIView):
    def get(self, *args, **kwargs):
        matricula = self.request.GET.get('id')
        dados, status, mensagem = BO.funcionario.funcionario.Funcionario().get_funcionario(matricula=matricula)
        return JsonResponse({'dados': dados, 'status': status, 'mensagem': mensagem})

class SenhaPadrao(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        senha_padrao = self.request.GET.get('senha_padrao')
        matricula = self.request.GET.get('matricula')
        verificacao ,status, mensagem = BO.funcionario.funcionario.Funcionario().verificar_senha_padrao(senha_padrao=senha_padrao, matricula=matricula)
        return JsonResponse({'verificacao':verificacao,'status': status, 'mensagem': mensagem})
    def post(self, *args, **kwargs):
        matricula = self.request.data.get('id')
        status, mensagem = BO.funcionario.funcionario.Funcionario().gerar_senha_padrao(username=matricula)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class PrecoExame(APIView):
    def get(self, *args, **kwargs):
        dados, status, mensagem = BO.exame.exame.Exame().get_preco_exames()
        return JsonResponse({'dados':dados, 'status': status, 'mensagem': mensagem})

class Exame(APIView):
    def get(self, *args, **kwargs):
        dados, status, mensagem = BO.exame.exame.Exame().get_tipo_exames()
        return JsonResponse({'dados':dados, 'status': status, 'mensagem': mensagem})
    def post(self, *args, **kwargs):
        nome = self.request.data.get('exame')
        valor_padrao = self.request.data.get('valor')

        status, mensagem = BO.exame.exame.Exame().cadastrar_exame(nome=nome,
                                                                  valor_padrao=valor_padrao)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def put(self, *args, **kwargs):
        id = self.request.data.get('id')
        nome = self.request.data.get('exame')
        valor_padrao = self.request.data.get('valor')
        status, mensagem = BO.exame.exame.Exame().editar_exame(id=id,
                                                               nome=nome,
                                                               valor_padrao=valor_padrao)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def delete(self, *args, **kwargs):

        id = self.request.GET.get('id')
        status, mensagem = BO.exame.exame.Exame().excluir_exame(id=id)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class Laudo(APIView):
    def get(self, *args, **kwargs):
        dados, status, mensagem = BO.exame.exame.Exame().get_laudos()
        return JsonResponse({'dados':dados, 'status': status, 'mensagem': mensagem})


class Especie(APIView):
    def get(self, *args, **kwargs):
        dados, status, mensagem = BO.exame.exame.Exame().get_especie()
        return JsonResponse({'dados':dados, 'status': status, 'mensagem': mensagem})
    def post(self, *args, **kwargs):
        nome = self.request.data.get('nome')

        status, mensagem = BO.exame.exame.Exame().cadastrar_especie(nome=nome)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def put(self, *args, **kwargs):
        nome = self.request.data.get('nome')
        id = self.request.data.get('id')
        status, mensagem = BO.exame.exame.Exame().editar_especie(id=id, nome=nome)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def delete(self, *args, **kwargs):
        id = self.request.GET.get('id')
        status, mensagem = BO.exame.exame.Exame().excluir_especie(id=id)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class Filiais(APIView):
    def get(self, *args, **kwargs):
        matricula = self.request.user.username
        status, mensagem, dados = BO.funcionario.funcionario.Funcionario().get_filiais()
        return JsonResponse({'dados': dados, 'status': status, 'mensagem': mensagem})


class FiliaisFuncionario(APIView):
    def get(self, *args, **kwargs):
        matricula = self.request.user.username
        status, mensagem, dados = BO.funcionario.funcionario.Funcionario().get_filiais_funcionario(matricula=matricula)
        return JsonResponse({'dados': dados, 'status': status, 'mensagem': mensagem})


class AtendimentoExecucao(APIView):
    def get(self, *args, **kwargs):
        id = self.request.GET.get('id')
        dados, status, mensagem = BO.exame.exame.Exame().get_exame_execucao(exame_id=id)
        return JsonResponse({'dados': dados, 'status': status, 'mensagem': mensagem})

    def post(self, *args, **kwargs):

        data_execucao = self.request.data.get('dataExecucao')
        work = self.request.data.get('work')
        doper = self.request.data.get('doper')
        paciente = self.request.data.get('paciente')
        tutor = self.request.data.get('tutor')
        status = self.request.data.get('status')
        valor = self.request.data.get('valor')
        exame = self.request.data.get('exame')
        laudo = self.request.data.get('laudo')
        especie = self.request.data.get('especie')
        filial = self.request.data.get('filial')

        objeto, status, mensagem = BO.exame.exame.Exame().cadastrar_exames_execucao(data_execucao=data_execucao,
                                                                            work=work,
                                                                            doper=doper,
                                                                            paciente=paciente,
                                                                            tutor=tutor,
                                                                            valor=valor,
                                                                            exame_tipo=exame,
                                                                            laudo=laudo,
                                                                            especie=especie,
                                                                            filial=filial)
        return JsonResponse({'status': status, 'mensagem': mensagem})

    def put(self, *args, **kwargs):
        id = self.request.data.get('id')
        data_execucao = self.request.data.get('dataExecucao')
        work = self.request.data.get('work')
        doper = self.request.data.get('doper')
        paciente = self.request.data.get('paciente')
        tutor = self.request.data.get('tutor')
        status = self.request.data.get('status')
        valor = self.request.data.get('valor')
        exame = self.request.data.get('exame')
        laudo = self.request.data.get('laudo')
        especie = self.request.data.get('especie')
        filial = self.request.data.get('filial')
        dados, status, mensagem = BO.exame.exame.Exame().editar_exames_execucao(data_execucao=data_execucao,
                                                                            work=work,
                                                                            doper=doper,
                                                                            paciente=paciente,
                                                                            tutor=tutor,
                                                                            valor=valor,
                                                                            exame_id=exame,
                                                                            laudo=laudo,
                                                                            especie=especie,
                                                                            filial=filial,
                                                                            id=id)
        return JsonResponse({'status': status, 'mensagem': mensagem})

    def delete(self, *args, **kwargs):
        id = self.request.GET.get('id')
        dados, status, mensagem = BO.exame.exame.Exame().excluir_exames_execucao(id=id)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class Dashboard(APIView):
    def get(self, *args, **kwargs):
        filial = self.request.GET.get('filial')
        dat_inicial = self.request.GET.get('dataInicial')
        dat_final = self.request.GET.get('dataFinal')
        dados, status, mensagem = BO.exame.exame.Exame().get_dashboard(filial=filial,
                                                                       dat_inicial=dat_inicial,
                                                                       dat_final=dat_final,
                                                                       funcionario_id=self.request.user.pk)

        return JsonResponse({'dados':dados, 'status': status, 'mensagem': mensagem})
    def post(self, *args, **kwargs):
        nome = self.request.data.get('nome')
        nm_descritivo = self.request.data.get('nm_descritivo')
        valor_padrao = self.request.data.get('valor_padrao')

        status, mensagem = BO.exame.exame.Exame().cadastrar_exame(nome=nome,
                                                                  nm_descritivo=nm_descritivo,
                                                                  valor_padrao=valor_padrao)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def put(self, *args, **kwargs):
        nome = self.request.data.get('nome')
        nm_descritivo = self.request.data.get('nm_descritivo')
        valor_padrao = self.request.data.get('valor_padrao')
        id = self.request.data.get('id')
        status, mensagem = BO.exame.exame.Exame().editar_exame(id=id,nome=nome,
                                                               nm_descritivo=nm_descritivo,
                                                               valor_padrao=valor_padrao)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def delete(self, *args, **kwargs):

        nome = self.request.data.get('nome')
        id = self.request.GET.get('id')
        status, mensagem = BO.exame.exame.Exame().excluir_exame(id=id,nome=nome)
        return JsonResponse({'status': status, 'mensagem': mensagem})
