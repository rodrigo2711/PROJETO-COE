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

def smartloggers():

    def smartlogger_01():
        smartlogger01_endereco = '192.168.163.10'
        smartlogger01_porta= 502
        smartlogger01_ID = 10
        smartlogger01_ID1 = 11
        smartlogger01_ID2 = 12
        smartlogger01_ID3 = 13
        
        
        smartlogger01 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID, auto_open=True, auto_close=True)
        smartlogger11 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID1, auto_open=True, auto_close=True)
        smartlogger12 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID2, auto_open=True, auto_close=True)
        smartlogger13 = ModbusClient(host=smartlogger01_endereco, port=smartlogger01_porta, unit_id=smartlogger01_ID3, auto_open=True, auto_close=True)
        
        leiturasmartlogger01 = smartlogger01.read_holding_registers(40550, 28)
        leitura_inv11 = smartlogger11.read_holding_registers(32015, 80)
        leitura_inv12 = smartlogger12.read_holding_registers(32015, 80)
        leitura_inv13 = smartlogger13.read_holding_registers(32015, 80)

        
        def correnteDC():

            energydaily01 = np.multiply(leiturasmartlogger01[13], 0.1)
            correnteDC01 = np.multiply(leiturasmartlogger01[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger01[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger01[25:29:1], 0.1)
            
            correnteDC_inv11 = np.multiply(leitura_inv11[2:38:2], 0.01)
            correnteDC_inv12 = np.multiply(leitura_inv12[2:38:2], 0.01)
            correnteDC_inv13 = np.multiply(leitura_inv13[2:38:2], 0.01)
            
            tensaoDC_inv11 = np.multiply(leitura_inv11[1:37:2], 0.1)
            tensaoDC_inv12 = np.multiply(leitura_inv12[1:37:2], 0.1)
            tensaoDC_inv13 = np.multiply(leitura_inv13[1:37:2], 0.1)

            tempinterna_inv11 = np.multiply(leitura_inv11[72], 0.1)
            tempinterna_inv12 = np.multiply(leitura_inv12[72], 0.1)
            tempinterna_inv13 = np.multiply(leitura_inv13[72], 0.1)

            tensoaAC_inv11 = np.multiply(leitura_inv11[51:54:1], 0.1)
            tensoaAC_inv12 = np.multiply(leitura_inv12[51:54:1], 0.1)
            tensoaAC_inv13 = np.multiply(leitura_inv13[51:54:1], 0.1)

            correnteAC_inv11 = np.multiply(leitura_inv11[58:64:2], 0.001)
            correnteAC_inv12 = np.multiply(leitura_inv12[58:64:2], 0.001)
            correnteAC_inv13 = np.multiply(leitura_inv13[58:64:2], 0.001)

            potativaAC_inv11 = np.multiply(leitura_inv11[66], 0.1)
            potativaAC_inv12 = np.multiply(leitura_inv12[66], 0.1)
            potativaAC_inv13 = np.multiply(leitura_inv13[66], 0.1)

            potenciaDC_inv11 = np.multiply(leitura_inv11[50], 0.1)
            potenciaDC_inv12 = np.multiply(leitura_inv12[50], 0.1)
            potenciaDC_inv13 = np.multiply(leitura_inv13[50], 0.1)

        correnteDC()

    def smartlogger_02():
        smartlogger02_endereco = '192.168.163.11'
        smartlogger02_porta= 502
        smartlogger02_ID = 101
        smartlogger02_ID1 = 11
        smartlogger02_ID2 = 12
        smartlogger02_ID3 = 13
        
        smartlogger02 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID, auto_open=True, auto_close=True)
        smartlogger21 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID1, auto_open=True, auto_close=True)
        smartlogger22 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID2, auto_open=True, auto_close=True)
        smartlogger23 = ModbusClient(host=smartlogger02_endereco, port=smartlogger02_porta, unit_id=smartlogger02_ID3, auto_open=True, auto_close=True)
        
        leiturasmartlogger02 = smartlogger02.read_holding_registers(40550, 28)
        leitura_inv21 = smartlogger21.read_holding_registers(32015, 80)
        leitura_inv22 = smartlogger22.read_holding_registers(32015, 80)
        leitura_inv23 = smartlogger23.read_holding_registers(32015, 80)
        #print(leitura_inv21)
        
        def correnteDC():

            energydaily02 = np.multiply(leiturasmartlogger02[13], 0.1)
            correnteDC02 = np.multiply(leiturasmartlogger02[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger02[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger02[25:29:1], 0.1)

            correnteDC_inv21 = np.multiply(leitura_inv21[2:38:2], 0.01)
            correnteDC_inv22 = np.multiply(leitura_inv22[2:38:2], 0.01)
            correnteDC_inv23 = np.multiply(leitura_inv23[2:38:2], 0.01)
            
            tensaoDC_inv21 = np.multiply(leitura_inv21[1:37:2], 0.1)
            tensaoDC_inv22 = np.multiply(leitura_inv22[1:37:2], 0.1)
            tensaoDC_inv23 = np.multiply(leitura_inv23[1:37:2], 0.1)

            tempinterna_inv21 = np.multiply(leitura_inv21[72], 0.1)
            tempinterna_inv22 = np.multiply(leitura_inv22[72], 0.1)
            tempinterna_inv23 = np.multiply(leitura_inv23[72], 0.1)

            tensoaAC_inv21 = np.multiply(leitura_inv21[51:54:1], 0.1)
            tensoaAC_inv22 = np.multiply(leitura_inv22[51:54:1], 0.1)
            tensoaAC_inv23 = np.multiply(leitura_inv23[51:54:1], 0.1)

            correnteAC_inv21 = np.multiply(leitura_inv21[58:64:2], 0.001)
            correnteAC_inv22 = np.multiply(leitura_inv22[58:64:2], 0.001)
            correnteAC_inv23 = np.multiply(leitura_inv23[58:64:2], 0.001)

            potativaAC_inv21 = np.multiply(leitura_inv21[66], 0.1)
            potativaAC_inv22 = np.multiply(leitura_inv22[66], 0.1)
            potativaAC_inv23 = np.multiply(leitura_inv23[66], 0.1)

            potenciaDC_inv21 = np.multiply(leitura_inv21[50], 0.1)
            potenciaDC_inv22 = np.multiply(leitura_inv22[50], 0.1)
            potenciaDC_inv23 = np.multiply(leitura_inv23[50], 0.1)

        
        correnteDC()

    def smartlogger_03():
        smartlogger03_endereco = '192.168.163.12'
        smartlogger03_porta= 502
        smartlogger03_ID = 101
        smartlogger03_ID1 = 11
        smartlogger03_ID2 = 12
        smartlogger03_ID3 = 13
        
        smartlogger03 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID, auto_open=True, auto_close=True)
        smartlogger31 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID1, auto_open=True, auto_close=True)
        smartlogger32 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID2, auto_open=True, auto_close=True)
        smartlogger33 = ModbusClient(host=smartlogger03_endereco, port=smartlogger03_porta, unit_id=smartlogger03_ID3, auto_open=True, auto_close=True)
        
        leiturasmartlogger03 = smartlogger03.read_holding_registers(40550, 28)
        leitura_inv31 = smartlogger31.read_holding_registers(32015, 80)
        leitura_inv32 = smartlogger32.read_holding_registers(32015, 80)
        leitura_inv33 = smartlogger33.read_holding_registers(32015, 80)
        #print(leitura_inv31)
        
        def correnteDC():

            energydaily03 = np.multiply(leiturasmartlogger03[13], 0.1)
            correnteDC03 = np.multiply(leiturasmartlogger03[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger03[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger03[25:29:1], 0.1)

            correnteDC_inv31 = np.multiply(leitura_inv31[2:38:2], 0.01)
            correnteDC_inv32 = np.multiply(leitura_inv32[2:38:2], 0.01)
            correnteDC_inv33 = np.multiply(leitura_inv33[2:38:2], 0.01)
            
            tensaoDC_inv31 = np.multiply(leitura_inv31[1:37:2], 0.1)
            tensaoDC_inv32 = np.multiply(leitura_inv32[1:37:2], 0.1)
            tensaoDC_inv33 = np.multiply(leitura_inv33[1:37:2], 0.1)

            tempinterna_inv31 = np.multiply(leitura_inv31[72], 0.1)
            tempinterna_inv32 = np.multiply(leitura_inv32[72], 0.1)
            tempinterna_inv33 = np.multiply(leitura_inv33[72], 0.1)

            tensoaAC_inv31 = np.multiply(leitura_inv31[51:54:1], 0.1)
            tensoaAC_inv32 = np.multiply(leitura_inv32[51:54:1], 0.1)
            tensoaAC_inv33 = np.multiply(leitura_inv33[51:54:1], 0.1)

            correnteAC_inv31 = np.multiply(leitura_inv31[58:64:2], 0.001)
            correnteAC_inv32 = np.multiply(leitura_inv32[58:64:2], 0.001)
            correnteAC_inv33 = np.multiply(leitura_inv33[58:64:2], 0.001)

            potativaAC_inv31 = np.multiply(leitura_inv31[66], 0.1)
            potativaAC_inv32 = np.multiply(leitura_inv32[66], 0.1)
            potativaAC_inv33 = np.multiply(leitura_inv33[66], 0.1)

            potenciaDC_inv31 = np.multiply(leitura_inv31[50], 0.1)
            potenciaDC_inv32 = np.multiply(leitura_inv32[50], 0.1)
            potenciaDC_inv33 = np.multiply(leitura_inv33[50], 0.1)

        correnteDC()

    def smartlogger_04():
        smartlogger04_endereco = '192.168.163.13'
        smartlogger04_porta= 502
        smartlogger04_ID = 101
        smartlogger04_ID1 = 11
        smartlogger04_ID2 = 12
        smartlogger04_ID3 = 13
        
        smartlogger04 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID, auto_open=True, auto_close=True)
        smartlogger41 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID1, auto_open=True, auto_close=True)
        smartlogger42 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID2, auto_open=True, auto_close=True)
        smartlogger43 = ModbusClient(host=smartlogger04_endereco, port=smartlogger04_porta, unit_id=smartlogger04_ID3, auto_open=True, auto_close=True)
        
        leiturasmartlogger04 = smartlogger04.read_holding_registers(40550, 28)
        leitura_inv41 = smartlogger41.read_holding_registers(32015, 80)
        leitura_inv42 = smartlogger42.read_holding_registers(32015, 80)
        leitura_inv43 = smartlogger43.read_holding_registers(32015, 80)
        #print(leitura_inv41)
        
        def correnteDC():

            energydaily04 = np.multiply(leiturasmartlogger04[13], 0.1)
            correnteDC04 = np.multiply(leiturasmartlogger04[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger04[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger04[25:29:1], 0.1)

            correnteDC_inv41 = np.multiply(leitura_inv41[2:38:2], 0.01)
            correnteDC_inv42 = np.multiply(leitura_inv42[2:38:2], 0.01)
            correnteDC_inv43 = np.multiply(leitura_inv43[2:38:2], 0.01)
            
            tensaoDC_inv41 = np.multiply(leitura_inv41[1:37:2], 0.1)
            tensaoDC_inv42 = np.multiply(leitura_inv42[1:37:2], 0.1)
            tensaoDC_inv43 = np.multiply(leitura_inv43[1:37:2], 0.1)

            tempinterna_inv41 = np.multiply(leitura_inv41[72], 0.1)
            tempinterna_inv42 = np.multiply(leitura_inv42[72], 0.1)
            tempinterna_inv43 = np.multiply(leitura_inv43[72], 0.1)

            tensoaAC_inv41 = np.multiply(leitura_inv41[51:54:1], 0.1)
            tensoaAC_inv42 = np.multiply(leitura_inv42[51:54:1], 0.1)
            tensoaAC_inv43 = np.multiply(leitura_inv43[51:54:1], 0.1)

            correnteAC_inv41 = np.multiply(leitura_inv41[58:64:2], 0.001)
            correnteAC_inv42 = np.multiply(leitura_inv42[58:64:2], 0.001)
            correnteAC_inv43 = np.multiply(leitura_inv43[58:64:2], 0.001)

            potativaAC_inv41 = np.multiply(leitura_inv41[66], 0.1)
            potativaAC_inv42 = np.multiply(leitura_inv42[66], 0.1)
            potativaAC_inv43 = np.multiply(leitura_inv43[66], 0.1)

            potenciaDC_inv41 = np.multiply(leitura_inv41[50], 0.1)
            potenciaDC_inv42 = np.multiply(leitura_inv42[50], 0.1)
            potenciaDC_inv43 = np.multiply(leitura_inv43[50], 0.1)

        correnteDC()

    def smartlogger_05():
        smartlogger05_endereco = '192.168.163.14'
        smartlogger05_porta= 502
        smartlogger05_ID = 101
        smartlogger05_ID1 = 11
        smartlogger05_ID2 = 12
        
        smartlogger05 = ModbusClient(host=smartlogger05_endereco, port=smartlogger05_porta, unit_id=smartlogger05_ID, auto_open=True, auto_close=True)
        smartlogger51 = ModbusClient(host=smartlogger05_endereco, port=smartlogger05_porta, unit_id=smartlogger05_ID1, auto_open=True, auto_close=True)
        smartlogger52 = ModbusClient(host=smartlogger05_endereco, port=smartlogger05_porta, unit_id=smartlogger05_ID2, auto_open=True, auto_close=True)
        
        leiturasmartlogger05 = smartlogger05.read_holding_registers(40550, 28)
        leitura_inv51 = smartlogger51.read_holding_registers(32015, 80)
        leitura_inv52 = smartlogger52.read_holding_registers(32015, 80)
        #print(leitura_inv51)
        
        def correnteDC():

            energydaily05 = np.multiply(leiturasmartlogger05[13], 0.1)
            correnteDC05 = np.multiply(leiturasmartlogger05[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger05[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger05[25:29:1], 0.1)

            correnteDC_inv51 = np.multiply(leitura_inv51[2:38:2], 0.05)
            correnteDC_inv52 = np.multiply(leitura_inv52[2:38:2], 0.05)
            
            
            tensaoDC_inv51 = np.multiply(leitura_inv51[1:37:2], 0.1)
            tensaoDC_inv52 = np.multiply(leitura_inv52[1:37:2], 0.1)
            

            tempinterna_inv51 = np.multiply(leitura_inv51[72], 0.1)
            tempinterna_inv52 = np.multiply(leitura_inv52[72], 0.1)

            tensoaAC_inv51 = np.multiply(leitura_inv51[51:54:1], 0.1)
            tensoaAC_inv52 = np.multiply(leitura_inv52[51:54:1], 0.1)

            correnteAC_inv51 = np.multiply(leitura_inv51[58:64:2], 0.001)
            correnteAC_inv52 = np.multiply(leitura_inv52[58:64:2], 0.001)

            potativaAC_inv51 = np.multiply(leitura_inv51[66], 0.1)
            potativaAC_inv52 = np.multiply(leitura_inv52[66], 0.1)

            potenciaDC_inv51 = np.multiply(leitura_inv51[50], 0.1)
            potenciaDC_inv52 = np.multiply(leitura_inv52[50], 0.1)
            

        correnteDC()

    def smartlogger_06():
        smartlogger06_endereco = '192.168.163.15'
        smartlogger06_porta= 502
        smartlogger06_ID = 101
        smartlogger06_ID1 = 11
        smartlogger06_ID2 = 12
        
        smartlogger06 = ModbusClient(host=smartlogger06_endereco, port=smartlogger06_porta, unit_id=smartlogger06_ID, auto_open=True, auto_close=True)
        smartlogger61 = ModbusClient(host=smartlogger06_endereco, port=smartlogger06_porta, unit_id=smartlogger06_ID1, auto_open=True, auto_close=True)
        smartlogger62 = ModbusClient(host=smartlogger06_endereco, port=smartlogger06_porta, unit_id=smartlogger06_ID2, auto_open=True, auto_close=True)
        
        leiturasmartlogger06 = smartlogger06.read_holding_registers(40550, 28)
        leitura_inv61 = smartlogger61.read_holding_registers(32015, 80)
        leitura_inv62 = smartlogger62.read_holding_registers(32015, 80)
        #print(leitura_inv61)
        
        def correnteDC():

            energydaily06 = np.multiply(leiturasmartlogger06[13], 0.1)
            correnteDC06 = np.multiply(leiturasmartlogger06[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger06[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger06[25:29:1], 0.1)

            correnteDC_inv61 = np.multiply(leitura_inv61[2:38:2], 0.06)
            correnteDC_inv62 = np.multiply(leitura_inv62[2:38:2], 0.06)
            
            
            tensaoDC_inv61 = np.multiply(leitura_inv61[1:37:2], 0.1)
            tensaoDC_inv62 = np.multiply(leitura_inv62[1:37:2], 0.1)
            

            tempinterna_inv61 = np.multiply(leitura_inv61[72], 0.1)
            tempinterna_inv62 = np.multiply(leitura_inv62[72], 0.1)

            tensoaAC_inv61 = np.multiply(leitura_inv61[51:54:1], 0.1)
            tensoaAC_inv62 = np.multiply(leitura_inv62[51:54:1], 0.1)

            correnteAC_inv61 = np.multiply(leitura_inv61[58:64:2], 0.001)
            correnteAC_inv62 = np.multiply(leitura_inv62[58:64:2], 0.001)

            potativaAC_inv61 = np.multiply(leitura_inv61[66], 0.1)
            potativaAC_inv62 = np.multiply(leitura_inv62[66], 0.1)

            potenciaDC_inv61 = np.multiply(leitura_inv61[50], 0.1)
            potenciaDC_inv62 = np.multiply(leitura_inv62[50], 0.1)
            

        correnteDC()

    def smartlogger_07():
        smartlogger07_endereco = '192.168.163.16'
        smartlogger07_porta= 502
        smartlogger07_ID = 101
        smartlogger07_ID1 = 11
        smartlogger07_ID2 = 12
        
        smartlogger07 = ModbusClient(host=smartlogger07_endereco, port=smartlogger07_porta, unit_id=smartlogger07_ID, auto_open=True, auto_close=True)
        smartlogger71 = ModbusClient(host=smartlogger07_endereco, port=smartlogger07_porta, unit_id=smartlogger07_ID1, auto_open=True, auto_close=True)
        smartlogger72 = ModbusClient(host=smartlogger07_endereco, port=smartlogger07_porta, unit_id=smartlogger07_ID2, auto_open=True, auto_close=True)
        
        leiturasmartlogger07 = smartlogger07.read_holding_registers(40550, 28)
        leitura_inv71 = smartlogger71.read_holding_registers(32015, 80)
        leitura_inv72 = smartlogger72.read_holding_registers(32015, 80)
        #print(leitura_inv71)
        
        def correnteDC():

            energydaily07 = np.multiply(leiturasmartlogger07[13], 0.1)
            correnteDC07 = np.multiply(leiturasmartlogger07[5], 0.1)
            correnteDC_ABC = np.multiply(leiturasmartlogger07[22:25:1], 1)
            tensaoDC_ABC = np.multiply(leiturasmartlogger07[25:29:1], 0.1)

            correnteDC_inv71 = np.multiply(leitura_inv71[2:38:2], 0.07)
            correnteDC_inv72 = np.multiply(leitura_inv72[2:38:2], 0.07)
            
            
            tensaoDC_inv71 = np.multiply(leitura_inv71[1:37:2], 0.1)
            tensaoDC_inv72 = np.multiply(leitura_inv72[1:37:2], 0.1)
            

            tempinterna_inv71 = np.multiply(leitura_inv71[72], 0.1)
            tempinterna_inv72 = np.multiply(leitura_inv72[72], 0.1)

            tensoaAC_inv71 = np.multiply(leitura_inv71[51:54:1], 0.1)
            tensoaAC_inv72 = np.multiply(leitura_inv72[51:54:1], 0.1)

            correnteAC_inv71 = np.multiply(leitura_inv71[58:64:2], 0.001)
            correnteAC_inv72 = np.multiply(leitura_inv72[58:64:2], 0.001)

            potativaAC_inv71 = np.multiply(leitura_inv71[66], 0.1)
            potativaAC_inv72 = np.multiply(leitura_inv72[66], 0.1)

            potenciaDC_inv71 = np.multiply(leitura_inv71[50], 0.1)
            potenciaDC_inv72 = np.multiply(leitura_inv72[50], 0.1)
            

        correnteDC()

    smartlogger_U01 = smartlogger_01()
    smartlogger_U02 = smartlogger_02()
    smartlogger_U03 = smartlogger_03()
    smartlogger_U04 = smartlogger_04()
    smartlogger_U05 = smartlogger_05()
    smartlogger_U06 = smartlogger_06()
    smartlogger_U07 = smartlogger_07()


def main():
    estmet = estacao_solarimetrica()
    smartlogger = smartloggers()





if __name__ == "__main__":
    main()
