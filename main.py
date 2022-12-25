from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service

import os 
import time
import src.customFunctions.customFunctions as cf
import sys
import src.luciaRobot.luciaMain as robotLucia
import src.trivoRobot.trivoMain as robotTrivo
import src.promonsaRobot.promonsaMain as robotPromonsa

#cargo las variables de entorno
load_dotenv()
userdata =  '%s\\AppData\\Local\\Google\\Chrome\\User Data' %(os.path.expanduser("~"))

#configuracion de opciones para evitar que el navegador se cierre una vez ejecutadas las instrucciones
options = webdriver.ChromeOptions() 
options.add_argument('--user-data-dir=%s' % (userdata))
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)

application_path = os.path.dirname(sys.executable)
driver_service = Service(executable_path= '%s\\chromedriver.exe' %(application_path))


print('HOLA CHENNI, CUAL ROBOT QUIERES INICIAR?\nOpcion 1: Robot Lucia\nOpcion 2: Robot Trivo\nOpcion 3: Robot Promonsa')
print('Recuerda tener iniciada la sesion antes de iniciar')
option = input()
print('Listo... Tu tranquila, yo nervioso')

#instanciamiento del webdriver

browser = webdriver.Chrome(service = driver_service, options=options)
if option == '1':
    robotLucia.startLuciaRobot(browser)
elif option == '2':
    robotTrivo.startTrivoRobot(browser)
elif option == '3':
    robotPromonsa.startPromonsaRobot(browser)
else:
    print('Opcion no válida, Mejor me la saco...')
    print('*C va')
