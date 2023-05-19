import pyodbc

dados_conexao =(
    "Driver={SQL Server};"
    "Server=DESKTOP-9CIHE8J\SQLEXPRESS;"
    "Database=UFVCEI;"
)

conexao = pyodbc.connect(dados_conexao)
print("OK")

cursor = conexao.cursor()

GHI = 10
IPOA = 15
ALB = 12
TEMPMOD = 16
TEMPAMB = 13
comando = f"""INSERT INTO EM(GHI,IPOA,ALB,tempmod,tempamb)
VALUES({GHI},{IPOA},{ALB},{TEMPMOD},{TEMPAMB})"""

cursor.execute(comando)
cursor.commit() #NECESSÁRIO PARA UPDATE


