from selenium import webdriver
import operations.operations as operations
from dotenv import load_dotenv
import os 
import time
import customFunctions.customFunctions as cf

#cargo las variables de entorno
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
projectName = os.getenv("PROJECTNAME")
userdata =  os.getenv("USERDATA")

#configuracion de opciones para evitar que el navegador se cierre una vez ejecutadas las instrucciones
options = webdriver.ChromeOptions() 
options.add_argument('--user-data-dir=%s' % (userdata))
options.add_experimental_option("detach", True)

#instanciamiento del webdriver
browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

#abrir la paguina
browser.get('https://admin.trivo.com.ec/login')

#browser.get('https://web.whatsapp.com/send?l=es&phone=593994938897&text=Hola%20XXXX%2C%20%C2%A1Queremos%20saber%20de%20ti!%20Hace%20unos%20d%C3%ADas%20compartimos%20contigo%20las%20opciones%20de%20las%20unidades%20habitacionales%20del%20Conjunto%20Residencial%20Luc%C3%ADa%20que%20m%C3%A1s%20se%20ajustan%20a%20lo%20que%20buscas.%20Si%20tienes%20alguna%20duda%20o%20ya%20te%20decidiste%20por%20tus%20favoritas%2C%20ponte%20en%20contacto%20conmigo%20para%20agendar%20tu%20visita.')
#messages = ['Este es un mensaje predetermindao']

#operations.sendInfoWhatsApp(browser, '+593993055278', messages, dirImages)

##NO HACE FALTA INICIAR SESION SI INICIO CON EL PERFIL GUARDADO AL ABRIR EL NAVEGADOR
#operations.iniciarSesionTrivo(browser, email, password, projectName)

operations.orderListByDate(browser)

operations.followCustomers(browser)