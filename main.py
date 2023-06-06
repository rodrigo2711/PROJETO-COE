from pyModbusTCP.client import ModbusClient
import numpy as np
import time
from datetime import datetime
import pyodbc

###################################################################
                    #CONEXÃO BANCO DE DADOS

dados_conexao =(
    "Driver={SQL Server};"
    "Server=DESKTOP-9CIHE8J\SQLEXPRESS;"
    "Database=UFVCEI;"
)

conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

##############################################################
            #Estação Solarimétrica

server_em = '192.168.163.8'
porta_em = 502
ID_em = 2

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
GHI = valor_em[0]
IPOA = valor_em[1]
ALB = valor_em[2]
TEMP_MOD = valor_em[3]
TEMP_AMB = valor_em[4]
print(f'PIRANÔMETRO GHI = {valor_em[0]:.2f} (W/m²)')
print(f'PIRANÔMETRO IPOA = {valor_em[1]:.2f} (W/m²)')
print(f'ALBEDÔMETRO= {valor_em[2]:.2f} (W/m²)')
print(f'TEMP. MÓDULO = {valor_em[3]:.2f} (ºC)')
print(f'TEMP. AMBIENTE = {valor_em[4]:.2f} (ºC)')

comando_em = f"""INSERT INTO EM(GHI,IPOA,ALB,TEMP_MOD,TEMP_AMB, DIA, HORA)
VALUES({GHI},{IPOA},{ALB},{TEMP_MOD},{TEMP_AMB}, GETDATE(), CURRENT_TIMESTAMP)"""

################################################################################
                     #MÓDULOS USINA 01 SMARTLOGGER 01

server_u01_inv11 = '192.168.163.10'
porta_u01_inv11 = 502
ID_u01_inv11 = 11
c_u01_inv11 = ModbusClient(host=server_u01_inv11, port=porta_u01_inv11, unit_id=ID_u01_inv11, auto_open=True, auto_close=True)

ler_u01_inv11 = c_u01_inv11.read_holding_registers(32017, 36)
valor_u01_inv11 = np.multiply(ler_u01_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u01_inv11)

U01_INV01_I_PV1 = valor_u01_inv11[0]
U01_INV01_I_PV2 = valor_u01_inv11[2]
U01_INV01_I_PV3 = valor_u01_inv11[4]
U01_INV01_I_PV4 = valor_u01_inv11[6]
U01_INV01_I_PV5 = valor_u01_inv11[8]
U01_INV01_I_PV6 = valor_u01_inv11[10]
U01_INV01_I_PV7 = valor_u01_inv11[12]
U01_INV01_I_PV8 = valor_u01_inv11[14]
U01_INV01_I_PV9 = valor_u01_inv11[16]
U01_INV01_I_PV10 = valor_u01_inv11[18]
U01_INV01_I_PV11 = valor_u01_inv11[20]
U01_INV01_I_PV12 = valor_u01_inv11[22]
U01_INV01_I_PV13 = valor_u01_inv11[24]
U01_INV01_I_PV14 = valor_u01_inv11[26]
U01_INV01_I_PV15 = valor_u01_inv11[28]
U01_INV01_I_PV16 = valor_u01_inv11[30]
U01_INV01_I_PV17 = valor_u01_inv11[32]
U01_INV01_I_PV18 = valor_u01_inv11[34]

#############################################################

            #MÓDULOS USINA 01 SMARTLOGGER 02

server_u01_inv12 = '192.168.163.10'
porta_u01_inv12 = 502
ID_u01_inv12 = 12
c_u01_inv12 = ModbusClient(host=server_u01_inv12, port=porta_u01_inv12, unit_id=ID_u01_inv12, auto_open=True, auto_close=True)

ler_u01_inv12 = c_u01_inv12.read_holding_registers(32017, 36)
valor_u01_inv12 = np.multiply(ler_u01_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u01_inv12)

U01_INV02_I_PV1 = valor_u01_inv12[0]
U01_INV02_I_PV2 = valor_u01_inv12[2]
U01_INV02_I_PV3 = valor_u01_inv12[4]
U01_INV02_I_PV4 = valor_u01_inv12[6]
U01_INV02_I_PV5 = valor_u01_inv12[8]
U01_INV02_I_PV6 = valor_u01_inv12[10]
U01_INV02_I_PV7 = valor_u01_inv12[12]
U01_INV02_I_PV8 = valor_u01_inv12[14]
U01_INV02_I_PV9 = valor_u01_inv12[16]
U01_INV02_I_PV10 = valor_u01_inv12[18]
U01_INV02_I_PV11 = valor_u01_inv12[20]
U01_INV02_I_PV12 = valor_u01_inv12[22]
U01_INV02_I_PV13 = valor_u01_inv12[24]
U01_INV02_I_PV14 = valor_u01_inv12[26]
U01_INV02_I_PV15 = valor_u01_inv12[28]
U01_INV02_I_PV16 = valor_u01_inv12[30]
U01_INV02_I_PV17 = valor_u01_inv12[32]
U01_INV02_I_PV18 = valor_u01_inv12[34]


# ############################################################
#
# MÓDULOS USINA 01 SMARTLOGGER 03

server_u01_inv13 = '192.168.163.10'
porta_u01_inv13 = 502
ID_u01_inv13 = 13
c_u01_inv13 = ModbusClient(host=server_u01_inv13, port=porta_u01_inv13, unit_id=ID_u01_inv13, auto_open=True, auto_close=True)

ler_u01_inv13 = c_u01_inv13.read_holding_registers(32017, 36)
valor_u01_inv13 = np.multiply(ler_u01_inv13, 0.01)
print("\n SMARTLOGGER 03 \n")

U01_INV03_I_PV1 = valor_u01_inv13[0]
U01_INV03_I_PV2 = valor_u01_inv13[2]
U01_INV03_I_PV3 = valor_u01_inv13[4]
U01_INV03_I_PV4 = valor_u01_inv13[6]
U01_INV03_I_PV5 = valor_u01_inv13[8]
U01_INV03_I_PV6 = valor_u01_inv13[10]
U01_INV03_I_PV7 = valor_u01_inv13[12]
U01_INV03_I_PV8 = valor_u01_inv13[14]
U01_INV03_I_PV9 = valor_u01_inv13[16]
U01_INV03_I_PV10 = valor_u01_inv13[18]
U01_INV03_I_PV11 = valor_u01_inv13[20]
U01_INV03_I_PV12 = valor_u01_inv13[22]
U01_INV03_I_PV13 = valor_u01_inv13[24]
U01_INV03_I_PV14 = valor_u01_inv13[26]
U01_INV03_I_PV15 = valor_u01_inv13[28]
U01_INV03_I_PV16 = valor_u01_inv13[30]
U01_INV03_I_PV17 = valor_u01_inv13[32]
U01_INV03_I_PV18 = valor_u01_inv13[34]


comando_u01 = f"""INSERT INTO U01(DIA, HORA, U01_INV01_I_PV1,
U01_INV01_I_PV2,
U01_INV01_I_PV3,
U01_INV01_I_PV4,
U01_INV01_I_PV5,
U01_INV01_I_PV6,
U01_INV01_I_PV7,
U01_INV01_I_PV8,
U01_INV01_I_PV9,
U01_INV01_I_PV10,
U01_INV01_I_PV11,
U01_INV01_I_PV12,
U01_INV01_I_PV13,
U01_INV01_I_PV14,
U01_INV01_I_PV15,
U01_INV01_I_PV16,
U01_INV01_I_PV17,
U01_INV01_I_PV18,
U01_INV02_I_PV1,
U01_INV02_I_PV2,
U01_INV02_I_PV3,
U01_INV02_I_PV4,
U01_INV02_I_PV5,
U01_INV02_I_PV6,
U01_INV02_I_PV7,
U01_INV02_I_PV8,
U01_INV02_I_PV9,
U01_INV02_I_PV10,
U01_INV02_I_PV11,
U01_INV02_I_PV12,
U01_INV02_I_PV13,
U01_INV02_I_PV14,
U01_INV02_I_PV15,
U01_INV02_I_PV16,
U01_INV02_I_PV17,
U01_INV02_I_PV18,
U01_INV03_I_PV1,
U01_INV03_I_PV2,
U01_INV03_I_PV3,
U01_INV03_I_PV4,
U01_INV03_I_PV5,
U01_INV03_I_PV6,
U01_INV03_I_PV7,
U01_INV03_I_PV8,
U01_INV03_I_PV9,
U01_INV03_I_PV10,
U01_INV03_I_PV11,
U01_INV03_I_PV12,
U01_INV03_I_PV13,
U01_INV03_I_PV14,
U01_INV03_I_PV15,
U01_INV03_I_PV16,
U01_INV03_I_PV17,
U01_INV03_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U01_INV01_I_PV1},
{U01_INV01_I_PV2},
{U01_INV01_I_PV3},
{U01_INV01_I_PV4},
{U01_INV01_I_PV5},
{U01_INV01_I_PV6},
{U01_INV01_I_PV7},
{U01_INV01_I_PV8},
{U01_INV01_I_PV9},
{U01_INV01_I_PV10},
{U01_INV01_I_PV11},
{U01_INV01_I_PV12},
{U01_INV01_I_PV13},
{U01_INV01_I_PV14},
{U01_INV01_I_PV15},
{U01_INV01_I_PV16},
{U01_INV01_I_PV17},
{U01_INV01_I_PV18},
{U01_INV02_I_PV1},
{U01_INV02_I_PV2},
{U01_INV02_I_PV3},
{U01_INV02_I_PV4},
{U01_INV02_I_PV5},
{U01_INV02_I_PV6},
{U01_INV02_I_PV7},
{U01_INV02_I_PV8},
{U01_INV02_I_PV9},
{U01_INV02_I_PV10},
{U01_INV02_I_PV11},
{U01_INV02_I_PV12},
{U01_INV02_I_PV13},
{U01_INV02_I_PV14},
{U01_INV02_I_PV15},
{U01_INV02_I_PV16},
{U01_INV02_I_PV17},
{U01_INV02_I_PV18},
{U01_INV03_I_PV1},
{U01_INV03_I_PV2},
{U01_INV03_I_PV3},
{U01_INV03_I_PV4},
{U01_INV03_I_PV5},
{U01_INV03_I_PV6},
{U01_INV03_I_PV7},
{U01_INV03_I_PV8},
{U01_INV03_I_PV9},
{U01_INV03_I_PV10},
{U01_INV03_I_PV11},
{U01_INV03_I_PV12},
{U01_INV03_I_PV13},
{U01_INV03_I_PV14},
{U01_INV03_I_PV15},
{U01_INV03_I_PV16},
{U01_INV03_I_PV17},
{U01_INV03_I_PV18})"""

#
# ############################################################################

        #MÓDULOS USINA 02 SMARTLOGGER 01

server_u02_inv11 = '192.168.163.11'
porta_u02_inv11 = 502
ID_u02_inv11 = 11
c_u02_inv11 = ModbusClient(host=server_u02_inv11, port=porta_u02_inv11, unit_id=ID_u02_inv11, auto_open=True, auto_close=True)

ler_u02_inv11 = c_u02_inv11.read_holding_registers(32017, 36)
valor_u02_inv11 = np.multiply(ler_u02_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u02_inv11)

U02_INV01_I_PV1 = valor_u02_inv11[0]
U02_INV01_I_PV2 = valor_u02_inv11[2]
U02_INV01_I_PV3 = valor_u02_inv11[4]
U02_INV01_I_PV4 = valor_u02_inv11[6]
U02_INV01_I_PV5 = valor_u02_inv11[8]
U02_INV01_I_PV6 = valor_u02_inv11[10]
U02_INV01_I_PV7 = valor_u02_inv11[12]
U02_INV01_I_PV8 = valor_u02_inv11[14]
U02_INV01_I_PV9 = valor_u02_inv11[16]
U02_INV01_I_PV10 = valor_u02_inv11[18]
U02_INV01_I_PV11 = valor_u02_inv11[20]
U02_INV01_I_PV12 = valor_u02_inv11[22]
U02_INV01_I_PV13 = valor_u02_inv11[24]
U02_INV01_I_PV14 = valor_u02_inv11[26]
U02_INV01_I_PV15 = valor_u02_inv11[28]
U02_INV01_I_PV16 = valor_u02_inv11[30]
U02_INV01_I_PV17 = valor_u02_inv11[32]
U02_INV01_I_PV18 = valor_u02_inv11[34]



#############################################################

                #MÓDULOS USINA 02 SMARTLOGGER 02

server_u02_inv12 = '192.168.163.11'
porta_u02_inv12 = 502
ID_u02_inv12 = 12
c_u02_inv12 = ModbusClient(host=server_u02_inv12, port=porta_u02_inv12, unit_id=ID_u02_inv12, auto_open=True, auto_close=True)

ler_u02_inv12 = c_u02_inv12.read_holding_registers(32017, 36)
valor_u02_inv12 = np.multiply(ler_u02_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u02_inv12)

U02_INV02_I_PV1 = valor_u02_inv12[0]
U02_INV02_I_PV2 = valor_u02_inv12[2]
U02_INV02_I_PV3 = valor_u02_inv12[4]
U02_INV02_I_PV4 = valor_u02_inv12[6]
U02_INV02_I_PV5 = valor_u02_inv12[8]
U02_INV02_I_PV6 = valor_u02_inv12[10]
U02_INV02_I_PV7 = valor_u02_inv12[12]
U02_INV02_I_PV8 = valor_u02_inv12[14]
U02_INV02_I_PV9 = valor_u02_inv12[16]
U02_INV02_I_PV10 = valor_u02_inv12[18]
U02_INV02_I_PV11 = valor_u02_inv12[20]
U02_INV02_I_PV12 = valor_u02_inv12[22]
U02_INV02_I_PV13 = valor_u02_inv12[24]
U02_INV02_I_PV14 = valor_u02_inv12[26]
U02_INV02_I_PV15 = valor_u02_inv12[28]
U02_INV02_I_PV16 = valor_u02_inv12[30]
U02_INV02_I_PV17 = valor_u02_inv12[32]
U02_INV02_I_PV18 = valor_u02_inv12[34]



# #############################################################

            #MÓDULOS USINA 02 SMARTLOGGER 03

server_u02_inv13 = '192.168.163.11'
porta_u02_inv13 = 502
ID_u02_inv13 = 13
c_u02_inv13 = ModbusClient(host=server_u02_inv13, port=porta_u02_inv13, unit_id=ID_u02_inv13, auto_open=True, auto_close=True)

ler_u02_inv13 = c_u02_inv13.read_holding_registers(32017, 36)
valor_u02_inv13 = np.multiply(ler_u02_inv13, 0.01)
print("\n SMARTLOGGER 03 \n")

U02_INV03_I_PV1 = valor_u02_inv13[0]
U02_INV03_I_PV2 = valor_u02_inv13[2]
U02_INV03_I_PV3 = valor_u02_inv13[4]
U02_INV03_I_PV4 = valor_u02_inv13[6]
U02_INV03_I_PV5 = valor_u02_inv13[8]
U02_INV03_I_PV6 = valor_u02_inv13[10]
U02_INV03_I_PV7 = valor_u02_inv13[12]
U02_INV03_I_PV8 = valor_u02_inv13[14]
U02_INV03_I_PV9 = valor_u02_inv13[16]
U02_INV03_I_PV10 = valor_u02_inv13[18]
U02_INV03_I_PV11 = valor_u02_inv13[20]
U02_INV03_I_PV12 = valor_u02_inv13[22]
U02_INV03_I_PV13 = valor_u02_inv13[24]
U02_INV03_I_PV14 = valor_u02_inv13[26]
U02_INV03_I_PV15 = valor_u02_inv13[28]
U02_INV03_I_PV16 = valor_u02_inv13[30]
U02_INV03_I_PV17 = valor_u02_inv13[32]
U02_INV03_I_PV18 = valor_u02_inv13[34]

comando_u02 = f"""INSERT INTO U02(DIA, HORA, U02_INV01_I_PV1,
U02_INV01_I_PV2,
U02_INV01_I_PV3,
U02_INV01_I_PV4,
U02_INV01_I_PV5,
U02_INV01_I_PV6,
U02_INV01_I_PV7,
U02_INV01_I_PV8,
U02_INV01_I_PV9,
U02_INV01_I_PV10,
U02_INV01_I_PV11,
U02_INV01_I_PV12,
U02_INV01_I_PV13,
U02_INV01_I_PV14,
U02_INV01_I_PV15,
U02_INV01_I_PV16,
U02_INV01_I_PV17,
U02_INV01_I_PV18,
U02_INV02_I_PV1,
U02_INV02_I_PV2,
U02_INV02_I_PV3,
U02_INV02_I_PV4,
U02_INV02_I_PV5,
U02_INV02_I_PV6,
U02_INV02_I_PV7,
U02_INV02_I_PV8,
U02_INV02_I_PV9,
U02_INV02_I_PV10,
U02_INV02_I_PV11,
U02_INV02_I_PV12,
U02_INV02_I_PV13,
U02_INV02_I_PV14,
U02_INV02_I_PV15,
U02_INV02_I_PV16,
U02_INV02_I_PV17,
U02_INV02_I_PV18,
U02_INV03_I_PV1,
U02_INV03_I_PV2,
U02_INV03_I_PV3,
U02_INV03_I_PV4,
U02_INV03_I_PV5,
U02_INV03_I_PV6,
U02_INV03_I_PV7,
U02_INV03_I_PV8,
U02_INV03_I_PV9,
U02_INV03_I_PV10,
U02_INV03_I_PV11,
U02_INV03_I_PV12,
U02_INV03_I_PV13,
U02_INV03_I_PV14,
U02_INV03_I_PV15,
U02_INV03_I_PV16,
U02_INV03_I_PV17,
U02_INV03_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U02_INV01_I_PV1},
{U02_INV01_I_PV2},
{U02_INV01_I_PV3},
{U02_INV01_I_PV4},
{U02_INV01_I_PV5},
{U02_INV01_I_PV6},
{U02_INV01_I_PV7},
{U02_INV01_I_PV8},
{U02_INV01_I_PV9},
{U02_INV01_I_PV10},
{U02_INV01_I_PV11},
{U02_INV01_I_PV12},
{U02_INV01_I_PV13},
{U02_INV01_I_PV14},
{U02_INV01_I_PV15},
{U02_INV01_I_PV16},
{U02_INV01_I_PV17},
{U02_INV01_I_PV18},
{U02_INV02_I_PV1},
{U02_INV02_I_PV2},
{U02_INV02_I_PV3},
{U02_INV02_I_PV4},
{U02_INV02_I_PV5},
{U02_INV02_I_PV6},
{U02_INV02_I_PV7},
{U02_INV02_I_PV8},
{U02_INV02_I_PV9},
{U02_INV02_I_PV10},
{U02_INV02_I_PV11},
{U02_INV02_I_PV12},
{U02_INV02_I_PV13},
{U02_INV02_I_PV14},
{U02_INV02_I_PV15},
{U02_INV02_I_PV16},
{U02_INV02_I_PV17},
{U02_INV02_I_PV18},
{U02_INV03_I_PV1},
{U02_INV03_I_PV2},
{U02_INV03_I_PV3},
{U02_INV03_I_PV4},
{U02_INV03_I_PV5},
{U02_INV03_I_PV6},
{U02_INV03_I_PV7},
{U02_INV03_I_PV8},
{U02_INV03_I_PV9},
{U02_INV03_I_PV10},
{U02_INV03_I_PV11},
{U02_INV03_I_PV12},
{U02_INV03_I_PV13},
{U02_INV03_I_PV14},
{U02_INV03_I_PV15},
{U02_INV03_I_PV16},
{U02_INV03_I_PV17},
{U02_INV03_I_PV18})"""

# ################################################################################

#MÓDULOS USINA 03 SMARTLOGGER 01
server_u03_inv11 = '192.168.163.12'
porta_u03_inv11 = 502
ID_u03_inv11 = 11
c_u03_inv11 = ModbusClient(host=server_u03_inv11, port=porta_u03_inv11, unit_id=ID_u03_inv11, auto_open=True, auto_close=True)

ler_u03_inv11 = c_u03_inv11.read_holding_registers(32017, 36)
valor_u03_inv11 = np.multiply(ler_u03_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u03_inv11)

U03_INV01_I_PV1 = valor_u03_inv11[0]
U03_INV01_I_PV2 = valor_u03_inv11[2]
U03_INV01_I_PV3 = valor_u03_inv11[4]
U03_INV01_I_PV4 = valor_u03_inv11[6]
U03_INV01_I_PV5 = valor_u03_inv11[8]
U03_INV01_I_PV6 = valor_u03_inv11[10]
U03_INV01_I_PV7 = valor_u03_inv11[12]
U03_INV01_I_PV8 = valor_u03_inv11[14]
U03_INV01_I_PV9 = valor_u03_inv11[16]
U03_INV01_I_PV10 = valor_u03_inv11[18]
U03_INV01_I_PV11 = valor_u03_inv11[20]
U03_INV01_I_PV12 = valor_u03_inv11[22]
U03_INV01_I_PV13 = valor_u03_inv11[24]
U03_INV01_I_PV14 = valor_u03_inv11[26]
U03_INV01_I_PV15 = valor_u03_inv11[28]
U03_INV01_I_PV16 = valor_u03_inv11[30]
U03_INV01_I_PV17 = valor_u03_inv11[32]
U03_INV01_I_PV18 = valor_u03_inv11[34]



#############################################################

#MÓDULOS USINA 03 SMARTLOGGER 02

server_u03_inv12 = '192.168.163.12'
porta_u03_inv12 = 502
ID_u03_inv12 = 12
c_u03_inv12 = ModbusClient(host=server_u03_inv12, port=porta_u03_inv12, unit_id=ID_u03_inv12, auto_open=True, auto_close=True)

ler_u03_inv12 = c_u03_inv12.read_holding_registers(32017, 36)
valor_u03_inv12 = np.multiply(ler_u03_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u03_inv12)

U03_INV02_I_PV1 = valor_u03_inv12[0]
U03_INV02_I_PV2 = valor_u03_inv12[2]
U03_INV02_I_PV3 = valor_u03_inv12[4]
U03_INV02_I_PV4 = valor_u03_inv12[6]
U03_INV02_I_PV5 = valor_u03_inv12[8]
U03_INV02_I_PV6 = valor_u03_inv12[10]
U03_INV02_I_PV7 = valor_u03_inv12[12]
U03_INV02_I_PV8 = valor_u03_inv12[14]
U03_INV02_I_PV9 = valor_u03_inv12[16]
U03_INV02_I_PV10 = valor_u03_inv12[18]
U03_INV02_I_PV11 = valor_u03_inv12[20]
U03_INV02_I_PV12 = valor_u03_inv12[22]
U03_INV02_I_PV13 = valor_u03_inv12[24]
U03_INV02_I_PV14 = valor_u03_inv12[26]
U03_INV02_I_PV15 = valor_u03_inv12[28]
U03_INV02_I_PV16 = valor_u03_inv12[30]
U03_INV02_I_PV17 = valor_u03_inv12[32]
U03_INV02_I_PV18 = valor_u03_inv12[34]


#############################################################

#MÓDULOS USINA 03 SMARTLOGGER 03

server_u03_inv13 = '192.168.163.12'
porta_u03_inv13 = 502
ID_u03_inv13 = 13
c_u03_inv13 = ModbusClient(host=server_u03_inv13, port=porta_u03_inv13, unit_id=ID_u03_inv13, auto_open=True, auto_close=True)

ler_u03_inv13 = c_u03_inv13.read_holding_registers(32017, 36)
valor_u03_inv13 = np.multiply(ler_u03_inv13, 0.01)
print("\n SMARTLOGGER 03 \n")

U03_INV03_I_PV1 = valor_u03_inv13[0]
U03_INV03_I_PV2 = valor_u03_inv13[2]
U03_INV03_I_PV3 = valor_u03_inv13[4]
U03_INV03_I_PV4 = valor_u03_inv13[6]
U03_INV03_I_PV5 = valor_u03_inv13[8]
U03_INV03_I_PV6 = valor_u03_inv13[10]
U03_INV03_I_PV7 = valor_u03_inv13[12]
U03_INV03_I_PV8 = valor_u03_inv13[14]
U03_INV03_I_PV9 = valor_u03_inv13[16]
U03_INV03_I_PV10 = valor_u03_inv13[18]
U03_INV03_I_PV11 = valor_u03_inv13[20]
U03_INV03_I_PV12 = valor_u03_inv13[22]
U03_INV03_I_PV13 = valor_u03_inv13[24]
U03_INV03_I_PV14 = valor_u03_inv13[26]
U03_INV03_I_PV15 = valor_u03_inv13[28]
U03_INV03_I_PV16 = valor_u03_inv13[30]
U03_INV03_I_PV17 = valor_u03_inv13[32]
U03_INV03_I_PV18 = valor_u03_inv13[34]

comando_u03 = f"""INSERT INTO U03(DIA, HORA, U03_INV01_I_PV1,
U03_INV01_I_PV2,
U03_INV01_I_PV3,
U03_INV01_I_PV4,
U03_INV01_I_PV5,
U03_INV01_I_PV6,
U03_INV01_I_PV7,
U03_INV01_I_PV8,
U03_INV01_I_PV9,
U03_INV01_I_PV10,
U03_INV01_I_PV11,
U03_INV01_I_PV12,
U03_INV01_I_PV13,
U03_INV01_I_PV14,
U03_INV01_I_PV15,
U03_INV01_I_PV16,
U03_INV01_I_PV17,
U03_INV01_I_PV18,
U03_INV02_I_PV1,
U03_INV02_I_PV2,
U03_INV02_I_PV3,
U03_INV02_I_PV4,
U03_INV02_I_PV5,
U03_INV02_I_PV6,
U03_INV02_I_PV7,
U03_INV02_I_PV8,
U03_INV02_I_PV9,
U03_INV02_I_PV10,
U03_INV02_I_PV11,
U03_INV02_I_PV12,
U03_INV02_I_PV13,
U03_INV02_I_PV14,
U03_INV02_I_PV15,
U03_INV02_I_PV16,
U03_INV02_I_PV17,
U03_INV02_I_PV18,
U03_INV03_I_PV1,
U03_INV03_I_PV2,
U03_INV03_I_PV3,
U03_INV03_I_PV4,
U03_INV03_I_PV5,
U03_INV03_I_PV6,
U03_INV03_I_PV7,
U03_INV03_I_PV8,
U03_INV03_I_PV9,
U03_INV03_I_PV10,
U03_INV03_I_PV11,
U03_INV03_I_PV12,
U03_INV03_I_PV13,
U03_INV03_I_PV14,
U03_INV03_I_PV15,
U03_INV03_I_PV16,
U03_INV03_I_PV17,
U03_INV03_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U03_INV01_I_PV1},
{U03_INV01_I_PV2},
{U03_INV01_I_PV3},
{U03_INV01_I_PV4},
{U03_INV01_I_PV5},
{U03_INV01_I_PV6},
{U03_INV01_I_PV7},
{U03_INV01_I_PV8},
{U03_INV01_I_PV9},
{U03_INV01_I_PV10},
{U03_INV01_I_PV11},
{U03_INV01_I_PV12},
{U03_INV01_I_PV13},
{U03_INV01_I_PV14},
{U03_INV01_I_PV15},
{U03_INV01_I_PV16},
{U03_INV01_I_PV17},
{U03_INV01_I_PV18},
{U03_INV02_I_PV1},
{U03_INV02_I_PV2},
{U03_INV02_I_PV3},
{U03_INV02_I_PV4},
{U03_INV02_I_PV5},
{U03_INV02_I_PV6},
{U03_INV02_I_PV7},
{U03_INV02_I_PV8},
{U03_INV02_I_PV9},
{U03_INV02_I_PV10},
{U03_INV02_I_PV11},
{U03_INV02_I_PV12},
{U03_INV02_I_PV13},
{U03_INV02_I_PV14},
{U03_INV02_I_PV15},
{U03_INV02_I_PV16},
{U03_INV02_I_PV17},
{U03_INV02_I_PV18},
{U03_INV03_I_PV1},
{U03_INV03_I_PV2},
{U03_INV03_I_PV3},
{U03_INV03_I_PV4},
{U03_INV03_I_PV5},
{U03_INV03_I_PV6},
{U03_INV03_I_PV7},
{U03_INV03_I_PV8},
{U03_INV03_I_PV9},
{U03_INV03_I_PV10},
{U03_INV03_I_PV11},
{U03_INV03_I_PV12},
{U03_INV03_I_PV13},
{U03_INV03_I_PV14},
{U03_INV03_I_PV15},
{U03_INV03_I_PV16},
{U03_INV03_I_PV17},
{U03_INV03_I_PV18})"""


################################################################################

                    #MÓDULOS USINA 04 SMARTLOGGER 01

server_u04_inv11 = '192.168.163.13'
porta_u04_inv11 = 502
ID_u04_inv11 = 11
c_u04_inv11 = ModbusClient(host=server_u04_inv11, port=porta_u04_inv11, unit_id=ID_u04_inv11, auto_open=True, auto_close=True)

ler_u04_inv11 = c_u04_inv11.read_holding_registers(32017, 36)
valor_u04_inv11 = np.multiply(ler_u04_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u04_inv11)

U04_INV01_I_PV1 = valor_u04_inv11[0]
U04_INV01_I_PV2 = valor_u04_inv11[2]
U04_INV01_I_PV3 = valor_u04_inv11[4]
U04_INV01_I_PV4 = valor_u04_inv11[6]
U04_INV01_I_PV5 = valor_u04_inv11[8]
U04_INV01_I_PV6 = valor_u04_inv11[10]
U04_INV01_I_PV7 = valor_u04_inv11[12]
U04_INV01_I_PV8 = valor_u04_inv11[14]
U04_INV01_I_PV9 = valor_u04_inv11[16]
U04_INV01_I_PV10 = valor_u04_inv11[18]
U04_INV01_I_PV11 = valor_u04_inv11[20]
U04_INV01_I_PV12 = valor_u04_inv11[22]
U04_INV01_I_PV13 = valor_u04_inv11[24]
U04_INV01_I_PV14 = valor_u04_inv11[26]
U04_INV01_I_PV15 = valor_u04_inv11[28]
U04_INV01_I_PV16 = valor_u04_inv11[30]
U04_INV01_I_PV17 = valor_u04_inv11[32]
U04_INV01_I_PV18 = valor_u04_inv11[34]

#############################################################

                #MÓDULOS USINA 04 SMARTLOGGER 02

server_u04_inv12 = '192.168.163.13'
porta_u04_inv12 = 502
ID_u04_inv12 = 12
c_u04_inv12 = ModbusClient(host=server_u04_inv12, port=porta_u04_inv12, unit_id=ID_u04_inv12, auto_open=True, auto_close=True)

ler_u04_inv12 = c_u04_inv12.read_holding_registers(32017, 36)
valor_u04_inv12 = np.multiply(ler_u04_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u04_inv12)

U04_INV02_I_PV1 = valor_u04_inv12[0]
U04_INV02_I_PV2 = valor_u04_inv12[2]
U04_INV02_I_PV3 = valor_u04_inv12[4]
U04_INV02_I_PV4 = valor_u04_inv12[6]
U04_INV02_I_PV5 = valor_u04_inv12[8]
U04_INV02_I_PV6 = valor_u04_inv12[10]
U04_INV02_I_PV7 = valor_u04_inv12[12]
U04_INV02_I_PV8 = valor_u04_inv12[14]
U04_INV02_I_PV9 = valor_u04_inv12[16]
U04_INV02_I_PV10 = valor_u04_inv12[18]
U04_INV02_I_PV11 = valor_u04_inv12[20]
U04_INV02_I_PV12 = valor_u04_inv12[22]
U04_INV02_I_PV13 = valor_u04_inv12[24]
U04_INV02_I_PV14 = valor_u04_inv12[26]
U04_INV02_I_PV15 = valor_u04_inv12[28]
U04_INV02_I_PV16 = valor_u04_inv12[30]
U04_INV02_I_PV17 = valor_u04_inv12[32]
U04_INV02_I_PV18 = valor_u04_inv12[34]


#############################################################

#MÓDULOS USINA 04 SMARTLOGGER 03

server_u04_inv13 = '192.168.163.13'
porta_u04_inv13 = 502
ID_u04_inv13 = 13
c_u04_inv13 = ModbusClient(host=server_u04_inv13, port=porta_u04_inv13, unit_id=ID_u04_inv13, auto_open=True, auto_close=True)

ler_u04_inv13 = c_u04_inv13.read_holding_registers(32017, 36)
valor_u04_inv13 = np.multiply(ler_u04_inv13, 0.01)
print("\n SMARTLOGGER 03 \n")

U04_INV03_I_PV1 = valor_u04_inv13[0]
U04_INV03_I_PV2 = valor_u04_inv13[2]
U04_INV03_I_PV3 = valor_u04_inv13[4]
U04_INV03_I_PV4 = valor_u04_inv13[6]
U04_INV03_I_PV5 = valor_u04_inv13[8]
U04_INV03_I_PV6 = valor_u04_inv13[10]
U04_INV03_I_PV7 = valor_u04_inv13[12]
U04_INV03_I_PV8 = valor_u04_inv13[14]
U04_INV03_I_PV9 = valor_u04_inv13[16]
U04_INV03_I_PV10 = valor_u04_inv13[18]
U04_INV03_I_PV11 = valor_u04_inv13[20]
U04_INV03_I_PV12 = valor_u04_inv13[22]
U04_INV03_I_PV13 = valor_u04_inv13[24]
U04_INV03_I_PV14 = valor_u04_inv13[26]
U04_INV03_I_PV15 = valor_u04_inv13[28]
U04_INV03_I_PV16 = valor_u04_inv13[30]
U04_INV03_I_PV17 = valor_u04_inv13[32]
U04_INV03_I_PV18 = valor_u04_inv13[34]

comando_u04 = f"""INSERT INTO U04(DIA, HORA, U04_INV01_I_PV1,
U04_INV01_I_PV2,
U04_INV01_I_PV3,
U04_INV01_I_PV4,
U04_INV01_I_PV5,
U04_INV01_I_PV6,
U04_INV01_I_PV7,
U04_INV01_I_PV8,
U04_INV01_I_PV9,
U04_INV01_I_PV10,
U04_INV01_I_PV11,
U04_INV01_I_PV12,
U04_INV01_I_PV13,
U04_INV01_I_PV14,
U04_INV01_I_PV15,
U04_INV01_I_PV16,
U04_INV01_I_PV17,
U04_INV01_I_PV18,
U04_INV02_I_PV1,
U04_INV02_I_PV2,
U04_INV02_I_PV3,
U04_INV02_I_PV4,
U04_INV02_I_PV5,
U04_INV02_I_PV6,
U04_INV02_I_PV7,
U04_INV02_I_PV8,
U04_INV02_I_PV9,
U04_INV02_I_PV10,
U04_INV02_I_PV11,
U04_INV02_I_PV12,
U04_INV02_I_PV13,
U04_INV02_I_PV14,
U04_INV02_I_PV15,
U04_INV02_I_PV16,
U04_INV02_I_PV17,
U04_INV02_I_PV18,
U04_INV03_I_PV1,
U04_INV03_I_PV2,
U04_INV03_I_PV3,
U04_INV03_I_PV4,
U04_INV03_I_PV5,
U04_INV03_I_PV6,
U04_INV03_I_PV7,
U04_INV03_I_PV8,
U04_INV03_I_PV9,
U04_INV03_I_PV10,
U04_INV03_I_PV11,
U04_INV03_I_PV12,
U04_INV03_I_PV13,
U04_INV03_I_PV14,
U04_INV03_I_PV15,
U04_INV03_I_PV16,
U04_INV03_I_PV17,
U04_INV03_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U04_INV01_I_PV1},
{U04_INV01_I_PV2},
{U04_INV01_I_PV3},
{U04_INV01_I_PV4},
{U04_INV01_I_PV5},
{U04_INV01_I_PV6},
{U04_INV01_I_PV7},
{U04_INV01_I_PV8},
{U04_INV01_I_PV9},
{U04_INV01_I_PV10},
{U04_INV01_I_PV11},
{U04_INV01_I_PV12},
{U04_INV01_I_PV13},
{U04_INV01_I_PV14},
{U04_INV01_I_PV15},
{U04_INV01_I_PV16},
{U04_INV01_I_PV17},
{U04_INV01_I_PV18},
{U04_INV02_I_PV1},
{U04_INV02_I_PV2},
{U04_INV02_I_PV3},
{U04_INV02_I_PV4},
{U04_INV02_I_PV5},
{U04_INV02_I_PV6},
{U04_INV02_I_PV7},
{U04_INV02_I_PV8},
{U04_INV02_I_PV9},
{U04_INV02_I_PV10},
{U04_INV02_I_PV11},
{U04_INV02_I_PV12},
{U04_INV02_I_PV13},
{U04_INV02_I_PV14},
{U04_INV02_I_PV15},
{U04_INV02_I_PV16},
{U04_INV02_I_PV17},
{U04_INV02_I_PV18},
{U04_INV03_I_PV1},
{U04_INV03_I_PV2},
{U04_INV03_I_PV3},
{U04_INV03_I_PV4},
{U04_INV03_I_PV5},
{U04_INV03_I_PV6},
{U04_INV03_I_PV7},
{U04_INV03_I_PV8},
{U04_INV03_I_PV9},
{U04_INV03_I_PV10},
{U04_INV03_I_PV11},
{U04_INV03_I_PV12},
{U04_INV03_I_PV13},
{U04_INV03_I_PV14},
{U04_INV03_I_PV15},
{U04_INV03_I_PV16},
{U04_INV03_I_PV17},
{U04_INV03_I_PV18})"""


# ############################################################################

################################################################################

                            #MÓDULOS USINA 05 SMARTLOGGER 01

server_u05_inv11 = '192.168.163.14'
porta_u05_inv11 = 502
ID_u05_inv11 = 11
c_u05_inv11 = ModbusClient(host=server_u05_inv11, port=porta_u05_inv11, unit_id=ID_u05_inv11, auto_open=True, auto_close=True)

ler_u05_inv11 = c_u05_inv11.read_holding_registers(32017, 36)
valor_u05_inv11 = np.multiply(ler_u05_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u05_inv11)

U05_INV01_I_PV1 = valor_u05_inv11[0]
U05_INV01_I_PV2 = valor_u05_inv11[2]
U05_INV01_I_PV3 = valor_u05_inv11[4]
U05_INV01_I_PV4 = valor_u05_inv11[6]
U05_INV01_I_PV5 = valor_u05_inv11[8]
U05_INV01_I_PV6 = valor_u05_inv11[10]
U05_INV01_I_PV7 = valor_u05_inv11[12]
U05_INV01_I_PV8 = valor_u05_inv11[14]
U05_INV01_I_PV9 = valor_u05_inv11[16]
U05_INV01_I_PV10 = valor_u05_inv11[18]
U05_INV01_I_PV11 = valor_u05_inv11[20]
U05_INV01_I_PV12 = valor_u05_inv11[22]
U05_INV01_I_PV13 = valor_u05_inv11[24]
U05_INV01_I_PV14 = valor_u05_inv11[26]
U05_INV01_I_PV15 = valor_u05_inv11[28]
U05_INV01_I_PV16 = valor_u05_inv11[30]
U05_INV01_I_PV17 = valor_u05_inv11[32]
U05_INV01_I_PV18 = valor_u05_inv11[34]


#############################################################

                        #MÓDULOS USINA 05 SMARTLOGGER 02

server_u05_inv12 = '192.168.163.14'
porta_u05_inv12 = 502
ID_u05_inv12 = 12
c_u05_inv12 = ModbusClient(host=server_u05_inv12, port=porta_u05_inv12, unit_id=ID_u05_inv12, auto_open=True, auto_close=True)

ler_u05_inv12 = c_u05_inv12.read_holding_registers(32017, 36)
valor_u05_inv12 = np.multiply(ler_u05_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u05_inv12)

U05_INV02_I_PV1 = valor_u05_inv12[0]
U05_INV02_I_PV2 = valor_u05_inv12[2]
U05_INV02_I_PV3 = valor_u05_inv12[4]
U05_INV02_I_PV4 = valor_u05_inv12[6]
U05_INV02_I_PV5 = valor_u05_inv12[8]
U05_INV02_I_PV6 = valor_u05_inv12[10]
U05_INV02_I_PV7 = valor_u05_inv12[12]
U05_INV02_I_PV8 = valor_u05_inv12[14]
U05_INV02_I_PV9 = valor_u05_inv12[16]
U05_INV02_I_PV10 = valor_u05_inv12[18]
U05_INV02_I_PV11 = valor_u05_inv12[20]
U05_INV02_I_PV12 = valor_u05_inv12[22]
U05_INV02_I_PV13 = valor_u05_inv12[24]
U05_INV02_I_PV14 = valor_u05_inv12[26]
U05_INV02_I_PV15 = valor_u05_inv12[28]
U05_INV02_I_PV16 = valor_u05_inv12[30]
U05_INV02_I_PV17 = valor_u05_inv12[32]
U05_INV02_I_PV18 = valor_u05_inv12[34]


comando_u05 = f"""INSERT INTO U05(DIA, HORA, U05_INV01_I_PV1,
U05_INV01_I_PV2,
U05_INV01_I_PV3,
U05_INV01_I_PV4,
U05_INV01_I_PV5,
U05_INV01_I_PV6,
U05_INV01_I_PV7,
U05_INV01_I_PV8,
U05_INV01_I_PV9,
U05_INV01_I_PV10,
U05_INV01_I_PV11,
U05_INV01_I_PV12,
U05_INV01_I_PV13,
U05_INV01_I_PV14,
U05_INV01_I_PV15,
U05_INV01_I_PV16,
U05_INV01_I_PV17,
U05_INV01_I_PV18,
U05_INV02_I_PV1,
U05_INV02_I_PV2,
U05_INV02_I_PV3,
U05_INV02_I_PV4,
U05_INV02_I_PV5,
U05_INV02_I_PV6,
U05_INV02_I_PV7,
U05_INV02_I_PV8,
U05_INV02_I_PV9,
U05_INV02_I_PV10,
U05_INV02_I_PV11,
U05_INV02_I_PV12,
U05_INV02_I_PV13,
U05_INV02_I_PV14,
U05_INV02_I_PV15,
U05_INV02_I_PV16,
U05_INV02_I_PV17,
U05_INV02_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U05_INV01_I_PV1},
{U05_INV01_I_PV2},
{U05_INV01_I_PV3},
{U05_INV01_I_PV4},
{U05_INV01_I_PV5},
{U05_INV01_I_PV6},
{U05_INV01_I_PV7},
{U05_INV01_I_PV8},
{U05_INV01_I_PV9},
{U05_INV01_I_PV10},
{U05_INV01_I_PV11},
{U05_INV01_I_PV12},
{U05_INV01_I_PV13},
{U05_INV01_I_PV14},
{U05_INV01_I_PV15},
{U05_INV01_I_PV16},
{U05_INV01_I_PV17},
{U05_INV01_I_PV18},
{U05_INV02_I_PV1},
{U05_INV02_I_PV2},
{U05_INV02_I_PV3},
{U05_INV02_I_PV4},
{U05_INV02_I_PV5},
{U05_INV02_I_PV6},
{U05_INV02_I_PV7},
{U05_INV02_I_PV8},
{U05_INV02_I_PV9},
{U05_INV02_I_PV10},
{U05_INV02_I_PV11},
{U05_INV02_I_PV12},
{U05_INV02_I_PV13},
{U05_INV02_I_PV14},
{U05_INV02_I_PV15},
{U05_INV02_I_PV16},
{U05_INV02_I_PV17},
{U05_INV02_I_PV18})"""

#################################################################################

                    #MÓDULOS USINA 06 SMARTLOGGER 01

server_u06_inv11 = '192.168.163.15'
porta_u06_inv11 = 502
ID_u06_inv11 = 11
c_u06_inv11 = ModbusClient(host=server_u06_inv11, port=porta_u06_inv11, unit_id=ID_u06_inv11, auto_open=True, auto_close=True)

ler_u06_inv11 = c_u06_inv11.read_holding_registers(32017, 36)
valor_u06_inv11 = np.multiply(ler_u06_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u06_inv11)

U06_INV01_I_PV1 = valor_u06_inv11[0]
U06_INV01_I_PV2 = valor_u06_inv11[2]
U06_INV01_I_PV3 = valor_u06_inv11[4]
U06_INV01_I_PV4 = valor_u06_inv11[6]
U06_INV01_I_PV5 = valor_u06_inv11[8]
U06_INV01_I_PV6 = valor_u06_inv11[10]
U06_INV01_I_PV7 = valor_u06_inv11[12]
U06_INV01_I_PV8 = valor_u06_inv11[14]
U06_INV01_I_PV9 = valor_u06_inv11[16]
U06_INV01_I_PV10 = valor_u06_inv11[18]
U06_INV01_I_PV11 = valor_u06_inv11[20]
U06_INV01_I_PV12 = valor_u06_inv11[22]
U06_INV01_I_PV13 = valor_u06_inv11[24]
U06_INV01_I_PV14 = valor_u06_inv11[26]
U06_INV01_I_PV15 = valor_u06_inv11[28]
U06_INV01_I_PV16 = valor_u06_inv11[30]
U06_INV01_I_PV17 = valor_u06_inv11[32]
U06_INV01_I_PV18 = valor_u06_inv11[34]


#############################################################

                    #MÓDULOS USINA 06 SMARTLOGGER 02

server_u06_inv12 = '192.168.163.15'
porta_u06_inv12 = 502
ID_u06_inv12 = 12
c_u06_inv12 = ModbusClient(host=server_u06_inv12, port=porta_u06_inv12, unit_id=ID_u06_inv12, auto_open=True, auto_close=True)

ler_u06_inv12 = c_u06_inv12.read_holding_registers(32017, 36)
valor_u06_inv12 = np.multiply(ler_u06_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u06_inv12)

U06_INV02_I_PV1 = valor_u06_inv12[0]
U06_INV02_I_PV2 = valor_u06_inv12[2]
U06_INV02_I_PV3 = valor_u06_inv12[4]
U06_INV02_I_PV4 = valor_u06_inv12[6]
U06_INV02_I_PV5 = valor_u06_inv12[8]
U06_INV02_I_PV6 = valor_u06_inv12[10]
U06_INV02_I_PV7 = valor_u06_inv12[12]
U06_INV02_I_PV8 = valor_u06_inv12[14]
U06_INV02_I_PV9 = valor_u06_inv12[16]
U06_INV02_I_PV10 = valor_u06_inv12[18]
U06_INV02_I_PV11 = valor_u06_inv12[20]
U06_INV02_I_PV12 = valor_u06_inv12[22]
U06_INV02_I_PV13 = valor_u06_inv12[24]
U06_INV02_I_PV14 = valor_u06_inv12[26]
U06_INV02_I_PV15 = valor_u06_inv12[28]
U06_INV02_I_PV16 = valor_u06_inv12[30]
U06_INV02_I_PV17 = valor_u06_inv12[32]
U06_INV02_I_PV18 = valor_u06_inv12[34]

comando_u06 = f"""INSERT INTO U06(DIA, HORA, U06_INV01_I_PV1,
U06_INV01_I_PV2,
U06_INV01_I_PV3,
U06_INV01_I_PV4,
U06_INV01_I_PV5,
U06_INV01_I_PV6,
U06_INV01_I_PV7,
U06_INV01_I_PV8,
U06_INV01_I_PV9,
U06_INV01_I_PV10,
U06_INV01_I_PV11,
U06_INV01_I_PV12,
U06_INV01_I_PV13,
U06_INV01_I_PV14,
U06_INV01_I_PV15,
U06_INV01_I_PV16,
U06_INV01_I_PV17,
U06_INV01_I_PV18,
U06_INV02_I_PV1,
U06_INV02_I_PV2,
U06_INV02_I_PV3,
U06_INV02_I_PV4,
U06_INV02_I_PV5,
U06_INV02_I_PV6,
U06_INV02_I_PV7,
U06_INV02_I_PV8,
U06_INV02_I_PV9,
U06_INV02_I_PV10,
U06_INV02_I_PV11,
U06_INV02_I_PV12,
U06_INV02_I_PV13,
U06_INV02_I_PV14,
U06_INV02_I_PV15,
U06_INV02_I_PV16,
U06_INV02_I_PV17,
U06_INV02_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U06_INV01_I_PV1},
{U06_INV01_I_PV2},
{U06_INV01_I_PV3},
{U06_INV01_I_PV4},
{U06_INV01_I_PV5},
{U06_INV01_I_PV6},
{U06_INV01_I_PV7},
{U06_INV01_I_PV8},
{U06_INV01_I_PV9},
{U06_INV01_I_PV10},
{U06_INV01_I_PV11},
{U06_INV01_I_PV12},
{U06_INV01_I_PV13},
{U06_INV01_I_PV14},
{U06_INV01_I_PV15},
{U06_INV01_I_PV16},
{U06_INV01_I_PV17},
{U06_INV01_I_PV18},
{U06_INV02_I_PV1},
{U06_INV02_I_PV2},
{U06_INV02_I_PV3},
{U06_INV02_I_PV4},
{U06_INV02_I_PV5},
{U06_INV02_I_PV6},
{U06_INV02_I_PV7},
{U06_INV02_I_PV8},
{U06_INV02_I_PV9},
{U06_INV02_I_PV10},
{U06_INV02_I_PV11},
{U06_INV02_I_PV12},
{U06_INV02_I_PV13},
{U06_INV02_I_PV14},
{U06_INV02_I_PV15},
{U06_INV02_I_PV16},
{U06_INV02_I_PV17},
{U06_INV02_I_PV18})"""

#################################################################################

                #MÓDULOS USINA 07 SMARTLOGGER 01

server_u07_inv11 = '192.168.163.16'
porta_u07_inv11 = 502
ID_u07_inv11 = 11
c_u07_inv11 = ModbusClient(host=server_u07_inv11, port=porta_u07_inv11, unit_id=ID_u07_inv11, auto_open=True, auto_close=True)

ler_u07_inv11 = c_u07_inv11.read_holding_registers(32017, 36)
valor_u07_inv11 = np.multiply(ler_u07_inv11, 0.01)

print("\n SMARTLOGGER 01 \n")
print(valor_u07_inv11)

U07_INV01_I_PV1 = valor_u07_inv11[0]
U07_INV01_I_PV2 = valor_u07_inv11[2]
U07_INV01_I_PV3 = valor_u07_inv11[4]
U07_INV01_I_PV4 = valor_u07_inv11[6]
U07_INV01_I_PV5 = valor_u07_inv11[8]
U07_INV01_I_PV6 = valor_u07_inv11[10]
U07_INV01_I_PV7 = valor_u07_inv11[12]
U07_INV01_I_PV8 = valor_u07_inv11[14]
U07_INV01_I_PV9 = valor_u07_inv11[16]
U07_INV01_I_PV10 = valor_u07_inv11[18]
U07_INV01_I_PV11 = valor_u07_inv11[20]
U07_INV01_I_PV12 = valor_u07_inv11[22]
U07_INV01_I_PV13 = valor_u07_inv11[24]
U07_INV01_I_PV14 = valor_u07_inv11[26]
U07_INV01_I_PV15 = valor_u07_inv11[28]
U07_INV01_I_PV16 = valor_u07_inv11[30]
U07_INV01_I_PV17 = valor_u07_inv11[32]
U07_INV01_I_PV18 = valor_u07_inv11[34]

#############################################################

                #MÓDULOS USINA 07 SMARTLOGGER 02

server_u07_inv12 = '192.168.163.16'
porta_u07_inv12 = 502
ID_u07_inv12 = 12
c_u07_inv12 = ModbusClient(host=server_u07_inv12, port=porta_u07_inv12, unit_id=ID_u07_inv12, auto_open=True, auto_close=True)

ler_u07_inv12 = c_u07_inv12.read_holding_registers(32017, 36)
valor_u07_inv12 = np.multiply(ler_u07_inv12, 0.01)
print("\n SMARTLOGGER 02 \n")
print(valor_u07_inv12)

U07_INV02_I_PV1 = valor_u07_inv12[0]
U07_INV02_I_PV2 = valor_u07_inv12[2]
U07_INV02_I_PV3 = valor_u07_inv12[4]
U07_INV02_I_PV4 = valor_u07_inv12[6]
U07_INV02_I_PV5 = valor_u07_inv12[8]
U07_INV02_I_PV6 = valor_u07_inv12[10]
U07_INV02_I_PV7 = valor_u07_inv12[12]
U07_INV02_I_PV8 = valor_u07_inv12[14]
U07_INV02_I_PV9 = valor_u07_inv12[16]
U07_INV02_I_PV10 = valor_u07_inv12[18]
U07_INV02_I_PV11 = valor_u07_inv12[20]
U07_INV02_I_PV12 = valor_u07_inv12[22]
U07_INV02_I_PV13 = valor_u07_inv12[24]
U07_INV02_I_PV14 = valor_u07_inv12[26]
U07_INV02_I_PV15 = valor_u07_inv12[28]
U07_INV02_I_PV16 = valor_u07_inv12[30]
U07_INV02_I_PV17 = valor_u07_inv12[32]
U07_INV02_I_PV18 = valor_u07_inv12[34]

comando_u07 = f"""INSERT INTO U07(DIA, HORA, U07_INV01_I_PV1,
U07_INV01_I_PV2,
U07_INV01_I_PV3,
U07_INV01_I_PV4,
U07_INV01_I_PV5,
U07_INV01_I_PV6,
U07_INV01_I_PV7,
U07_INV01_I_PV8,
U07_INV01_I_PV9,
U07_INV01_I_PV10,
U07_INV01_I_PV11,
U07_INV01_I_PV12,
U07_INV01_I_PV13,
U07_INV01_I_PV14,
U07_INV01_I_PV15,
U07_INV01_I_PV16,
U07_INV01_I_PV17,
U07_INV01_I_PV18,
U07_INV02_I_PV1,
U07_INV02_I_PV2,
U07_INV02_I_PV3,
U07_INV02_I_PV4,
U07_INV02_I_PV5,
U07_INV02_I_PV6,
U07_INV02_I_PV7,
U07_INV02_I_PV8,
U07_INV02_I_PV9,
U07_INV02_I_PV10,
U07_INV02_I_PV11,
U07_INV02_I_PV12,
U07_INV02_I_PV13,
U07_INV02_I_PV14,
U07_INV02_I_PV15,
U07_INV02_I_PV16,
U07_INV02_I_PV17,
U07_INV02_I_PV18)
VALUES(GETDATE(), CURRENT_TIMESTAMP, {U07_INV01_I_PV1},
{U07_INV01_I_PV2},
{U07_INV01_I_PV3},
{U07_INV01_I_PV4},
{U07_INV01_I_PV5},
{U07_INV01_I_PV6},
{U07_INV01_I_PV7},
{U07_INV01_I_PV8},
{U07_INV01_I_PV9},
{U07_INV01_I_PV10},
{U07_INV01_I_PV11},
{U07_INV01_I_PV12},
{U07_INV01_I_PV13},
{U07_INV01_I_PV14},
{U07_INV01_I_PV15},
{U07_INV01_I_PV16},
{U07_INV01_I_PV17},
{U07_INV01_I_PV18},
{U07_INV02_I_PV1},
{U07_INV02_I_PV2},
{U07_INV02_I_PV3},
{U07_INV02_I_PV4},
{U07_INV02_I_PV5},
{U07_INV02_I_PV6},
{U07_INV02_I_PV7},
{U07_INV02_I_PV8},
{U07_INV02_I_PV9},
{U07_INV02_I_PV10},
{U07_INV02_I_PV11},
{U07_INV02_I_PV12},
{U07_INV02_I_PV13},
{U07_INV02_I_PV14},
{U07_INV02_I_PV15},
{U07_INV02_I_PV16},
{U07_INV02_I_PV17},
{U07_INV02_I_PV18})"""

#############################################################################

cursor.execute(comando_em)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u01)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u02)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u03)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u04)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u05)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u06)
cursor.commit() #NECESSÁRIO PARA UPDATE
cursor.execute(comando_u07)
cursor.commit() #NECESSÁRIO PARA UPDATE





