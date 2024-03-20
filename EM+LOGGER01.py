from pyModbusTCP.client import ModbusClient
import numpy as np

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
    print("ESTAÇÃO SOLARIMÉTRICA \n")
    print(f'PIRANÔMETRO GHI = {valor_em[0]:.2f} (W/m²)')
    print(f'PIRANÔMETRO IPOA = {valor_em[1]:.2f} (W/m²)')
    print(f'ALBEDÔMETRO= {valor_em[2]:.2f} (W/m²)')
    print(f'TEMP. MÓDULO = {valor_em[3]:.2f} (ºC)')
    print(f'TEMP. AMBIENTE = {valor_em[4]:.2f} (ºC)')


def smartlogger_01():
    smartlogger01_endereco = '192.168.163.10'
    smartlogger01_porta= 502
    smartlogger01_ID1 = 11
    smartlogger01_ID2 = 12
    smartlogger01_ID3 = 13
    
    smartlogger11 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID1, auto_open=True, auto_close=True)
    smartlogger12 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID2, auto_open=True, auto_close=True)
    smartlogger13 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID3, auto_open=True, auto_close=True)
    
    def correntePV():

        leitura_inv11 = smartlogger11.read_holding_registers(32017, 36)
        leitura_inv12 = smartlogger12.read_holding_registers(32017, 36)
        leitura_inv13 = smartlogger13.read_holding_registers(32017, 36)

        dados_inv11 = np.multiply(leitura_inv11, 0.01)
        dados_inv12 = np.multiply(leitura_inv12, 0.01)
        dados_inv13 = np.multiply(leitura_inv13, 0.01)

        correntePV_inv11 = [dados_inv11[i] for i in range(0, len(dados_inv11), 2)]
        correntePV_inv12 = [dados_inv12[i] for i in range(0, len(dados_inv12), 2)]
        correntePV_inv13 = [dados_inv13[i] for i in range(0, len(dados_inv13), 2)]
        
        print("\nSMARTLOGGER 01 \n")
        print("\nINVERSOR  01 \n") 
        print(correntePV_inv11)
        print("\nINVERSOR  02 \n") 
        print(correntePV_inv12)
        print("\nINVERSOR  03 \n") 
        print(correntePV_inv13)
    
    correntePV()
  

def main():
    estmet = estacao_solarimetrica()
    smartlogger_U01 = smartlogger_01()


if __name__ == "__main__":
    main()
