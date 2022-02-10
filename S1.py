import dsd as dsd
from datetime import date


dominio="http://portal.stf.jus.br/"
path="pauta/services/calendario-service.asp?dados=calendarios&"
dados_pauta = []


anoinicial = 2016
anofinal = 2021
lista_datas = []
lista_sessoes_virtuais = []

for ano_delta in range(anofinal-anoinicial+1):
    ano = anofinal-ano_delta
    for mes in ('01','02','03','04','05','06','07','08','09','10','11','12'):
        html = 'NA'
        mes_int = int(mes)
        
        querry = 'mes='+ mes + '&ano=' + str(ano)
        url = dominio+path+querry
        html = dsd.solicitar_dados(dominio,path,querry)
        
        presencial_dias = dsd.extrair(html,'"diasPresenciais":[',']')
        presencial_dias = presencial_dias.split(',')
        if presencial_dias[0] != '':
            for dia in presencial_dias:
                data_sessao_presencial = date(ano, mes_int, int(dia)).strftime("%d/%m/%Y")

                lista_datas.append([data_sessao_presencial])
        
        sessao = ''
        virtual_sessoes = dsd.extrair(html,',"julgamentosVirtuais":[',']')
        virtual_sessoes = virtual_sessoes.split('},{')
        if virtual_sessoes[0] != '':
            for sessao in virtual_sessoes:
                sessao = sessao.strip('{')
                sessao = sessao.strip('}')
                datainicial = dsd.extrair(sessao,'"dataInicial":"','"')
                datafinal = dsd.extrair(sessao,'"dataFinal":"','"')
                plenario = dsd.extrair(sessao,'"qtdProcessosPlenario":"','"')
                T1 = dsd.extrair(sessao,'"qtdPrimeiraTurma":"','"')
                T2 = dsd.extrair(sessao,'"qtdSegundaTurma":"','"')
                dados_sessao = [datainicial,datafinal,plenario,T1,T2]

                lista_sessoes_virtuais.append(dados_sessao)

        print (html)

#     # função de gravação
dsd.limpar_arquivo ('SessoesPresenciais2016-2021.txt')
dsd.write_csv_header ('SessoesPresenciais2016-2021.txt', 'data')
dsd.write_csv_lines ('SessoesPresenciais2016-2021.txt', lista_datas)

dsd.limpar_arquivo ('SessoesVirtuais2016-2021.txt')
dsd.write_csv_header ('SessoesVirtuais2016-2021.txt', 'datainicial,datafinal,plenario,T1,T2')
dsd.write_csv_lines ('SessoesVirtuais2016-2021.txt', lista_sessoes_virtuais)
