from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import customFunctions.customFunctions as CF
from operations.Observation import Observation
import os 
import pyautogui
import time
import sys


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



def sendInfoWhatsApp(browser, phone, messages, dirImages):
    ##este metodo solo funciona para enviar 3 fotos que se encuentren en dirImages
    ##dirImages: direccion de la carpeta raiz de las imagenes
    ##messages: lista que contiene todos los mensajes que se enviaran
    ##phone: numero de telefono al cual enviar la informacion
    ##browser: la instancia del navegador en el cual esta trabajando el robot
    
    #phone = '+593993055278'
    try:
        #cambio a la nueva ventana que se abrio automaticamente
        browser.switch_to.window(browser.window_handles[1])        
    
        phoneformatted = CF.formatPhoneNumber(phone)
        ##verifico que sea un numero de celular con +593 para quitarle
        if phoneformatted != None:
            browser.get('https://web.whatsapp.com/send?l=es&phone=%s&text=' %(phoneformatted.lstrip('+'))) 

            #espero a que la caja de texto del whatsapp se muestre para poder ingresar 
            messageBoxText = WebDriverWait(browser, 60).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'))
            )
            #cuando se inicia, se cargan todos los elementos, pero aparece un popup de cargando mensajes...tengo que esperar a que se quite
            WebDriverWait(browser, 30).until(
                EC.invisibility_of_element_located((By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div'))
            )
            
            for msg in messages:
                messageBoxText.send_keys(msg)
                messageBoxText.send_keys(Keys.ENTER)
                time.sleep(1)

            sendFileButton = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div')
            sendFileButton.click()

            selectSendImage = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button'))
            )

            selectSendImage.click()
            
            time.sleep(1.5)

            pyautogui.write('"%s\\Lucia (7).jpeg" "%s\\Lucia (1).jpeg" "%s\\Lucia (2).jpeg"' % (dirImages,dirImages,dirImages))  
            pyautogui.press('enter')

            sendImageButton = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div'))
            )
            sendImageButton.click()         
            
            time.sleep(2)
            ##espero a que se haya enviado la imagen, y cierro la pestaña de whatsapp
            ##obtengo el div del chat, el cual tiene todos los divs de los mensajes (la cantidad de divs internos es la cantidad de mensajes cargados en la web)
            chatContainer = browser.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/div[2]/div[3]')
            messagesContainers = chatContainer.find_elements(By.XPATH,'*')
            #print('longitud '+str(len(messagesContainers)))

            pathFitstCheckButton = '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[%s]/div/div/div[1]/div[1]/div/div[2]/div/div/span' %(str(len(messagesContainers) - 2))
            pathSecondCheckButton = '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[%s]/div/div/div[1]/div[1]/div/div[2]/div/div/span'%(str(len(messagesContainers) - 1))
            pathThirdCheckButton = '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[%s]/div/div/div[1]/div[1]/div/div[2]/div/div/span' %(str(len(messagesContainers)))

            ##sepero a que las imagenes se hayan enviado
            try:
                WebDriverWait(browser, 20).until(
                    EC.all_of(
                        CF.texts_to_be_presents_in_element_attribute((By.XPATH, pathFitstCheckButton), 'aria-label', [' Enviado ', ' Entregado ']),
                        CF.texts_to_be_presents_in_element_attribute((By.XPATH, pathSecondCheckButton), 'aria-label', [' Enviado ', ' Entregado ']),
                        CF.texts_to_be_presents_in_element_attribute((By.XPATH, pathThirdCheckButton), 'aria-label', [' Enviado ', ' Entregado '])
                    )
                )
            except: 
                print('NO SE PUDO ENVIAR LAS IMAGENES, ES PROBABLE QUE NO ESTE CONECTADO A INTERNET, O LA CONEXION SEA MUY LENTA, ENVÍE MANUALMENTE LAS IMAGENES Y EJECUTE NUEVAMENTE EL ROBOT...')
                print('Numero telefonico pendiente de envio de Informacion: '+phone)
                sys.exit()
                browser.quit()

            browser.close()
            browser.switch_to.window(browser.window_handles[0])
          
        else:
            print('SE ENCONTRO UN NUMERO DE TELEFONO INVALIDO, PROGRAMAR LA LOGICA PRRO')
            browser.quit()
            sys.exit()
            
        
    except:
        print('ERROR DESCONOCIDO CUANDO SE ENVIABA LA INFORMACION POR WHATSAPP...')
        sys.exit()
        #browser.quit()

def followCustomers(browser):
    name = ''
    phoneNumber = ''
    messagesTemplate = ['','Buenos días XXXX le saluda Katherine Quintana, Asesora Inmobiliaria de trivo.','Le escribo porque queremos saber si aún tiene interés en adquirir bienes inmuebles.']
    linkWhatsaPo = ''
    sector = '' # de acuerdo al sector, aparecen unas opciones u otras
    observations = [
        Observation("whatsapp", 'Seguimiento.'),
        Observation("whatsapp", 'Se enviaron fotos de Lucia.'),
        Observation("nota", 'Esperando contestación.'),
    ]
    

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
                return ('//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[%s]' % (i))
                

        print('TODAS LOS CLIENTES QUE SE MUESTRAN EN LA TABLA SON NUEVOS')
        return ''

    
    while True:
        #obtengo el xpath de la fila del cliente que lleva mas tiempo sin interacciones
        xpath = findCustomertoEdit(browser)
        #obtengo la columna donde está guardado el sector de dicho usuario
        xpathSector = '%s/td[7]' % (xpath)
        #guardo el sector de dicha columna
        sectorTable = browser.find_element(By.XPATH, xpathSector)
        sector = sectorTable.text
        #obtengo la columna donde está guardado el boton de editar
        xpathEdit = '%s/td[2]' % (xpath)

        #verifico que el la ultima fecha de contacto sea mayor a 50 dias (que es mas o menos cuando se pone en rojo), caso contrario paro de hacer seguimiento
        if not CF.dateInRed:
            break

        #hago click en el cliente que mas tiempo le tengo olvidado
        editButton = browser.find_element(By.XPATH, xpathEdit)
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

        ### NOTA IMPORTANTE
        ### En esta parte del cuestionario, los clientes que tienen sector definido (eso se ve en la tabla con un signo '-'), se les muestra una opcion extra (en la primera posicion)
        ### La opcion es "ASIGNAR LEAD", la cual va en la primera posicion del cuestionario
        ### por lo que se valida en todos los componentes para evitar dar click en otro componente, simplemente se accede a una posicion menos
        hasLead = (sector != '-')
        #muestro las opciones
        selectField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div[2]/div/div/div/div' %('3' if hasLead else '2'))
        selectField.click()
           #selecciono la opcion de seguimiento
        selectFieldSecondOption = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]'))
        )
        selectFieldSecondOption.click()

        #copio el mensaje que se enviara al whatsapo
        messageField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div[2]/div[2]/div[2]/div' %('3' if hasLead else '2')))
        )  
        #guardo el mensaje
        messages = messagesTemplate[:]
        messages[0] = messageField.text.replace('XXXX', name)
        #en el segundo mensaje del array, el nombre esta con XXXX
        messages[1] = messages[1].replace('XXXX', name.split()[0])
        #click en el boton para continuar (Esto abre whatsapp en una nueva ventana)
        continueButton = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div/button' %('10' if hasLead else '9'))
        continueButton.click()

        #confirmar que deseo continuar
        confirmButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[2]'))                 ##USAR ESTA INSTRUCCION
            #EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[1]'))
        ) 
        confirmButton.click()

        ##pyautogui.hotkey('ctrl', 't')                                                                               ##BORRAR ESTA INSTRUCCION           

        #envio info por whatsapp
        sendInfoWhatsApp(browser, phoneNumber, messages, '%s\\Pictures\\FotosTrivo\\Lucia' %(os.path.expanduser("~")))
        #regreso a donde inicie (A la tabla de clientes)
        goBackFirst = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/button')
        goBackFirst.click()
        
        ##procedo a añadir las notas del seguimiento
        for observation in observations:
            interactionsList = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div/div/div/div')
            interactionsList.click()
            observationOption = browser.find_element(By.XPATH, observation.xpath)
            observationOption.click()
            textArea = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[3]/div[3]/div/div/textarea')
            textArea.send_keys(observation.message)
            addObservationButton = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[3]/div[4]/button') 
            addObservationButton.click()
            time.sleep(1)
            WebDriverWait(browser, 10).until(
                EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div[2]/div[8]/div[1]/div/*[name()="svg"]'))
            )
        goBackTable = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[1]/button')
        goBackTable.click()

