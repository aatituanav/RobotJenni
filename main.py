from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import operations.operations as operations




#datos de acceso a la plataforma
email = "katherineq@trivo.com.ec"
password = "h4x9kska"
projectName = "lucia"

#configuracion de opciones para evitar que el navegador se cierre una vez ejecutadas las instrucciones
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


#instanciamiento del webdriver
browser = webdriver.Chrome(chrome_options=chrome_options)
#abrir la paguina
browser.get('https://admin.trivo.com.ec/login')


operations.iniciarSesionTrivo(browser, email, password, projectName)

operations.orderListByDate(browser)