import dsd
import pandas as pd

def processar_lista (listas_string):
    listas = listas_string.split('"idTipo":"')[1:]
    for lista in listas:
        tipo = lista[0]
        tipo_desc = dsd.extrair(lista,'"descricao":"','"')
        tipo_desc = tipo_desc.replace('Listas dos Relatores (Incidentes e Recursos - Todas as Classes)','Incidentes&Recursos')
        tipo_desc = tipo_desc.replace('Listas dos Relatores (Mérito, exceto Controle Concentrado)','Geral')
        tipo_desc = tipo_desc.replace('Listas de Devoluções de Vistas','VistasDevolução')
        tipo_desc = tipo_desc.replace('Listas dos Relatores em Ações de Controle Concentrado (Mérito)','ControleConcentradoMérito')
        lista = dsd.extrair(lista, '"ministros":[{','')
        lista = lista.replace('MINISTRA','MINISTRO')
        lista = lista.replace('MINISTRO','MIN.')
        listasplit = lista.split('"nome":"MIN. ')[1:]
        print (listasplit)
        for elemento in listasplit:
            elementosplit = elemento.split('","listaJulgamento":[{')
            relator = dsd.remover_acentos(elementosplit[0].upper())
            dados_lista = elementosplit[1].split('"id":"')[1:]
            for objeto in dados_lista:
                objeto = objeto.split('}')[0].strip('"')
                lista_id = dsd.extrair(objeto, '', '","')
                lista_desc = dsd.extrair(objeto, '"descricao":"', '","')
                lista_ordem = dsd.extrair(objeto, '"ordem":"', '","')
                lista_quantidade = dsd.extrair(objeto, '"quantidadeProcessos":"', '"')
                lista_dados = [orgao,data_inicial,data_final,tipo,tipo_desc,relator,lista_id,lista_desc,lista_ordem,lista_quantidade]
                id_list.append([lista_id,orgao])
                dados_a_gravar.append(lista_dados)
    
    
dados = dsd.csv_to_list ('SessoesVirtuais2016-2021.txt')
dados_a_gravar = []
id_list = []
espera = 0

for sessao in dados[2:]:
    
    espera = espera +1
    dsd.esperar(1,20,espera)

    data_inicial = sessao[0]
    data_final = sessao[1]
    print (data_inicial)
    
    dominio = "http://portal.stf.jus.br/"
    path = "pauta/services/calendario-service.asp?dados=sessao-virtual&inicio="
    querry = data_inicial + '&fim=' + data_final
    
    url = dominio+path+querry
    html = dsd.solicitar_dados(dominio,path,querry)

    
    listasT1 = dsd.extrair(html,'"codigo":"1T"','},{"codigo":')
    orgao = 'T1'
    processar_lista(listasT1)
    
    listasT2 = dsd.extrair(html,'"codigo":"2T"','},{"codigo":')
    orgao = 'T2'
    processar_lista(listasT2)
    
    listasPleno = dsd.extrair(html,'"codigo":"TP"','')
    orgao = 'TP'
    processar_lista(listasPleno)

dsd.limpar_arquivo ('ListasVirtuais2016-2021.txt')
dsd.write_csv_header ('listasvirtuais2016-2021.txt', 'orgao,data_inicial,data_final,tipo,tipo_desc,relator,lista_id,lista_desc,lista_ordem,lista_quantidade')
dsd.write_csv_lines ('ListasVirtuais2016-2021.txt', dados_a_gravar)

dsd.limpar_arquivo ('IDListas2016-2021.txt')
dsd.write_csv_header ('IDListas2016-2021.txt', 'ID,orgao')
dsd.write_csv_lines ('IDListas2016-2021.txt', id_list)