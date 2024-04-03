from pyModbusTCP.client import ModbusClient
from datetime import datetime
import numpy as np
import pandas as pd
import time
import math



def teste():
    
    smartlogger_porta = 502
    ret_inv = []
    total = 14

    for i in range (10, 17): 
        
        smartlogger_endereco = f"192.168.163.{i}"
        
        #DEFINIR SE VAI RODAR 3 INVERSORES OU 2 INVERSORES

        if(i >=14):
           total = 13
 
        else:         
            total = 14
 
        #FOR PARA RODAR NOS INVERSORES
 
        for ID in range (10, total):
            time.sleep(1)

            #APENAS NA USINA 01 O ID DO SMARTLOGGER É 10
            if (ID == 10):
                    if(smartlogger_endereco == "192.168.163.10"):
                        ID = 10
                    else:    
                        ID = 101

            smartlogger = ModbusClient(host=smartlogger_endereco, port=smartlogger_porta, unit_id=ID, auto_open="True", auto_close="True") 
            #print("SMARTLOGGER", smartlogger)
            
            #DEFINIR SE É LEITURA DO SMARTLOGGER OU DO INVERSOR
            if (ID == 10 or ID == 101):
                #print("DADOS SMARTLOGGER")
      
                leiturasmartlogger = smartlogger.read_holding_registers(40550, 28)
                
                energydaily =       np.multiply(leiturasmartlogger[13], 0.1)
                corrente_smart_A =  np.multiply(leiturasmartlogger[22], 1)
                corrente_smart_B =  np.multiply(leiturasmartlogger[23], 1)
                corrente_smart_C =  np.multiply(leiturasmartlogger[24], 1)
                tensao_smart_A =    np.multiply(leiturasmartlogger[25], 0.1)
                tensao_smart_B =    np.multiply(leiturasmartlogger[26], 0.1)
                tensao_smart_C =    np.multiply(leiturasmartlogger[27], 0.1)

                ret_smartogger = np.round([energydaily, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)


            else:              
                #print("DADOS INVERSORES")

                leitura_inv = smartlogger.read_holding_registers(32015, 80)
                         
                correntePV_inv =  np.multiply(leitura_inv[2:38:2], 0.01)
                tensaoAC_inv =    np.multiply(leitura_inv[51:54:1], 0.1)
                corrente_inv =    np.multiply(leitura_inv[58:64:2], 0.001)
                tempinterna_inv = np.multiply(leitura_inv[72], 0.1)
                potativaAC_inv =  np.multiply(leitura_inv[66], 0.001)
                InputPower_inv=   np.multiply(leitura_inv[50], 0.001)

                aux_array = [tempinterna_inv, potativaAC_inv, InputPower_inv]
                aux_ret_inv = np.round(np.concatenate((np.array(aux_array), np.array(tensaoAC_inv), np.array(corrente_inv), np.array(correntePV_inv))),3)

                ret_inv = np.concatenate((np.array(ret_inv), np.array(aux_ret_inv)))
                
        
        agora = datetime.now()
        data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
        ret_usina = np.concatenate((np.array(data_hora), np.array(ret_smartogger),(np.array(ret_inv))))
        usina = i-9
        #print("USINA = ", usina)
        #print("DADOS: ", ret_usina)

        #LIMPAR OS DADOS DA VARIÁVEL EM CADA USINA
        if ((ID == 13 and usina <= 4) or (ID==12 and usina > 4)):
            salvar_smartloggers_teste(usina, ret_usina)
            #print("SALVEI")
            ret_inv = []
            ret_smartogger = []

        
    return 

def salvar_smartloggers_teste(usina, dados_usina):
    print("USINA: ", usina)
    #print(ret_usina)
   
    tag_usina_aux = []
    tag_corrente_inv_aux = []
    tag_inv = []

    tag_smartlogger = ["DATA HORA", f"SMARTLOGGER{usina}.MED.kWh_Dia", f"SMARTLOGGER{usina}.MED.IA", f"SMARTLOGGER{usina}.MED.IB", f"SMARTLOGGER{usina}.MED.IC", f"SMARTLOGGER{usina}.MED.VAB", f"SMARTLOGGER{usina}.MED.VBC", f"SMARTLOGGER{usina}.MED.VCA"]
 
    if usina < 5:
        for i in range (1,4):
            inv = f"{usina}_{i}"
            tag_inv_aux = [f"INV{inv}.MED.TEMP_INT", f"INV{inv}.MED.kW", f"INV{inv}.MED.INPUT_POWER", f"INV{inv}.MED.VAB", f"INV{inv}.MED.VBC", f"INV{inv}.MED.VCA", f"INV{inv}.MED.IA", f"INV{inv}.MED.IB", f"INV{inv}.MED.IC"]
            
            for string in range(1,19):
                tag_correnteinv = [f"INV{inv}.MED.AMP_S{string}"]
                tag_corrente_inv_aux += tag_correnteinv
            
            
            tag_usina_aux += tag_inv_aux + tag_corrente_inv_aux
            tag_corrente_inv_aux = []
        
    else:
        for i in range (1,3):
            inv = f"{usina}_{i}"
            tag_inv_aux = [f"INV{inv}.MED.TEMP_INT", f"INV{inv}.MED.kW", f"INV{inv}.MED.INPUT_POWER", f"INV{inv}.MED.VAB", f"INV{inv}.MED.VBC", f"INV{inv}.MED.VCA", f"INV{inv}.MED.IA", f"INV{inv}.MED.IB", f"INV{inv}.MED.IC"]
 
            for string in range(1,19):
                tag_correnteinv = [f"INV{inv}.MED.AMP_S{string}"]
                tag_corrente_inv_aux += tag_correnteinv
            
            
            tag_usina_aux += tag_inv_aux + tag_corrente_inv_aux
            tag_corrente_inv_aux = []
    
    tag_usina = tag_smartlogger + tag_usina_aux
    
    dados_dict = {titulo: dado for titulo, dado in zip(tag_usina, dados_usina)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA01" já existe
        if f"USINA0{usina}" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA01"
            df_concatenado = pd.concat([df_existente[f"USINA0{usina}"], df], ignore_index=True)
        else:
            # Se a aba "USINA01" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA01"
            df_concatenado.to_excel(writer, index=False, sheet_name=f"USINA0{usina}")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name=f"USINA0{usina}")


def estacao_solarimetrica():
    #Estação Solarimétrica
    #IP: 192.168.163.8
    #PORTA: 502
    #UNIT ID: 2

    server_em = '192.168.163.8'
    porta_em = 502
    ID_em = 2
    cont_em = 0
    c_em = ModbusClient(host=server_em,port=porta_em,unit_id=ID_em, auto_open = True, auto_close = True)

    #MAPA MODBUS
    #3 -
    #4 - PIRANÔMETRO IPOA (W/m²)
    #5 - ALBEDÔMETRO (W/m²)
    #6 - TEMP MÓDULO (ºC)
    #7 - TEMP AMBIENTE (ºC)

    ler_em = c_em.read_holding_registers(3, 5)
    valor_em = np.multiply (ler_em, 0.1)
    valor_em = np.round(valor_em,2)
       
    dados =valor_em[0], valor_em[1], valor_em[2], valor_em[3], valor_em[4]
    # print("ESTAÇÃO SOLARIMÉTRICA \n")
    # print(f'PIRANÔMETRO GHI = {valor_em[0]:.2f} (W/m²)')
    # print(f'PIRANÔMETRO IPOA = {valor_em[1]:.2f} (W/m²)')
    # print(f'ALBEDÔMETRO= {valor_em[2]:.2f} (W/m²)')
    # print(f'TEMP. MÓDULO = {valor_em[3]:.2f} (ºC)')
    # print(f'TEMP. AMBIENTE = {valor_em[4]:.2f} (ºC)')

    return dados

def smartlogger_01():
    smartlogger01_endereco = '192.168.163.10'
    smartlogger01_porta= 502
    smartlogger01_ID = 10
    smartlogger01_ID1 = 11
    smartlogger01_ID2 = 12
    smartlogger01_ID3 = 13
    data_hora = []

    smartlogger01 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID) 
    smartlogger11 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID1) 
    smartlogger12 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID2)
    smartlogger13 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID3) 

    smartlogger01.open()
    smartlogger11.open()
    smartlogger12.open()
    smartlogger13.open()

    leiturasmartlogger01 = smartlogger01.read_holding_registers(40550, 28)
    leitura_inv11 = smartlogger11.read_holding_registers(32015, 80)
    leitura_inv12 = smartlogger12.read_holding_registers(32015, 80)
    leitura_inv13 = smartlogger13.read_holding_registers(32015, 80)

    smartlogger01.close()
    smartlogger11.close()
    smartlogger12.close()
    smartlogger13.close()

    energydaily01 = np.multiply(leiturasmartlogger01[13], 0.1)
    #corrente01 = np.multiply(leiturasmartlogger01[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger01[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger01[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger01[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger01[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger01[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger01[27], 0.1)

    correntePV_inv11 = np.multiply(leitura_inv11[2:38:2], 0.01)
    correntePV_inv12 = np.multiply(leitura_inv12[2:38:2], 0.01)
    correntePV_inv13 = np.multiply(leitura_inv13[2:38:2], 0.01)
    
    # tensaoPV_inv11 = np.multiply(leitura_inv11[1:37:2], 0.1)
    # tensaoPV_inv12 = np.multiply(leitura_inv12[1:37:2], 0.1)
    # tensaoPV_inv13 = np.multiply(leitura_inv13[1:37:2], 0.1)

    tensaoAC_inv11 = np.multiply(leitura_inv11[51:54:1], 0.1)
    tensaoAC_inv12 = np.multiply(leitura_inv12[51:54:1], 0.1)
    tensaoAC_inv13 = np.multiply(leitura_inv13[51:54:1], 0.1)

    corrente_inv11 = np.multiply(leitura_inv11[58:64:2], 0.001)
    corrente_inv12 = np.multiply(leitura_inv12[58:64:2], 0.001)
    corrente_inv13 = np.multiply(leitura_inv13[58:64:2], 0.001)

    tempinterna_inv11 = np.multiply(leitura_inv11[72], 0.1)
    tempinterna_inv12 = np.multiply(leitura_inv12[72], 0.1)
    tempinterna_inv13 = np.multiply(leitura_inv13[72], 0.1)

    potativaAC_inv11 = np.multiply(leitura_inv11[66], 0.001)
    potativaAC_inv12 = np.multiply(leitura_inv12[66], 0.001)
    potativaAC_inv13 = np.multiply(leitura_inv13[66], 0.001)

    InputPower_inv11= np.multiply(leitura_inv11[50], 0.001)
    InputPower_inv12 = np.multiply(leitura_inv12[50], 0.001)
    InputPower_inv13 = np.multiply(leitura_inv13[50], 0.001)

    aux_array11 = [tempinterna_inv11, potativaAC_inv11, InputPower_inv11]
    aux_array12 = [tempinterna_inv12, potativaAC_inv12, InputPower_inv12]
    aux_array13 = [tempinterna_inv13, potativaAC_inv13, InputPower_inv13]

    ret_inv11 = np.round(np.concatenate((np.array(aux_array11), np.array(tensaoAC_inv11), np.array(corrente_inv11), np.array(correntePV_inv11))),3)
    ret_inv12 = np.round(np.concatenate((np.array(aux_array12), np.array(tensaoAC_inv12), np.array(corrente_inv12), np.array(correntePV_inv12))),3)
    ret_inv13 = np.round(np.concatenate((np.array(aux_array13), np.array(tensaoAC_inv13), np.array(corrente_inv13), np.array(correntePV_inv13))),3) 

    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger01 = np.round([energydaily01, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina01 = np.concatenate((np.array(data_hora), np.array(ret_smartogger01),np.array(ret_inv11), np.array(ret_inv12), np.array(ret_inv13)))
    print("VALOR SMARTLOGGER: ", ret_usina01)
    return ret_usina01
      
def smartlogger_02():
    smartlogger02_endereco = '192.168.163.11'
    smartlogger02_porta= 502
    smartlogger02_ID = 101
    smartlogger02_ID1 = 11
    smartlogger02_ID2 = 12
    smartlogger02_ID3 = 13
    
    smartlogger02 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID)
    smartlogger21 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID1)
    smartlogger22 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID2)
    smartlogger23 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID3)
    print("Estou aqui3")
    smartlogger02.open()
    smartlogger21.open()
    smartlogger22.open()
    smartlogger23.open()

    leiturasmartlogger02 = smartlogger02.read_holding_registers(40550, 28)
    leitura_inv21 = smartlogger21.read_holding_registers(32015, 80)
    leitura_inv22 = smartlogger22.read_holding_registers(32015, 80)
    leitura_inv23 = smartlogger23.read_holding_registers(32015, 80)

    smartlogger02.close()
    smartlogger21.close()
    smartlogger22.close()
    smartlogger23.close()
    print("Estou aqui4")

    energydaily02 = np.multiply(leiturasmartlogger02[13], 0.1)
    #corrente02 = np.multiply(leiturasmartlogger02[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger02[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger02[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger02[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger02[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger02[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger02[27], 0.1)

    correntePV_inv21 = np.multiply(leitura_inv21[2:38:2], 0.01)
    correntePV_inv22 = np.multiply(leitura_inv22[2:38:2], 0.01)
    correntePV_inv23 = np.multiply(leitura_inv23[2:38:2], 0.01)
    
    # tensaoPV_inv21 = np.multiply(leitura_inv21[1:37:2], 0.1)
    # tensaoPV_inv22 = np.multiply(leitura_inv22[1:37:2], 0.1)
    # tensaoPV_inv23 = np.multiply(leitura_inv23[1:37:2], 0.1)

    tensaoAC_inv21 = np.multiply(leitura_inv21[51:54:1], 0.1)
    tensaoAC_inv22 = np.multiply(leitura_inv22[51:54:1], 0.1)
    tensaoAC_inv23 = np.multiply(leitura_inv23[51:54:1], 0.1)

    corrente_inv21 = np.multiply(leitura_inv21[58:64:2], 0.001)
    corrente_inv22 = np.multiply(leitura_inv22[58:64:2], 0.001)
    corrente_inv23 = np.multiply(leitura_inv23[58:64:2], 0.001)

    tempinterna_inv21 = np.multiply(leitura_inv21[72], 0.1)
    tempinterna_inv22 = np.multiply(leitura_inv22[72], 0.1)
    tempinterna_inv23 = np.multiply(leitura_inv23[72], 0.1)

    potativaAC_inv21 = np.multiply(leitura_inv21[66], 0.001)
    potativaAC_inv22 = np.multiply(leitura_inv22[66], 0.001)
    potativaAC_inv23 = np.multiply(leitura_inv23[66], 0.001)

    InputPower_inv21= np.multiply(leitura_inv21[50], 0.001)
    InputPower_inv22 = np.multiply(leitura_inv22[50], 0.001)
    InputPower_inv23 = np.multiply(leitura_inv23[50], 0.001)


    aux_array21 = [tempinterna_inv21, potativaAC_inv21, InputPower_inv21]
    aux_array22 = [tempinterna_inv22, potativaAC_inv22, InputPower_inv22]
    aux_array23 = [tempinterna_inv23, potativaAC_inv23, InputPower_inv23]

    ret_inv21 = np.round(np.concatenate((np.array(aux_array21), np.array(tensaoAC_inv21), np.array(corrente_inv21), np.array(correntePV_inv21))),3)
    ret_inv22 = np.round(np.concatenate((np.array(aux_array22), np.array(tensaoAC_inv22), np.array(corrente_inv22), np.array(correntePV_inv22))),3)
    ret_inv23 = np.round(np.concatenate((np.array(aux_array23), np.array(tensaoAC_inv23), np.array(corrente_inv23), np.array(correntePV_inv23))),3)
    
    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger02 = np.round([energydaily02, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina02 = np.concatenate((np.array(data_hora), np.array(ret_smartogger02),np.array(ret_inv21), np.array(ret_inv22), np.array(ret_inv23)))

    return ret_usina02

def smartlogger_03():
    smartlogger03_endereco = '192.168.163.12'
    smartlogger03_porta= 502
    smartlogger03_ID = 101
    smartlogger03_ID1 = 11
    smartlogger03_ID2 = 12
    smartlogger03_ID3 = 13
    
    smartlogger03 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID)
    smartlogger31 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID1)
    smartlogger32 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID2)
    smartlogger33 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID3)
    print("Estou aqui5")
    smartlogger03.open()
    smartlogger31.open()
    smartlogger32.open()
    smartlogger33.open()

    leiturasmartlogger03 = smartlogger03.read_holding_registers(40550, 28)
    leitura_inv31 = smartlogger31.read_holding_registers(32015, 80)
    leitura_inv32 = smartlogger32.read_holding_registers(32015, 80)
    leitura_inv33 = smartlogger33.read_holding_registers(32015, 80)

    smartlogger03.close()
    smartlogger31.close()
    smartlogger32.close()
    smartlogger33.close()
    print("Estou aqui6")
    
    energydaily03 = np.multiply(leiturasmartlogger03[13], 0.1)
    #corrente03 = np.multiply(leiturasmartlogger03[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger03[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger03[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger03[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger03[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger03[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger03[27], 0.1)

    correntePV_inv31 = np.multiply(leitura_inv31[2:38:2], 0.01)
    correntePV_inv32 = np.multiply(leitura_inv32[2:38:2], 0.01)
    correntePV_inv33 = np.multiply(leitura_inv33[2:38:2], 0.01)
    
    # tensaoPV_inv31 = np.multiply(leitura_inv31[1:37:2], 0.1)
    # tensaoPV_inv32 = np.multiply(leitura_inv32[1:37:2], 0.1)
    # tensaoPV_inv33 = np.multiply(leitura_inv33[1:37:2], 0.1)

    tensaoAC_inv31 = np.multiply(leitura_inv31[51:54:1], 0.1)
    tensaoAC_inv32 = np.multiply(leitura_inv32[51:54:1], 0.1)
    tensaoAC_inv33 = np.multiply(leitura_inv33[51:54:1], 0.1)

    corrente_inv31 = np.multiply(leitura_inv31[58:64:2], 0.001)
    corrente_inv32 = np.multiply(leitura_inv32[58:64:2], 0.001)
    corrente_inv33 = np.multiply(leitura_inv33[58:64:2], 0.001)

    tempinterna_inv31 = np.multiply(leitura_inv31[72], 0.1)
    tempinterna_inv32 = np.multiply(leitura_inv32[72], 0.1)
    tempinterna_inv33 = np.multiply(leitura_inv33[72], 0.1)

    potativaAC_inv31 = np.multiply(leitura_inv31[66], 0.001)
    potativaAC_inv32 = np.multiply(leitura_inv32[66], 0.001)
    potativaAC_inv33 = np.multiply(leitura_inv33[66], 0.001)

    InputPower_inv31= np.multiply(leitura_inv31[50], 0.001)
    InputPower_inv32 = np.multiply(leitura_inv32[50], 0.001)
    InputPower_inv33 = np.multiply(leitura_inv33[50], 0.001)


    aux_array31 = [tempinterna_inv31, potativaAC_inv31, InputPower_inv31]
    aux_array32 = [tempinterna_inv32, potativaAC_inv32, InputPower_inv32]
    aux_array33 = [tempinterna_inv33, potativaAC_inv33, InputPower_inv33]

    ret_inv31 = np.round(np.concatenate((np.array(aux_array31), np.array(tensaoAC_inv31), np.array(corrente_inv31), np.array(correntePV_inv31))),3)
    ret_inv32 = np.round(np.concatenate((np.array(aux_array32), np.array(tensaoAC_inv32), np.array(corrente_inv32), np.array(correntePV_inv32))),3)
    ret_inv33 = np.round(np.concatenate((np.array(aux_array33), np.array(tensaoAC_inv33), np.array(corrente_inv33), np.array(correntePV_inv33))),3)
    
    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger03 = np.round([energydaily03, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina03 = np.concatenate((np.array(data_hora), np.array(ret_smartogger03),np.array(ret_inv31), np.array(ret_inv32), np.array(ret_inv33)))

    return ret_usina03

def smartlogger_04():
    smartlogger04_endereco = '192.168.163.13'
    smartlogger04_porta= 502
    smartlogger04_ID = 101
    smartlogger04_ID1 = 11
    smartlogger04_ID2 = 12
    smartlogger04_ID3 = 13
    
    smartlogger04 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID)
    smartlogger41 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID1)
    smartlogger42 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID2)
    smartlogger43 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID3)
    print("Estou aqui7")
    smartlogger04.open()
    smartlogger41.open()
    smartlogger42.open()
    smartlogger43.open()

    leiturasmartlogger04 = smartlogger04.read_holding_registers(40550, 28)
    leitura_inv41 = smartlogger41.read_holding_registers(32015, 80)
    leitura_inv42 = smartlogger42.read_holding_registers(32015, 80)
    leitura_inv43 = smartlogger43.read_holding_registers(32015, 80)

    smartlogger04.close()
    smartlogger41.close()
    smartlogger42.close()
    smartlogger43.close()
    print("Estou aqui8")
    
    energydaily04 = np.multiply(leiturasmartlogger04[13], 0.1)
    #corrente04 = np.multiply(leiturasmartlogger04[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger04[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger04[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger04[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger04[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger04[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger04[27], 0.1)

    correntePV_inv41 = np.multiply(leitura_inv41[2:38:2], 0.01)
    correntePV_inv42 = np.multiply(leitura_inv42[2:38:2], 0.01)
    correntePV_inv43 = np.multiply(leitura_inv43[2:38:2], 0.01)
    
    # tensaoPV_inv41 = np.multiply(leitura_inv41[1:37:2], 0.1)
    # tensaoPV_inv42 = np.multiply(leitura_inv42[1:37:2], 0.1)
    # tensaoPV_inv43 = np.multiply(leitura_inv43[1:37:2], 0.1)

    tensaoAC_inv41 = np.multiply(leitura_inv41[51:54:1], 0.1)
    tensaoAC_inv42 = np.multiply(leitura_inv42[51:54:1], 0.1)
    tensaoAC_inv43 = np.multiply(leitura_inv43[51:54:1], 0.1)

    corrente_inv41 = np.multiply(leitura_inv41[58:64:2], 0.001)
    corrente_inv42 = np.multiply(leitura_inv42[58:64:2], 0.001)
    corrente_inv43 = np.multiply(leitura_inv43[58:64:2], 0.001)

    tempinterna_inv41 = np.multiply(leitura_inv41[72], 0.1)
    tempinterna_inv42 = np.multiply(leitura_inv42[72], 0.1)
    tempinterna_inv43 = np.multiply(leitura_inv43[72], 0.1)

    potativaAC_inv41 = np.multiply(leitura_inv41[66], 0.001)
    potativaAC_inv42 = np.multiply(leitura_inv42[66], 0.001)
    potativaAC_inv43 = np.multiply(leitura_inv43[66], 0.001)

    InputPower_inv41= np.multiply(leitura_inv41[50], 0.001)
    InputPower_inv42 = np.multiply(leitura_inv42[50], 0.001)
    InputPower_inv43 = np.multiply(leitura_inv43[50], 0.001)


    aux_array41 = [tempinterna_inv41, potativaAC_inv41, InputPower_inv41]
    aux_array42 = [tempinterna_inv42, potativaAC_inv42, InputPower_inv42]
    aux_array43 = [tempinterna_inv43, potativaAC_inv43, InputPower_inv43]

    ret_inv41 = np.round(np.concatenate((np.array(aux_array41), np.array(tensaoAC_inv41), np.array(corrente_inv41), np.array(correntePV_inv41))),3)
    ret_inv42 = np.round(np.concatenate((np.array(aux_array42), np.array(tensaoAC_inv42), np.array(corrente_inv42), np.array(correntePV_inv42))),3)
    ret_inv43 = np.round(np.concatenate((np.array(aux_array43), np.array(tensaoAC_inv43), np.array(corrente_inv43), np.array(correntePV_inv43))),3)
    
    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger04 = np.round([energydaily04, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina04 = np.concatenate((np.array(data_hora), np.array(ret_smartogger04),np.array(ret_inv41), np.array(ret_inv42), np.array(ret_inv43)))

    return ret_usina04

def smartlogger_05():
    smartlogger05_endereco = '192.168.163.14'
    smartlogger05_porta= 502
    smartlogger05_ID = 101
    smartlogger05_ID1 = 11
    smartlogger05_ID2 = 12
    
    smartlogger05 = ModbusClient(host=smartlogger05_endereco, port=smartlogger05_porta, unit_id=smartlogger05_ID)
    smartlogger51 = ModbusClient(host=smartlogger05_endereco, port=smartlogger05_porta, unit_id=smartlogger05_ID1)
    smartlogger52 = ModbusClient(host=smartlogger05_endereco, port=smartlogger05_porta, unit_id=smartlogger05_ID2)
    print("Estou aqui9")
    smartlogger05.open()
    smartlogger51.open()
    smartlogger52.open()

    leiturasmartlogger05 = smartlogger05.read_holding_registers(40550, 28)
    leitura_inv51 = smartlogger51.read_holding_registers(32015, 80)
    leitura_inv52 = smartlogger52.read_holding_registers(32015, 80)

    smartlogger05.close()
    smartlogger51.close()
    smartlogger52.close()
    print("Estou aqui10")
    
    energydaily05 = np.multiply(leiturasmartlogger05[13], 0.1)
    #corrente05 = np.multiply(leiturasmartlogger05[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger05[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger05[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger05[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger05[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger05[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger05[27], 0.1)

    correntePV_inv51 = np.multiply(leitura_inv51[2:38:2], 0.01)
    correntePV_inv52 = np.multiply(leitura_inv52[2:38:2], 0.01)
  
    # tensaoPV_inv51 = np.multiply(leitura_inv51[1:37:2], 0.1)
    # tensaoPV_inv52 = np.multiply(leitura_inv52[1:37:2], 0.1)

    tensaoAC_inv51 = np.multiply(leitura_inv51[51:54:1], 0.1)
    tensaoAC_inv52 = np.multiply(leitura_inv52[51:54:1], 0.1)

    corrente_inv51 = np.multiply(leitura_inv51[58:64:2], 0.001)
    corrente_inv52 = np.multiply(leitura_inv52[58:64:2], 0.001)

    tempinterna_inv51 = np.multiply(leitura_inv51[72], 0.1)
    tempinterna_inv52 = np.multiply(leitura_inv52[72], 0.1)
 
    potativaAC_inv51 = np.multiply(leitura_inv51[66], 0.001)
    potativaAC_inv52 = np.multiply(leitura_inv52[66], 0.001)

    InputPower_inv51= np.multiply(leitura_inv51[50], 0.001)
    InputPower_inv52 = np.multiply(leitura_inv52[50], 0.001)

    aux_array51 = [tempinterna_inv51, potativaAC_inv51, InputPower_inv51]
    aux_array52 = [tempinterna_inv52, potativaAC_inv52, InputPower_inv52]

    ret_inv51 = np.round(np.concatenate((np.array(aux_array51), np.array(tensaoAC_inv51), np.array(corrente_inv51), np.array(correntePV_inv51))),3)
    ret_inv52 = np.round(np.concatenate((np.array(aux_array52), np.array(tensaoAC_inv52), np.array(corrente_inv52), np.array(correntePV_inv52))),3)

    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger05 = np.round([energydaily05, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina05 = np.concatenate((np.array(data_hora), np.array(ret_smartogger05),np.array(ret_inv51), np.array(ret_inv52)))

    return ret_usina05

def smartlogger_06():
    smartlogger06_endereco = '192.168.163.15'
    smartlogger06_porta= 502
    smartlogger06_ID = 101
    smartlogger06_ID1 = 11
    smartlogger06_ID2 = 12
    
    smartlogger06 = ModbusClient(host=smartlogger06_endereco, port=smartlogger06_porta, unit_id=smartlogger06_ID)
    smartlogger61 = ModbusClient(host=smartlogger06_endereco, port=smartlogger06_porta, unit_id=smartlogger06_ID1)
    smartlogger62 = ModbusClient(host=smartlogger06_endereco, port=smartlogger06_porta, unit_id=smartlogger06_ID2)
    print("Estou aqui11")
    smartlogger06.open()
    smartlogger61.open()
    smartlogger62.open()

    leiturasmartlogger06 = smartlogger06.read_holding_registers(40550, 28)
    leitura_inv61 = smartlogger61.read_holding_registers(32015, 80)
    leitura_inv62 = smartlogger62.read_holding_registers(32015, 80)
 
    smartlogger06.close()
    smartlogger61.close()
    smartlogger62.close()
    print("Estou aqui12")
    
    energydaily06 = np.multiply(leiturasmartlogger06[13], 0.1)
    #corrente06 = np.multiply(leiturasmartlogger06[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger06[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger06[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger06[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger06[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger06[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger06[27], 0.1)

    correntePV_inv61 = np.multiply(leitura_inv61[2:38:2], 0.01)
    correntePV_inv62 = np.multiply(leitura_inv62[2:38:2], 0.01)
  
    # tensaoPV_inv61 = np.multiply(leitura_inv61[1:37:2], 0.1)
    # tensaoPV_inv62 = np.multiply(leitura_inv62[1:37:2], 0.1)

    tensaoAC_inv61 = np.multiply(leitura_inv61[51:54:1], 0.1)
    tensaoAC_inv62 = np.multiply(leitura_inv62[51:54:1], 0.1)

    corrente_inv61 = np.multiply(leitura_inv61[58:64:2], 0.001)
    corrente_inv62 = np.multiply(leitura_inv62[58:64:2], 0.001)

    tempinterna_inv61 = np.multiply(leitura_inv61[72], 0.1)
    tempinterna_inv62 = np.multiply(leitura_inv62[72], 0.1)
 
    potativaAC_inv61 = np.multiply(leitura_inv61[66], 0.001)
    potativaAC_inv62 = np.multiply(leitura_inv62[66], 0.001)

    InputPower_inv61= np.multiply(leitura_inv61[50], 0.001)
    InputPower_inv62 = np.multiply(leitura_inv62[50], 0.001)

    aux_array61 = [tempinterna_inv61, potativaAC_inv61, InputPower_inv61]
    aux_array62 = [tempinterna_inv62, potativaAC_inv62, InputPower_inv62]

    ret_inv61 = np.round(np.concatenate((np.array(aux_array61), np.array(tensaoAC_inv61), np.array(corrente_inv61), np.array(correntePV_inv61))),3)
    ret_inv62 = np.round(np.concatenate((np.array(aux_array62), np.array(tensaoAC_inv62), np.array(corrente_inv62), np.array(correntePV_inv62))),3)

    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger06 = np.round([energydaily06, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina06 = np.concatenate((np.array(data_hora), np.array(ret_smartogger06),np.array(ret_inv61), np.array(ret_inv62)))

    return ret_usina06

def smartlogger_07():

    smartlogger07_endereco = '192.168.163.16'
    smartlogger07_porta= 502
    smartlogger07_ID = 101
    smartlogger07_ID1 = 11
    smartlogger07_ID2 = 12
    
    smartlogger07 = ModbusClient(host=smartlogger07_endereco, port=smartlogger07_porta, unit_id=smartlogger07_ID)
    smartlogger71 = ModbusClient(host=smartlogger07_endereco, port=smartlogger07_porta, unit_id=smartlogger07_ID1)
    smartlogger72 = ModbusClient(host=smartlogger07_endereco, port=smartlogger07_porta, unit_id=smartlogger07_ID2)
    print("Estou aqui13")
    smartlogger07.open()
    smartlogger71.open()
    smartlogger72.open()

    leiturasmartlogger07 = smartlogger07.read_holding_registers(40550, 28)
    leitura_inv71 = smartlogger71.read_holding_registers(32015, 80)
    leitura_inv72 = smartlogger72.read_holding_registers(32015, 80)

    smartlogger07 .close()
    smartlogger71 .close()
    smartlogger72 .close()
    print("Estou aqui14")
    
    energydaily07 = np.multiply(leiturasmartlogger07[13], 0.1)
    #corrente07 = np.multiply(leiturasmartlogger07[5], 0.1)
    corrente_smart_A = np.multiply(leiturasmartlogger07[22], 1)
    corrente_smart_B = np.multiply(leiturasmartlogger07[23], 1)
    corrente_smart_C = np.multiply(leiturasmartlogger07[24], 1)
    tensao_smart_A = np.multiply(leiturasmartlogger07[25], 0.1)
    tensao_smart_B = np.multiply(leiturasmartlogger07[26], 0.1)
    tensao_smart_C = np.multiply(leiturasmartlogger07[27], 0.1)

    correntePV_inv71 = np.multiply(leitura_inv71[2:38:2], 0.01)
    correntePV_inv72 = np.multiply(leitura_inv72[2:38:2], 0.01)
  
    # tensaoPV_inv71 = np.multiply(leitura_inv71[1:37:2], 0.1)
    # tensaoPV_inv72 = np.multiply(leitura_inv72[1:37:2], 0.1)

    tensaoAC_inv71 = np.multiply(leitura_inv71[51:54:1], 0.1)
    tensaoAC_inv72 = np.multiply(leitura_inv72[51:54:1], 0.1)

    corrente_inv71 = np.multiply(leitura_inv71[58:64:2], 0.001)
    corrente_inv72 = np.multiply(leitura_inv72[58:64:2], 0.001)

    tempinterna_inv71 = np.multiply(leitura_inv71[72], 0.1)
    tempinterna_inv72 = np.multiply(leitura_inv72[72], 0.1)
 
    potativaAC_inv71 = np.multiply(leitura_inv71[66], 0.001)
    potativaAC_inv72 = np.multiply(leitura_inv72[66], 0.001)

    InputPower_inv71= np.multiply(leitura_inv71[50], 0.001)
    InputPower_inv72 = np.multiply(leitura_inv72[50], 0.001)

    aux_array71 = [tempinterna_inv71, potativaAC_inv71, InputPower_inv71]
    aux_array72 = [tempinterna_inv72, potativaAC_inv72, InputPower_inv72]

    ret_inv71 = np.round(np.concatenate((np.array(aux_array71), np.array(tensaoAC_inv71), np.array(corrente_inv71), np.array(correntePV_inv71))),3)
    ret_inv72 = np.round(np.concatenate((np.array(aux_array72), np.array(tensaoAC_inv72), np.array(corrente_inv72), np.array(correntePV_inv72))),3)

    agora = datetime.now()
    data_hora = [agora.strftime("%d/%m/%Y %H:%M")]
    ret_smartogger07 = np.round([energydaily07, corrente_smart_A, corrente_smart_B, corrente_smart_C, tensao_smart_A, tensao_smart_B, tensao_smart_C],3)
    ret_usina07 = np.concatenate((np.array(data_hora), np.array(ret_smartogger07),np.array(ret_inv71), np.array(ret_inv72)))

    return ret_usina07

def tracker():

    ncu_endereco = '192.168.163.17'
    ncu_porta = 502
    ncu_ID = 1
    inicio_endereco = 30151
    ntrackers = 5
    i= 1
    ret_tag = []
    ret_trackers = []
       
    ncu_comunicacao = ModbusClient(host=ncu_endereco, port=ncu_porta, unit_id=ncu_ID)
    ncu_comunicacao.open()
  
    # Loop para ler os dados de cada tracker
    for i in range(ntrackers):

        leitura_ncu = ncu_comunicacao.read_holding_registers(inicio_endereco, 20)
        tracker = ntrackers
        tensaopainel =              np.multiply(leitura_ncu[0], 0.001) 
        posicao =                   np.multiply(leitura_ncu[1],0.1745)
        correntemotor =             np.multiply(leitura_ncu[3], 0.001) 
        correntepicomotor =         np.multiply(leitura_ncu[4], 0.001) 
        targetangle =               np.multiply(leitura_ncu[5], 0.001) 
        correntepainel =            np.multiply(leitura_ncu[7], 0.001) #30158
        tensaobateria =             np.multiply(leitura_ncu[11], 0.001) #30162
        correntebateria =           np.multiply(leitura_ncu[13], 0.001)
        temperaturabateria_aux =    np.multiply(leitura_ncu[15], 0.1)
        temperaturabateria = temperaturabateria_aux - 273.15
        inicio_endereco = inicio_endereco+22
        num_tracker = f"{i+1:02}"
        colunas = [f"TRACKER_{num_tracker}.MED.PanelVoltage", f"TRACKER_{num_tracker}.MED.PanelCurrent", f"TRACKER_{num_tracker}.MED.Position", 
                   f"TRACKER_{num_tracker}.MED.TargetAngl", f"TRACKER_{num_tracker}.MED.MotorCurrent", f"TRACKER_{num_tracker}.MED.MotorCurrentPeak", 
                   f"TRACKER_{num_tracker}.MED.Voltage", f"TRACKER_{num_tracker}.MED.Current", f"TRACKER_{num_tracker}.MED.TempPcb_Kelvin"]
        
        ret_tag = ret_tag + colunas
        dados_tracker_atual = [tensaopainel, correntepainel, posicao, targetangle, correntemotor, correntepicomotor, tensaobateria, correntebateria, temperaturabateria] 
        ret_trackers =  ret_trackers + dados_tracker_atual
        
        time.sleep(0.5)
        print(i)
    
    ncu_comunicacao.close()
    print(ret_tag)
    print("\n")
    print(ret_trackers)
    return ret_tag, ret_trackers
    
def pextron():
    moxa_endereco = '192.168.163.6'
    rele1_porta = 4001
    rele1_ID = 1

    rele_comunicacao = ModbusClient(host=moxa_endereco, port=rele1_porta, unit_id=rele1_ID, auto_open = True, auto_close = True)
    leitura_rele = rele_comunicacao.read_holding_registers(700, 100)
    print(leitura_rele)

def salvar_estmet(estmet):
    print(estmet)
    
    colunas = ['GHI', 'IPOA', 'ALBEDÔMETRO', 'TEMP. MÓDULO', 'TEMP. AMBIENTE']
    dados_dict = {titulo: dado for titulo, dado in zip(colunas, estmet)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "ESTMET3" já existe
        if "ESTMET" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "ESTMET3"
            df_concatenado = pd.concat([df_existente["ESTMET"], df], ignore_index=True)
        else:
            # Se a aba "ESTMET3" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "ESTMET3"
            df_concatenado.to_excel(writer, index=False, sheet_name="ESTMET")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="ESTMET")

def salvar_usina01(usina01):
    #print(usina01)
    tag11 = []
    tag12 = [] 
    tag13 = []   

    for i in range(18):
        tag_corrente11 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente12 = [f"INV1_2.MED.AMP_S{i+1}"]
        tag_corrente13 = [f"INV1_3.MED.AMP_S{i+1}"]
        tag11 += tag_corrente11
        tag12 += tag_corrente12
        tag13 += tag_corrente13
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv11 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv12 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    tag_inv13 = ["INV1_3.MED.TEMP_INT", "INV1_3.MED.kW", "INV1_3.MED.INPUT_POWER", "INV1_3.MED.VAB", "INV1_3.MED.VBC", "INV1_3.MED.VCA", "INV1_3.MED.IA", "INV1_3.MED.IB", "INV1_3.MED.IC"]
    colunas = tagsmartlogger + tag_inv11 + tag11 + tag_inv12 + tag12 + tag_inv13 + tag13

    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina01)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA01" já existe
        if "USINA01" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA01"
            df_concatenado = pd.concat([df_existente["USINA01"], df], ignore_index=True)
        else:
            # Se a aba "USINA01" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA01"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA01")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA01")

def salvar_usina02(usina02):
   #print(usina02)
    tag21 = []
    tag22 = [] 
    tag23 = []   

    for i in range(18):
        tag_corrente21 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente22 = [f"INV1_2.MED.AMP_S{i+1}"]
        tag_corrente23 = [f"INV1_3.MED.AMP_S{i+1}"]
        tag21 += tag_corrente21
        tag22 += tag_corrente22
        tag23 += tag_corrente23
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv21 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv22 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    tag_inv23 = ["INV1_3.MED.TEMP_INT", "INV1_3.MED.kW", "INV1_3.MED.INPUT_POWER", "INV1_3.MED.VAB", "INV1_3.MED.VBC", "INV1_3.MED.VCA", "INV1_3.MED.IA", "INV1_3.MED.IB", "INV1_3.MED.IC"]
    colunas = tagsmartlogger + tag_inv21 + tag21 + tag_inv22 + tag22 + tag_inv23 + tag23

    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina02)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA02" já existe
        if "USINA02" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA02"
            df_concatenado = pd.concat([df_existente["USINA02"], df], ignore_index=True)
        else:
            # Se a aba "USINA02" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA02"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA02")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA02")

def salvar_usina03(usina03):
    print(usina03)
    tag31 = []
    tag32 = [] 
    tag33 = []   

    for i in range(18):
        tag_corrente31 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente32 = [f"INV1_2.MED.AMP_S{i+1}"]
        tag_corrente33 = [f"INV1_3.MED.AMP_S{i+1}"]
        tag31 += tag_corrente31
        tag32 += tag_corrente32
        tag33 += tag_corrente33
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv31 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv32 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    tag_inv33 = ["INV1_3.MED.TEMP_INT", "INV1_3.MED.kW", "INV1_3.MED.INPUT_POWER", "INV1_3.MED.VAB", "INV1_3.MED.VBC", "INV1_3.MED.VCA", "INV1_3.MED.IA", "INV1_3.MED.IB", "INV1_3.MED.IC"]
    colunas = tagsmartlogger + tag_inv31 + tag31 + tag_inv32 + tag32 + tag_inv33 + tag33


    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina03)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA03" já existe
        if "USINA03" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA03"
            df_concatenado = pd.concat([df_existente["USINA03"], df], ignore_index=True)
        else:
            # Se a aba "USINA03" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA03"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA03")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA03")

def salvar_usina04(usina04):
    print(usina04)
    tag41 = []
    tag42 = [] 
    tag43 = []   

    for i in range(18):
        tag_corrente41 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente42 = [f"INV1_2.MED.AMP_S{i+1}"]
        tag_corrente43 = [f"INV1_3.MED.AMP_S{i+1}"]
        tag41 += tag_corrente41
        tag42 += tag_corrente42
        tag43 += tag_corrente43
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv41 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv42 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    tag_inv43 = ["INV1_3.MED.TEMP_INT", "INV1_3.MED.kW", "INV1_3.MED.INPUT_POWER", "INV1_3.MED.VAB", "INV1_3.MED.VBC", "INV1_3.MED.VCA", "INV1_3.MED.IA", "INV1_3.MED.IB", "INV1_3.MED.IC"]
    colunas = tagsmartlogger + tag_inv41 + tag41 + tag_inv42 + tag42 + tag_inv43 + tag43


    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina04)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA04" já existe
        if "USINA04" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA04"
            df_concatenado = pd.concat([df_existente["USINA04"], df], ignore_index=True)
        else:
            # Se a aba "USINA04" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA04"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA04")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA04")

def salvar_usina05(usina05):
    print(usina05)
    
    tag51 = []
    tag52 = [] 
    

    for i in range(18):
        tag_corrente51 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente52 = [f"INV1_2.MED.AMP_S{i+1}"]

        tag51 += tag_corrente51
        tag52 += tag_corrente52
     
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv51 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv52 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    
    colunas = tagsmartlogger + tag_inv51 + tag51 + tag_inv52 + tag52


    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina05)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA05" já existe
        if "USINA05" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA05"
            df_concatenado = pd.concat([df_existente["USINA05"], df], ignore_index=True)
        else:
            # Se a aba "USINA05" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA05"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA05")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA05")

def salvar_usina06(usina06):
    print(usina06)
    
    
    tag61 = []
    tag62 = [] 
    

    for i in range(18):
        tag_corrente61 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente62 = [f"INV1_2.MED.AMP_S{i+1}"]

        tag61 += tag_corrente61
        tag62 += tag_corrente62
     
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv61 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv62 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    
    colunas = tagsmartlogger + tag_inv61 + tag61 + tag_inv62 + tag62

    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina06)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA06" já existe
        if "USINA06" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA06"
            df_concatenado = pd.concat([df_existente["USINA06"], df], ignore_index=True)
        else:
            # Se a aba "USINA06" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA06"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA06")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA06")

def salvar_usina07(usina07):
    print(usina07)

    
    tag72 = []
    tag72 = [] 
    

    for i in range(18):
        tag_corrente72 = [f"INV1_1.MED.AMP_S{i+1}"]
        tag_corrente72 = [f"INV1_2.MED.AMP_S{i+1}"]

        tag72 += tag_corrente72
        tag72 += tag_corrente72
     
    
    tagsmartlogger = ["DATA HORA", "SMARTLOGGER1.MED.kWh_Dia", "SMARTLOGGER1.MED.IA", "SMARTLOGGER1.MED.IB", "SMARTLOGGER1.MED.IC", "SMARTLOGGER1.MED.VAB", "SMARTLOGGER1.MED.VBC", "SMARTLOGGER1.MED.VCA"]
    tag_inv72 = ["INV1_1.MED.TEMP_INT", "INV1_1.MED.kW", "INV1_1.MED.INPUT_POWER", "INV1_1.MED.VAB", "INV1_1.MED.VBC", "INV1_1.MED.VCA", "INV1_1.MED.IA", "INV1_1.MED.IB", "INV1_1.MED.IC"]
    tag_inv72 = ["INV1_2.MED.TEMP_INT", "INV1_2.MED.kW", "INV1_2.MED.INPUT_POWER", "INV1_2.MED.VAB", "INV1_2.MED.VBC", "INV1_2.MED.VCA", "INV1_2.MED.IA", "INV1_2.MED.IB", "INV1_2.MED.IC"]
    
    colunas = tagsmartlogger + tag_inv72 + tag72 + tag_inv72 + tag72

    dados_dict = {titulo: dado for titulo, dado in zip(colunas, usina07)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "USINA07" já existe
        if "USINA07" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "USINA07"
            df_concatenado = pd.concat([df_existente["USINA07"], df], ignore_index=True)
        else:
            # Se a aba "USINA07" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "USINA07"
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA07")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="USINA07")

def salvar_trackers(tags, trackers):
    print(tags)
    print("/n")
    print(trackers)

    colunas = tags
    dados_dict = {titulo: dado for titulo, dado in zip(colunas, trackers)}
    df = pd.DataFrame(dados_dict, index=[0])
    nome_arquivo = 'C:/Users/rosantos/Documents/AUTOMAÇÃO/UFV CEILÂNDIA/dados.xlsx'

    try:
        # Ler o arquivo Excel existente
        df_existente = pd.read_excel(nome_arquivo, sheet_name=None)

        # Verificar se a aba "TRACKERS" já existe
        if "TRACKERS" in df_existente:
            # Concatenar o DataFrame existente com os novos dados na aba "TRACKERS"
            df_concatenado = pd.concat([df_existente["TRACKERS"], df], ignore_index=True)
        else:
            # Se a aba "TRACKERS" não existir, criar um novo DataFrame com os novos dados
            df_concatenado = df

        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            # Adicionar o DataFrame na aba "TRACKERS"
            df_concatenado.to_excel(writer, index=False, sheet_name="TRACKERS")
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame com os novos dados
        df_concatenado = df
        # Salvar o DataFrame completo em um novo arquivo Excel
        with pd.ExcelWriter(nome_arquivo, mode='w', engine='openpyxl') as writer:
            df_concatenado.to_excel(writer, index=False, sheet_name="TRACKERS")


def main():
    # estmet = estacao_solarimetrica()
    #usina01 = smartlogger_01()
    #time.sleep(2)
    # usina02 = smartlogger_02()
    # usina03 = smartlogger_03()
    # usina04 = smartlogger_04()
    # usina05 = smartlogger_05()
    # usina06 = smartlogger_06()
    # usina07 = smartlogger_07()
    #tags, trackers = tracker() 
    # reles = pextron()
   
    # dados_estemet = salvar_estmet(estmet)
    # dados_usina01 = salvar_usina01(usina01)
    # time.sleep(1)
    # dados_usina02 = salvar_usina02(usina02)
    # time.sleep(1)
    # dados_usina03 = salvar_usina03(usina03)
    # time.sleep(1)
    # dados_usina04 = salvar_usina04(usina04)
    # time.sleep(1)
    # dados_usina05 = salvar_usina05(usina05)
    # time.sleep(1)    
    # dados_usina06 = salvar_usina06(usina06)
    # time.sleep(1)
    # dados_usina07 = salvar_usina07(usina07)
    #dados_trackers = salvar_trackers(tags, trackers)
    teste()


if __name__ == "__main__":
    main()
