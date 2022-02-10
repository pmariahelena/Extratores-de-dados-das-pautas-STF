import dsd
  
    
dados = dsd.csv_to_list ('ListasVirtuais2016-2021.txt')
dados_a_gravar = []
dados_TP = []

espera = 0

dsd.limpar_arquivo ('IDProcessoPautadoVirtual2016-2021.txt')
dsd.write_csv_header ('IDProcessoPautadoVirtual2016-2021.txt', 'incidente,orgao,id_lista,data_inicio,classe,numero,descricao,origem,partes')

for item in dados[1:]:
    
    if item[0] == "TP":
        dados_TP.append(item)
                
        
for lista_virtual in dados_TP[0:]:
    
        print(f'{espera+1} de {len(dados_TP)}')
        espera = espera +1
        dsd.esperar(5,40,espera)
        dsd.esperar(10,200,espera)
        dsd.esperar(30,700,espera)

    
    
        dominio = "http://portal.stf.jus.br/"
        path = "pauta/services/lista-service.asp?lista="
        id_lista = str(lista_virtual[6])
        data_inicio = lista_virtual[1]
        orgao = lista_virtual[0]
        
        url = dominio+path+id_lista
        html = dsd.solicitar_dados(dominio,path,id_lista)
        # print (html)
    
        
        processos = html.split('"id":"')[1:]
        
        for processo in processos:
            
            incidente = 'NA'
            classe = 'NA'
            numero = 'NA'
            descricao = 'NA'
            origem = 'NA'
            partes = 'NA'
                      
            incidente = dsd.extrair(processo, '','","classe":')
            classe = dsd.extrair(processo, '"classe":"','","numero":')
            numero = dsd.extrair(processo, '","numero":"','","cadeia"')
            descricao = dsd.extrair(processo, '"cadeia":"','","procedencia')
            origem = dsd.extrair(processo, 'procedencia":"','","partes":')
            partes = dsd.extrair(processo, '","partes":','')
            
            dados_a_gravar.append([incidente,orgao,id_lista,data_inicio,classe,numero,descricao,origem,partes])

            dsd.write_csv_line ('IDProcessoPautadoVirtualTP2016-2021.txt', [incidente,orgao,id_lista,data_inicio,classe,numero,descricao,origem,partes])
