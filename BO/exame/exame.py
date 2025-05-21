from datetime import datetime
import core.exames.models
import core.funcionario.models
class Exame():
     def __init__(self, id=None):
         self.id = id

     def get_total_atendimentos(self):
        try:
            exames =list(core.exames.models.Exame.objects().values())
            return exames, True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar os exames atuais'


     def get_percentual_exames(self):
        try:
            exames =list(core.exames.models.Exame.objects().values())
            return exames, True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar os exames atuais'

     def get_quantidade_por_especie(self):
        try:
            exames =list(core.exames.models.Exame.objects().values())
            return exames, True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar os exames atuais'


     def get_quantidade_por_especie_percentual(self):
        try:
            exames =list(core.exames.models.Exame.objects().values())
            return exames, True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar os exames atuais'

     def get_especie(self):
        try:
            especie = list(core.exames.models.Tipo.objects.values().filter(tipo='CODIGO.ESPECIE', status=True))
            return especie , True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar as especies'


     def get_laudos(self):
        try:
            laudo = list(core.exames.models.Tipo.objects.values().filter(tipo='CODIGO.LAUDO', status=True))
            return laudo , True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar as especies'

     def get_exame_execucao(self, exame_id=None):
         try:
             exame = core.exames.models.ExameExecucao.objects.values().filter(id=exame_id).first()
             return exame, True, ''
         except:
             return {}, False, 'ocorreu um erro ao coletar as especies'



     def transformar_data(self, data_str):
         try:
             # Caso o formato seja 'dd/mm/yyyy'
             if '/' in data_str:
                 data_obj = datetime.strptime(data_str, '%d/%m/%Y')
             else:
                 # Remove o GMT e o texto entre parênteses
                 data_limpa = data_str.split('GMT')[0].strip()
                 data_obj = datetime.strptime(data_limpa, '%a %b %d %Y %H:%M:%S')

             # Retorna no formato anomesdia
             return data_obj.strftime('%Y%m%d')
         except Exception as e:
             return data_str

     def get_dashboard(self, filial=None, dat_inicial=None, dat_final=None, funcionario_id=None):
        if dat_inicial:
            dat_inicial_atualizada = self.transformar_data(dat_inicial)
        if dat_final:
            dat_final_atualizada = self.transformar_data(dat_final)
        try:

            tipos_especie = list(core.exames.models.Tipo.objects.values().filter(tipo='CODIGO.ESPECIE'))

            tipos_exames = list(core.exames.models.Exame.objects.values())

            lista_filiais_funcionario = list(core.funcionario.models.FilialFuncionario.objects.values_list('filial__id', flat=True).filter(funcionario=funcionario_id))

            dict_exame_incial = {}
            lista_incial_exame = []

            for exame in tipos_exames:
                dict_exame_incial['id'] = exame['id']
                dict_exame_incial['nome'] = exame['nome']
                dict_exame_incial['quantidade_exame'] = 0
                dict_exame_incial['valor_exame'] = 00.00
                dict_exame_incial['status'] = 'Ativo' if exame['status'] else 'Inativo'
                lista_incial_exame.append(dict_exame_incial)
                dict_exame_incial = {}

            dict_especie_incial = {}
            lista_incial_especie = []
            for especie in tipos_especie:
                dict_especie_incial['especie'] = especie['informacao']
                dict_especie_incial['id'] = especie['id']
                dict_especie_incial['quantidade_especie'] = 0
                dict_especie_incial['status'] = 'Ativo' if especie['status'] else 'Inativo'
                lista_incial_especie.append(dict_especie_incial)
                dict_especie_incial = {}

            dados_dashboard = {
                'tabela_exames': lista_incial_exame,
                'total_exames': 0,
                'valor_medio_exames': 0,
                'grafico_percentual_exames': [],
                'tabela_especie': lista_incial_especie,
                'total_geral_especie': 0,
                'grafico_percentual_quantidade_especie': [],
                'tabela_atendimento': []

            }

            if filial == 'null':
                exames = list(core.exames.models.ExameExecucao.objects.values('id','data_execucao','work','doper','paciente','tutor','status','valor','exame_id','exame__nome','laudo_id','laudo__informacao','especie_id','especie__informacao',
                ).filter(status=True, data_execucao__gte=dat_inicial_atualizada, data_execucao__lte=dat_final_atualizada, filial_id__in=lista_filiais_funcionario))
            else:
                exames = list(
                    core.exames.models.ExameExecucao.objects.values('id', 'data_execucao', 'work', 'doper', 'paciente',
                                                                    'tutor', 'status', 'valor', 'exame_id',
                                                                    'exame__nome', 'laudo_id', 'laudo__informacao',
                                                                    'especie_id', 'especie__informacao',
                                                                    ).filter(status=True, filial_id=filial, data_execucao__gte=dat_inicial_atualizada, data_execucao__lte=dat_final_atualizada))
            # Formatar a data_execucao para dd/mm/yyyy
            for exame in exames:
                data = str(exame.get('data_execucao'))
                if data:
                    exame['data_execucao'] = f"{data[6:]}/{data[4:6]}/{data[:4]}"

            if len(exames) <= 0:
                return dados_dashboard, True, ''
            total_exames = len(exames)
            total_valor_exames = 00.0
            quantidade_especie = {}

            for especie in tipos_especie:
                quantidade_especie[especie['id']] = {'informacao': especie['informacao'], 'status': 'Ativo' if especie['status'] else 'Inativo', 'codigo': especie['codigo'], 'quantidade':0}

            tabela_atendimento = {}
            for exame in exames:


                if exame['exame_id'] in list(tabela_atendimento):
                    tabela_atendimento[exame['exame_id']]['quantidade_exame'] += 1
                    tabela_atendimento[exame['exame_id']]['valor_exame'] += exame['valor']
                else:
                    tabela_atendimento[exame['exame_id']] = {'exame__nome': exame['exame__nome'],'quantidade_exame': 1, 'status':exame['status'], 'valor_exame': exame['valor']}


                total_valor_exames += exame['valor']
                if exame['especie_id'] in list(quantidade_especie):
                    quantidade_especie[exame['especie_id']]['quantidade'] += 1
                else:
                    quantidade_especie[exame['especie_id']]['quantidade'] += 1


            grafico_percentual_exames = {}
            for dado_exame in tabela_atendimento:
                tabela_atendimento[dado_exame]
                if dado_exame not in list(grafico_percentual_exames):
                    grafico_percentual_exames[dado_exame] = tabela_atendimento[dado_exame]['valor_exame']/total_valor_exames * 100

            grafico_percentual_especie = {}
            for dado_especie in quantidade_especie:
                quantidade_especie[dado_especie]['quantidade']
                if dado_especie not in list(grafico_percentual_especie):
                    grafico_percentual_especie[dado_especie] = quantidade_especie[dado_especie]['quantidade']/ total_exames * 100

            lista_quantidade_especie = []
            for i in quantidade_especie:
                dict_exemplo = {'id':i ,'especie': quantidade_especie[i]['informacao'], 'quantidade_especie':quantidade_especie[i]['quantidade'], 'status':quantidade_especie[i]['status']}
                lista_quantidade_especie.append(dict_exemplo)

            lista_grafico_especie = []
            for i in grafico_percentual_especie:
                dict_exemplo = {'nome': quantidade_especie[i]['informacao'], 'porcentagem': grafico_percentual_especie[i]}
                lista_grafico_especie.append(dict_exemplo)

            lista_quantidade_exames = []
            # for i in tabela_atendimento:
            #     dict_exemplo = {'id':i ,'nome': tabela_atendimento[i]['exame__nome'],'status':'Ativo' if tabela_atendimento[i]['status'] else 'Inativo', 'quantidade_exame': tabela_atendimento[i]['quantidade_exame'], 'valor_exame':tabela_atendimento[i]['valor_exame']}
            #     lista_quantidade_exames.append(dict_exemplo)

            for exame_faltante in lista_incial_exame:
                if exame_faltante['id'] in tabela_atendimento:
                    dict_exemplo = {'id': exame_faltante['id'], 'nome': tabela_atendimento[exame_faltante['id']]['exame__nome'],
                                    'status': exame_faltante['status'],
                                    'quantidade_exame': tabela_atendimento[exame_faltante['id']]['quantidade_exame'],
                                    'valor_exame': tabela_atendimento[exame_faltante['id']]['valor_exame']}
                    lista_quantidade_exames.append(dict_exemplo)
                if exame_faltante['id'] not in tabela_atendimento:
                    dict_exemplo = {'id': exame_faltante['id'],
                                    'nome': exame_faltante['nome'],
                                    'status': exame_faltante['status'],
                                    'quantidade_exame': exame_faltante['quantidade_exame'],
                                    'valor_exame': exame_faltante['valor_exame']}
                    lista_quantidade_exames.append(dict_exemplo)



            lista_grafico_exames= []
            for i in grafico_percentual_exames:
                dict_exemplo = {'nome': tabela_atendimento[i]['exame__nome'], 'porcentagem': grafico_percentual_exames[i]}
                lista_grafico_exames.append(dict_exemplo)


            dados_dashboard = {
                'tabela_exames': lista_quantidade_exames,
                'total_exames': total_exames,
                'valor_exames': total_valor_exames,
                'grafico_percentual_exames': lista_grafico_exames,
                'tabela_especie': lista_quantidade_especie,
                'total_geral_especie': total_exames,
                'grafico_percentual_quantidade_especie': lista_grafico_especie,
                'tabela_atendimento': exames

            }

            return dados_dashboard, True, ''
        except:
            return dados_dashboard , False, 'ocorreu um erro ao coletar os exames atuais'
     def get_tipo_exames(self):
         try:
             tipos_exames = list(core.exames.models.Exame.objects.values())
             return tipos_exames, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar as especies'

     def get_preco_exames(self):
         try:
             tipos_exames = list(core.exames.models.Exame.objects.values('id', 'nome', 'valor_padrao'))
             objeto_valores = {}
             for tipo in tipos_exames:
                 objeto_valores[tipo['id']] = tipo['valor_padrao']
             return objeto_valores, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar as especies'




     def get_tipo_exame(self, id=None):
         try:
             exame= core.exames.models.Exame.objects.values().filter(id=id).first()
             return exame, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar as especies'

     def get_tipo_especie(self, id=None):
         try:
             especie = core.exames.models.Tipo.objects.values().filter(id=id ,tipo='CODIGO.ESPECIE').first()
             return especie, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar as especies'
     def get_exame(self, filial=None):
        try:

            tipos_especie = list(core.exames.models.Tipo.objects.values().filter(tipo='CODIGO.ESPECIE', status=True))

            dados_dashboard = {
                'tabela_exames': [],
                'total_exames': 0,
                'valor_medio_exames': 0,
                'grafico_percentual_exames': [],
                'tabela_especie': [],
                'total_geral_especie': 0,
                'grafico_percentual_quantidade_especie': [],
                'tabela_atendimento': []

            }

            if not filial:
                exames = list(core.exames.models.ExameExecucao.objects.values('data_execucao','work','doper','paciente','tutor','status','valor','exame_id','exame__nome','laudo_id','laudo__informacao','especie_id','especie__informacao',
                ).filter(status=True))
            else:
                exames = list(
                    core.exames.models.ExameExecucao.objects.values('data_execucao', 'work', 'doper', 'paciente',
                                                                    'tutor', 'status', 'valor', 'exame_id',
                                                                    'exame__nome', 'laudo_id', 'laudo__informacao',
                                                                    'especie_id', 'especie__informacao',
                                                                    ).filter(status=True, filial_id=filial))

            total_exames = len(exames)
            total_valor_exames = 00.0
            quantidade_especie = {}

            for especie in tipos_especie:
                if especie not in list(quantidade_especie):
                    quantidade_especie[especie['informacao']] = 0

            tabela_atendimento = {}
            for exame in exames:


                if exame['exame__nome'] in list(tabela_atendimento):
                    tabela_atendimento[exame['exame__nome']]['quantidade_exame'] += 1
                    # quantidade_exame_atual += 1
                    tabela_atendimento[exame['exame__nome']]['valor_exame'] += exame['valor']
                    # valor_exame_atual += exame['valor']
                    # tabela_atendimento[exame.exame_nome] = {'quantidade_exame': quantidade_exame_atual, 'valor_exame': valor_exame_atual}
                    # quantidade_exame_atual = 0
                    # valor_exame_atual = 00.0
                else:
                    tabela_atendimento[exame['exame__nome']] = {'quantidade_exame': 1, 'valor_exame': exame['valor']}


                total_valor_exames += exame['valor']
                if exame['especie__informacao'] in list(quantidade_especie):
                    quantidade_especie[exame['especie__informacao']] += 1
                else:
                    quantidade_especie[exame['especie__informacao']] += 1


            grafico_percentual_exames = {}
            for dado_exame in tabela_atendimento:
                tabela_atendimento[dado_exame]
                if dado_exame not in list(grafico_percentual_exames):
                    grafico_percentual_exames[dado_exame] = tabela_atendimento[dado_exame]['valor_exame']/total_valor_exames * 100

            grafico_percentual_especie = {}
            for dado_especie in quantidade_especie:
                quantidade_especie[dado_especie]
                if dado_especie not in list(grafico_percentual_especie):
                    grafico_percentual_especie[dado_especie] = quantidade_especie[dado_especie]/ total_exames * 100

            lista_quantidade_especie = []
            for i in quantidade_especie:
                dict_exemplo = {'especie': i, 'quantidade_especie':quantidade_especie[i]}
                lista_quantidade_especie.append(dict_exemplo)

            lista_grafico_especie = []
            for i in grafico_percentual_especie:
                dict_exemplo = {'nome': i, 'porcentagem': grafico_percentual_especie[i]}
                lista_grafico_especie.append(dict_exemplo)

            lista_quantidade_exames = []
            for i in tabela_atendimento:
                dict_exemplo = {'nome': i, 'quantidade_exame': tabela_atendimento[i]['quantidade_exame'], 'valor_exame':tabela_atendimento[i]['valor_exame']}
                lista_quantidade_exames.append(dict_exemplo)

            lista_grafico_exames= []
            for i in grafico_percentual_exames:
                dict_exemplo = {'nome': i, 'porcentagem': grafico_percentual_exames[i]}
                lista_grafico_exames.append(dict_exemplo)


            dados_dashboard = {
                'tabela_exames': lista_quantidade_exames,
                'total_exames': total_exames,
                'valor_exames': total_valor_exames,
                'grafico_percentual_exames': lista_grafico_exames,
                'tabela_especie': lista_quantidade_especie,
                'total_geral_especie': total_exames,
                'grafico_percentual_quantidade_especie': lista_grafico_especie,
                'tabela_atendimento': exames

            }

            return dados_dashboard, True, ''
        except:
            return dados_dashboard , False, 'ocorreu um erro ao coletar os exames atuais'

     def cadastrar_exame(self, nome= None, nm_descritivo=None, valor_padrao=None):
         try:
             exame = core.exames.models.Exame()
             exame.nome = nome
             exame.nm_descritivo =nome
             exame.valor_padrao = valor_padrao
             exame.status = True
             exame.id = core.exames.models.Exame.objects.values('id').order_by('-id').first()['id'] + 1
             exame.save()
             return True, 'sucesso ao cadastrar o exame'
         except:
             return False, 'ocorreu um erro ao criar o exame caso o erro persista por favor informe o suporte'

     def editar_exame(self,id=None, nome= None, nm_descritivo=None, valor_padrao=None):
         try:
             exame = core.exames.models.Exame.objects.filter(id=id).first()
             exame.nm_descritivo = nome
             exame.nome = nome
             exame.valor_padrao = valor_padrao
             exame.status = True
             exame.save()
             return True, 'sucesso ao editar o exame'
         except:
             return False, 'ocorreu um erro ao editar o exame caso o erro persista por favor informe o suporte'

     def excluir_exame(self, id=None):
         try:
             exame = core.exames.models.Exame.objects.filter(id=id).first()
             if exame.status == False:
                 exame.status = True
             else:
                exame.status = False
             exame.save()
             return True, 'sucesso ao deletar o exame'
         except:
             return False, 'ocorreu um erro ao deletar o exame caso o erro persista por favor informe o suporte'

     def cadastrar_especie(self, nome=None):
         try:
             especie = core.exames.models.Tipo()
             especie.informacao = nome
             especie.tipo = 'CODIGO.ESPECIE'
             especie.status = True
             especie.save()
             return True, 'sucesso ao cadastrar o exame'
         except:
             return False, 'ocorreu um erro ao criar o exame caso o erro persista por favor informe o suporte'

     def editar_especie(self, id=None, nome=None):
         try:
             especie = core.exames.models.Tipo.objects.filter(id=id ,tipo='CODIGO.ESPECIE').first()
             especie.informacao = nome
             especie.save()
             return True, 'sucesso ao editar o exame'
         except:
             return False, 'ocorreu um erro ao editar o exame caso o erro persista por favor informe o suporte'

     def excluir_especie(self, id=None):
         try:
             especie = core.exames.models.Tipo.objects.filter(id=id).first()
             if especie.status ==True:
                especie.status = False
             else:
                 especie.status = True
             especie.save()
             return True, 'sucesso ao deletar o exame'
         except:
             return False, 'ocorreu um erro ao deletar o exame caso o erro persista por favor informe o suporte'



     def get_info_exames_execucao(self):
        try:
            exames = list(core.exames.models.ExameExecucao.objects().values())
            return exames, True, ''
        except:
            return [], False, 'ocorreu um erro ao coletar os exames atuais'

     def cadastrar_exames_execucao(self,data_execucao=None,work=None,doper=None,paciente=None,tutor=None,valor=None, exame_tipo=None,laudo=None,especie=None,filial=None):
         try:
             data_execucao_atualizada = self.transformar_data(data_execucao)
             exame = core.exames.models.ExameExecucao()
             exame.data_execucao = data_execucao_atualizada
             exame.work =work
             exame.doper =doper
             exame.paciente =paciente
             exame.tutor =tutor
             exame.status =True
             exame.valor =valor
             exame.exame_id =exame_tipo
             exame.laudo_id =laudo
             exame.especie_id =especie
             exame.filial_id =filial
             exame.save()
             return exame, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar os exames atuais'

     def editar_exames_execucao(self, id=None, data_execucao=None, work=None, doper=None, paciente=None, tutor=None, valor=None, exame_id=None, laudo=None, especie=None, filial=None):
         try:
             data_execucao_atualizada = self.transformar_data(data_execucao)
             exame = core.exames.models.ExameExecucao.objects.filter(id=id).first()
             exame.data_execucao = data_execucao_atualizada
             exame.work = work
             exame.doper = doper
             exame.paciente = paciente
             exame.tutor = tutor
             exame.status = True
             exame.valor = valor
             exame.exame_id = exame_id
             exame.laudo_id = laudo
             exame.especie_id = especie
             exame.filial_id = filial
             exame.save()
             return exame, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar os exames atuais'

     def excluir_exames_execucao(self, id=None):
         try:
             exame = core.exames.models.ExameExecucao.objects.filter(id=id).first()
             exame.status = False
             exame.save()
             return exame, True, ''
         except:
             return [], False, 'ocorreu um erro ao coletar os exames atuais'