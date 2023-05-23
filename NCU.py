import numpy
from pyModbusTCP.client import ModbusClient
import numpy as np


############################################

server_ncu01 = '192.168.163.17'
porta_ncu01 = 502
ID_ncu01 = 1
c_ncu01 = ModbusClient(host=server_ncu01, port=porta_ncu01, unit_id=ID_ncu01, auto_open = True, auto_close = True)

ler_ncu01 = c_ncu01.read_holding_registers(30150, 10)


PV = ler_ncu01[1]
PV = np.divide(PV, 1000)
PR = (ler_ncu01[2])
PR = np.degrees(PR)
MC = ler_ncu01[4]
MC = np.divide(MC, 1000)
CPK = ler_ncu01[5]
CPK = np.divide(CPK, 1000)
CP = ler_ncu01[8]
CP = np.divide(CP, 1000)

print(f' PAINEL VOLTAGE = {PV}')
print(f' POSITION RAD = {PR}')
print(f' CORRENTE MOTOR = {MC}')
print(f' CORRENTE MOTOR PICO = {CPK}')
print(f' TARGET ANGLE = {ler_ncu01[6]}')
print(f' CORRENTE PAINEL = {CP}')





print(ler_ncu01)
