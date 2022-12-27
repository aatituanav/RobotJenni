from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from dotenv import load_dotenv
from datetime import datetime
from getpass import getpass

import src.promonsaRobot.promonsaMain as robotPromonsa
import src.customFunctions.customFunctions as cf
import src.trivoRobot.trivoMain as robotTrivo
import src.luciaRobot.luciaMain as robotLucia
import time
import sys
import os 


#cargo las variables de entorno
load_dotenv(dotenv_path=cf.resource_path('.env'))

userdata =  '%s\\AppData\\Local\\Google\\Chrome\\User Data' %(os.path.expanduser("~"))

#configuracion de opciones para evitar que el navegador se cierre una vez ejecutadas las instrucciones
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=%s' % (userdata))
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)

application_path = os.path.dirname(sys.executable)
driver_service = Service(executable_path= cf.resource_path('chromedriver.exe'))

if datetime.now() <= datetime.strptime('2023-01-26', "%Y-%m-%d"):
    while True:
        print('CONTRASEÑA:')
        password = getpass()
        if password == os.getenv("PASSWORD"):
            break
    print('JELOU, A CUAL PROYECTO DESEAS HACER SEGUIMIENTO?\nOpcion 1: Lucia\nOpcion 2: Trivo\nOpcion 3: Promonsa')
    option = input()

    browser = webdriver.Chrome(service = driver_service, options=options)
    if option == '1':
        robotLucia.startLuciaRobot(browser)
    elif option == '2':
        robotTrivo.startTrivoRobot(browser)
    elif option == '3':
        robotPromonsa.startPromonsaRobot(browser)
    else:
        print('*C va')
else:
    print('El periodo de prueba ha terminado.')
    
