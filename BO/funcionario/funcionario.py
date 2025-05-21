from django.http import HttpResponseServerError

import core.funcionario.models
import jwt
from datetime import datetime as dt
import datetime
import random
import ast
import json
import random
import string

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicione campos personalizados ao token
        token['matricula'] = user.username
        token['cli_info'] = {
             'usuario_id': 123,
             'exp': (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).isoformat(),  # Expira em 30 minutos
             'iat': (datetime.datetime.utcnow()).isoformat(),
             'cli_info': {'cpf': user.cpf,
                          'nome': user.nome,
                          'sobrenome': user.sobrenome,
                          'email': user.email,
                          'perfil': {'perfil_id': user.perfil.pk,
                                     'perfil_nm_descritivo': user.perfil.nm_descritivo,
                                     'lista_filiais': list(core.funcionario.models.FilialFuncionario.objects.values('filial__nome','filial_id').filter(funcionario_id=user.username))}
                          },
         }

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.status:
            raise AuthenticationFailed('Conta inativa ou bloqueada')
        # Você pode adicionar informações adicionais ao response aqui, se necessário
        data['username'] = self.user.username

        return data

class Funcionario():
     def __init__(self, username=None, password=None):
         self.username = username
         self.password = password

     @staticmethod
     def limpar_cpf(cpf):
         if cpf is None:
             return ""
         return cpf.replace(".", "").replace("-", "")

     @staticmethod
     def limpar_data(data):
         if '/' in data:
             partes = data.split('/')

             # Verifica se a data já está no formato 'yyyy/mm/dd'
             if len(partes) == 3 and len(partes[0]) == 4 and len(partes[1]) == 2 and len(partes[2]) == 2:
                 # Retorna a data como está se já estiver no formato correto
                 pass
             # Caso contrário, assume que a data está em 'dd/mm/yyyy' e rearranja para 'yyyy/mm/dd'
             elif len(partes) == 3 and len(partes[0]) == 2 and len(partes[1]) == 2 and len(partes[2]) == 4:
                 data = f'{partes[2]}/{partes[1]}/{partes[0]}'

             # Retorna uma mensagem de erro se o formato não for reconhecido
             else:
                 return "Formato de data inválido"
             if data is None:
                 return ""
             return data.replace("/", "").replace("-", "")
         else:
             return data

     def get_filiais_funcionario(self, matricula=None):
        try:
            filiais = list(core.funcionario.models.FilialFuncionario.objects.values('filial__id', 'filial__nm_descritivo').filter(funcionario_id=matricula))
            return True, '', filiais
        except:
            return False, '', []

     def get_filiais(self):
        try:
            filiais = list(core.funcionario.models.Filial.objects.values('id', 'nm_descritivo').filter(status=True))
            return True, '', filiais
        except:
            return False, '', []

     def get_funcionario(self, matricula=None):
        try:
            funcionario = core.funcionario.models.Funcionario.objects.values().filter(username=matricula).first()
            lista_filias = list(core.funcionario.models.FilialFuncionario.objects.values('filial__nm_descritivo', 'filial_id').filter(funcionario_id=funcionario.get('username')))

            funcionario_atualizado = {
                'password': funcionario.get('password'),
                'last_login': funcionario.get('last_login'),
                'username': funcionario.get('username'),
                'email': funcionario.get('email'),
                'cpf': funcionario.get('cpf'),
                'nome': funcionario.get('nome'),
                'sobrenome': funcionario.get('sobrenome'),
                'data_nascimento': funcionario.get('data_nascimento'),
                'imagem': funcionario.get('imagem'),
                'perfil_id': funcionario.get('perfil_id'),
                'codigo_recuperacao': funcionario.get('codigo_recuperacao'),
                'status': funcionario.get('status'),
                'senha_padrao': funcionario.get('senha_padrao'),
                'filiais': []
            }
            dict_padrao_label = {}
            for filial in lista_filias:
                dict_padrao_label['filial_nm_descritivo'] = filial.get('filial__nm_descritivo')
                dict_padrao_label['id'] = filial.get('filial_id')
                funcionario_atualizado['filiais'].append(dict_padrao_label)
                dict_padrao_label = {}

            return funcionario_atualizado, True, ''
        except:
            return {}, False, ''

     def verificar_senha_padrao(self, senha_padrao=None, matricula=None):
        try:
            funcionario = core.funcionario.models.Funcionario.objects.values().filter(username=matricula,senha_padrao=senha_padrao).first()
            if funcionario:
                return True, True, 'usario liberado para alteração de senha'
            else:
                return False, True, 'usario não liberado para alteração de senha'
        except:
            return False, False, 'erro na verificação de senha do usuário'

     def gerar_senha_padrao(self, username=None):
         try:
             funcionario = core.funcionario.models.Funcionario.objects.filter(username=username).first()
             funcionario.senha_padrao = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=20))
             funcionario.save()
             return True, ''
         except:
             return False, ''

     def get_perfis(self):
        try:
            perfis = list(core.funcionario.models.Perfis.objects.values().filter(status=True))
            return perfis, True, ''
        except:
            return [], False, ''

     def editar_perfil_usuario(self, cpf=None, perfil_id=None):
         try:
             _, _, cliente_existe = self.get_funcionario(cpf=Funcionario.limpar_cpf(cpf))
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
             cliente = core.funcionario.models.Funcionario.objects.filter(cpf=Funcionario.limpar_cpf(cpf)).first()
             if not cliente:
                 return False, 'esse funcionario não existe'
             if perfil_id is None:
                 return False, 'esse perfil não existe'
             cliente.perfil_id = perfil_id
             cliente.save()
             return True

         except Exception as e:  # Captura a exceção e armazena na variável e # Imprime ou faça log da exceção para ver o erro exato
             return False  # Retorna a mensagem de erro

     def gerar_codigo(self, email=None):
        try:
            cliente = core.cliente.models.Cliente.objects.filter(email=email).first()
            cliente.codigo_recuperacao = random.randint(100000, 999999)
            cliente.save()

            self.send_html_email(email=email, codigo=cliente.codigo_recuperacao)

            return True, ''
        except:
            return False, ''

     def logar(self):
         descricao = 'Não foi possivel logar o funcionario, senha ou usuario incorretos'
         token_jwt = {}
         cliente = core.cliente.models.Cliente.objects.filter(matricula=self.username, status=True).first()
         if cliente is not None:
             status = cliente.check_password(raw_password=self.password)
             if status:
                 descricao = ''
                 token_jwt = self.get_token(cliente=cliente)
         else:
             status = False

         return status, descricao, token_jwt

     def get_token(self, cliente=None):
         # Definindo a chave secreta para assinar o token
         # Em produção, use uma chave secreta mais complexa e mantenha-a segura
         SECRET_KEY = 'minha_chave_secreta'

         # Informações do payload do token (os dados que você quer incluir no token, como ID do usuário, permissões, etc.)
         payload = {
             'usuario_id': 123,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # Expira em 30 minutos
             'iat': datetime.datetime.utcnow(),
             'cli_info': {'cpf':cliente.cpf,
                          'nome':cliente.nome,
                          'sobrenome':cliente.sobrenome,
                          'email':cliente.email,
                          'perfil':{'perfil_id':cliente.perfil.pk,
                                    'perfil_nm_descritivo':cliente.perfil.nm_descritivo,
                                    'perfil_nivel':cliente.perfil.nivel}
                          },
         }

         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

         # Para decodificar o token
         decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

         print(decoded_payload)

         return token

     def cadastrar_funcionario(self,nome=None,sobrenome=None,perfil=None,email=None,cpf=None,data_nasc=None,lista_filiais=[]):
         try:
             funcionario = core.funcionario.models.Funcionario()
             funcionario.email = email
             funcionario.cpf = cpf
             funcionario.nome = nome
             funcionario.sobrenome = sobrenome
             funcionario.data_nascimento = data_nasc.replace('/','')
             funcionario.perfil_id = perfil
             funcionario.username = int(core.funcionario.models.Funcionario.objects.values('username').order_by('-username').first().get('username')) + 1
             funcionario.save()

             for filial in lista_filiais:
                 funcionario_filial = core.funcionario.models.FilialFuncionario()
                 funcionario_filial.id =int( core.funcionario.models.FilialFuncionario.objects.values('id').order_by('-id').first().get(
                     'id')) + 1
                 funcionario_filial.funcionario_id = funcionario.username
                 funcionario_filial.filial_id = filial
                 funcionario_filial.save()

             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def editar_funcionario(self,username=None, nome=None, sobrenome=None, perfil=None, email=None, cpf=None, data_nasc=None,lista_filiais=[]):
         try:


             if 'T' in data_nasc:
                 dt = datetime.datetime.strptime(data_nasc, '%Y-%m-%dT%H:%M:%S.%fZ')
             else:
                 dt = datetime.datetime.strptime(data_nasc, '%d/%m/%Y')
             data_limpa = dt.strftime('%d%m%Y')

             funcionario = core.funcionario.models.Funcionario.objects.filter(username=username).first()
             funcionario.email = email
             funcionario.cpf = cpf
             funcionario.nome = nome
             funcionario.sobrenome = sobrenome
             funcionario.data_nascimento = data_limpa
             funcionario.perfil_id = perfil
             funcionario.save()


             core.funcionario.models.FilialFuncionario.objects.filter(funcionario_id=funcionario.username).delete()

             for filial in lista_filiais:
                 funcionario_filial = core.funcionario.models.FilialFuncionario()
                 funcionario_filial.funcionario_id = funcionario.username
                 ultimo_id = core.funcionario.models.FilialFuncionario.objects.values('id').order_by('-id').first()
                 if ultimo_id:
                    funcionario_filial.id = int(ultimo_id.get('id')) + 1
                 else:
                    funcionario_filial.id = 0
                 funcionario_filial.filial_id = filial
                 funcionario_filial.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def alterar_senha(self, matricula=None, senha=None):
         try:
             funcionario_existe = self.get_funcionario(matricula=matricula)
             if not funcionario_existe:
                 return False, 'erro ao alterar senha contate o suporte ERRO M001'
             funcionario = core.funcionario.models.Funcionario.objects.filter(username=matricula).first()
             funcionario.set_password(raw_password=senha)
             funcionario.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def resetar_senha(self, codigo=None, email=None):
         try:
             funcionario = core.funcionario.models.Funcionario.objects.filter(email=email).first()
             funcionario.set_password(raw_password=self.password)
             funcionario.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def verificar_codigo(self, email=None, codigo=None):
         try:
             funcionario = core.funcionario.models.Funcionario.objects.filter(email=email).first()
             if funcionario.codigo_recuperacao == int(codigo):
                funcionario.set_password(raw_password=self.password)
             funcionario.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def deletar_funcionario(self, username=None):
        try:
            funcionario = core.funcionario.models.Funcionario.objects.filter(username=username).first()
            if funcionario.status  == True:
                funcionario.status = False
            else:
                funcionario.status = True
            funcionario.save()
            return True, ''
        except:
            return False, 'não foi possivel deletar o funcionario'


     def validar_email(self, email=None):
        try:
            email = core.funcionario.models.Funcionario.objects.filter(email=email).first()
            if email:
                return True
        except:
            return False

     def enviar_email(self, email=None, codigo=None):
         return



     # settings.py

     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
     EMAIL_HOST = 'smtp.gmail.com'
     EMAIL_PORT = 587
     EMAIL_USE_TLS = True
     EMAIL_HOST_USER = 'goodgainoficcial@gmail.com'
     EMAIL_HOST_PASSWORD = 'Nika@1234'

     def send_my_email(self):
         send_mail(
             'Assunto do Email',
             'Mensagem do Email. Aqui vai o corpo do email.',
             'seu_email@gmail.com',  # Email de origem
             ['t.caron@terra.com.br'],  # Lista de emails que receberão a mensagem
             fail_silently=False,
         )

     def send_html_email(self, email=None, codigo=None):
         context = {'token': codigo}
         html_content = render_to_string('email_rest_senha.html', context)

         email = EmailMessage(
             'Código de reset de senha Rein!',
             html_content,
             'rein@gmail.com',
             [email]
         )
         email.content_subtype = 'html'
         email.send()

     #abaixo informações de admin
     def get_todos_usuarios(self, cpf_cliente=None):
         try:
             if cpf_cliente or self.username:
                 todos_usuarios = list(core.funcionario.models.Funcionario.objects.filter(cpf=cpf_cliente).values())
             else:
                 todos_usuarios = list(core.funcionario.models.Funcionario.objects.values().all())

             for usuario in todos_usuarios:
                 data = str(usuario.get('data_nascimento'))
                 if data:
                     # Se vier como objeto datetime
                     data_formatada = f"{data[:2]}/{data[2:4]}/{data[4:]}"
                     usuario['data_nascimento'] = data_formatada
                 if usuario['last_login']:
                     usuario['last_login'] = usuario['last_login'].strftime('%d/%m/%Y')
                 if usuario['status'] == True:
                     usuario['status'] = 'Ativo'
                 else:
                     usuario['status'] = 'Inativado'

             return True, '', todos_usuarios

         except Exception as e:
             return False, 'Ocorreu um erro ao tentar coletar os usuários', []
