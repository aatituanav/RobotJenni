from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import operations.operations as operations
from dotenv import load_dotenv
import os 

#cargo las variables de entorno
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
projectName = os.getenv("PROJECTNAME")

#configuracion de opciones para evitar que el navegador se cierre una vez ejecutadas las instrucciones
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


#instanciamiento del webdriver
browser = webdriver.Chrome(chrome_options=chrome_options)
#abrir la paguina
browser.get('https://admin.trivo.com.ec/login')


operations.iniciarSesionTrivo(browser, email, password, projectName)

operations.orderListByDate(browser)