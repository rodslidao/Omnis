from src.logs.log import logSetup
from time import sleep
logger = logSetup("Teste")
from src.utility.node_tester.node import retorno
sleep(5)
print(retorno)