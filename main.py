from selenium import webdriver
from dotenv import load_dotenv
import os 
import time
import src.customFunctions.customFunctions as cf
import sys
import src.luciaRobot.luciaMain as robotLucia
import src.trivoRobot.trivoMain as robotTrivo

#cargo las variables de entorno
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
projectName = os.getenv("PROJECTNAME")
userdata =  '%s\\AppData\\Local\\Google\\Chrome\\User Data' %(os.path.expanduser("~"))

#configuracion de opciones para evitar que el navegador se cierre una vez ejecutadas las instrucciones
options = webdriver.ChromeOptions() 
options.add_argument('--user-data-dir=%s' % (userdata))
options.add_experimental_option("detach", True)

application_path = os.path.dirname(sys.executable)
#instanciamiento del webdriver

browser = webdriver.Chrome(executable_path= '%s\\chromedriver.exe' %(application_path), options=options)

##INICIO EL ROBOT DE LUCIA
robotLucia.startLuciaRobot(browser)
#robotTrivo.startTrivoRobot(browser)