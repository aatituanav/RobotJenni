from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def iniciarSesionTrivo(browser, email, password, projectName):
    try:
        projectNameField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/form/div/div/input')) #This is a dummy element
        )
        projectNameField.send_keys(projectName)
        projectNameField.send_keys(Keys.ENTER)
    except Exception as e:
        print(e)
        browser.quit()

    try:
        #espero a que se cargue el campo de texto del correo
        emailField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[1]/div/input')) #This is a dummy element
        )
        emailField.send_keys(email)
        #encuentro el campo de texto para contrasenia
        passwordField = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/input')
        passwordField.send_keys(password)
        time.sleep(1)
        passwordField.send_keys(Keys.ENTER)
    except Exception as e: 
        print(e)
        browser.quit()


def orderListByDate(browser):
    try:
        #espero a que se cargue el campo de texto del correo
        lastDayContactHeader = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/table/thead/tr/th[12]')) 
        )
        lastDayContactHeader.click()
        lastDayContactHeader = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/table/thead/tr/th[12]'))
        )
        lastDayContactHeader.click()
    except Exception as e: 
        print(e)
        browser.quit()



def sendInfoWhatsApp(browser, phone, messages):
    phone = '+593993055278'
    try:
        #cambio a la nueva ventana que se abrio automaticamente
        browser.switch_to.window(browser.window_handles[1])
        ##verifico que sea un numero de celular con +593 para quitarle
        if phone.find('+') != -1:
            browser.get('https://web.whatsapp.com/send?l=es&phone=%s&text=' %(phone.lstrip('+'))) 

            #espero a que la caja de texto del whatsapp se muestre para poder ingresar 
            messageBoxText = WebDriverWait(browser, 40).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'))
            )
            #cuando se inicia, se cargan todos los elementos, pero aparece un popup de cargando mensajes...tengo que esperar a que se quite
            WebDriverWait(browser, 30).until(
                EC.invisibility_of_element_located((By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div'))
            )
            for msg in messages:
                messageBoxText.send_keys(msg)
                messageBoxText.send_keys(Keys.ENTER)
                time.sleep(2)
            print('cambio a la ventana anterior')
            browser.switch_to.window(browser.window_handles[0])

        else:
            print('SE ENCONTRO UN NUMERO DE TELEFONO INVALIDO, PROGRAMAR LA LOGICA PRRO')
            browser.quit()
        
    except Exception as e: 
        print(e)
        browser.quit()

def entertoCustomer(browser):
    name = ''
    phoneNumber = ''
    messages = ['','Buenos días XXXX le saluda Katherine Quintana, Asesora Inmobiliaria de trivo.','Le escribo porque queremos saber si aún tiene interés en adquirir bienes inmueble.']
    linkWhatsaPo = ''

    def findCustomertoEdit(browser):
        #Los nuevos usuarios aparecen con el campo "FECHA ULTIMO CONTACTO" vacio, por lo cual no hay que hacer seguimiento de dichos usuarios
        #Por lo tanto al ordenar por fecha, estos usuarios aparecen primero, por lo cual es necesario saber en que fila estan los usuarios no nuevos 
        #de esta manera si hay 4 usuarios nuevos, habria que hacer seguimiento al 5 usuario (siempre y cuando la tabla este ordenada por fecha)
        #este metodo regresara el xpath del componente que el robot tendra que hacer click
        numberofRows = 20
        ##la informacion se muestra desde la posicion 1, (0 es para la cabecera)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[1]/td[12]'))
        )

        for i in range(1, numberofRows + 1):
            selectField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[%s]/td[12]' % (i))
            if selectField.text != '-':
                return ('//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[%s]/td[2]' % (i))

        print('TODAS LOS CLIENTES QUE SE MUESTRAN EN LA TABLA SON NUEVOS')
        return ''

    

    try:
        #hago click en el cliente que mas tiempo le tengo olvidado
        xpath = findCustomertoEdit(browser)
        editButton = browser.find_element(By.XPATH, xpath)
        editButton.click()
        
        #espero a que cargue el boton de "SIGUIENTES ACCIONES" para pasar al siguiente cuestionario
        siguientesAccionesButton = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[2]/div/button'))
        )
        #obtengo el nombre del cliente
        nameField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div[1]/h4')
        name = nameField.text

        
        #obtengo el numero de celular del cliente
        phoneField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div[2]/a/h6')
        phoneNumber = phoneField.text.strip()

        #avanzo a la siguiente paguina
        siguientesAccionesButton.click()
        
        #espero que termine de cargar la paguina (que desaparezca el loadbutton)
        WebDriverWait(browser, 10).until(
            EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/*[name()="svg"]'))
        )

        ##lleno los datos del cuestinoario y continuo con la siguiente paguina
        #muestro las opciones
        selectField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/div/div/div/div')
        selectField.click()

       #selecciono la opcion de seguimiento
        selectFieldSecondOption = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]'))
        )
        selectFieldSecondOption.click()
        
        #copio el mensaje que se enviara al whatsapo
        messageField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/div[2]/div[2]/div'))
        )  
        #guardo el mensaje
        messages[0] = messageField.text.replace('XXXX', name)
        #en el segundo mensaje del array, el nombre esta con XXXX
        messages[1] = messages[1].replace('XXXX', name.split()[0])


        #click en el boton para continuar (Esto abre whatsapp en una nueva ventana)
        continueButton = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[10]/div/button')
        continueButton.click()
        
        #confirmar que deseo continuar
        confirmButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[2]'))
        )  
        confirmButton.click()

        #envio info por whatsapp
        sendInfoWhatsApp(browser, phoneNumber, messages)

        #regreso a donde inicie (A la tabla de clientes)
        goBackFirst = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/button')
        goBackFirst.click()
        goBackTable = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[1]/button')
        goBackTable.click()

    except Exception as e: 
        print(e)
        browser.quit()

    