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

def main():
    estmet = estacao_solarimetrica()


if __name__ == "__main__":
    main()
