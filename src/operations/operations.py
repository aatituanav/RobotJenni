from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from src.model.Observation import Observation
from selenium.webdriver.common.by import By


import src.customFunctions.customFunctions as CF
import pyautogui
import time
import sys
import os

def iniciarSesion(browser, projectObject):
    try:
        emailField = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[1]/div/input')
        emailField.clear()
        emailField.send_keys(projectObject.email)
        #encuentro el campo de texto para contrasenia
        passwordField = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/input')
        passwordField.clear()
        passwordField.send_keys(projectObject.password)
        time.sleep(0.5)
        passwordField.send_keys(Keys.ENTER)
    except Exception as e: 
        print(e)
        browser.quit()

def orderDataTableByLastContact(browser):
    #ordeno la tabla
    try:
        #espero a que se cargue el campo de texto del correo
        lastDayContactHeader = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/table/thead/tr/th[12]')) 
        )
        lastDayContactHeader.click()
        lastDayContactHeader = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/table/thead/tr/th[12]'))
        )
        lastDayContactHeader.click()
    except Exception as e: 
        print(e)
        browser.quit()

def selectDateInDatePicker(browser, date):
    
    year, month, day = [str(int(item)) for item in date.split('-')]
    #print('date '+date)
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    yearElement = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="picker-popover"]/div[2]/div[1]/div[1]/h6'))
    )
    if yearElement.text != year:
        yearElement.click()
        yearOption = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH,'//div[text()="%s"]' %(year)))
        )
        yearOption.click()
    
    calendarHeader = browser.find_element(By.XPATH, '//*[@id="picker-popover"]/div[2]/div[3]/div/div[1]/div[1]/div/p')
    monthText = calendarHeader.text.split(' ')[0]
    if monthText != meses[int(month) - 1]: 
        #para saber si se debe ir a la derecha en los meses o a la izquierda
        if meses.index(monthText) + 1 > int(month):
            #print('retroceder %s meses' %(meses.index(monthText) + 1  - int(month)))
            for i in range(meses.index(monthText) + 1  - int(month)):
                leftButton = browser.find_element(By.XPATH, '//*[@id="picker-popover"]/div[2]/div[3]/div/div[1]/div[1]/button[1]')
                leftButton.click()
                time.sleep(0.05)

        elif meses.index(monthText) + 1 < int(month):
            #print('adelantar %s meses' %(int(month) - (meses.index(monthText) + 1 )))
            for i in range(meses.index(monthText) + 1  - int(month)):
                rightButton = browser.find_element(By.XPATH, '//*[@id="picker-popover"]/div[2]/div[3]/div/div[1]/div[1]/button[2]')
                rightButton.click()   
                time.sleep(0.05)
    #espero a que el boton 15 se pueda hacer click (esto es por que cuando quiero hacer click en botones como el 31, hay 2 en el calendario, uno oculto y otro no, pero cuando hace la comprobacion si es clickable, solamente analiza con el primer elemento encontrado (el que no se puede hacer click) por eso la comprobacion falla), por eso hago la comprobacion con un boton que nunca va a tener un duplicado (que es el 15) 
    WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH,'//*[text()="15"]//ancestor::button')) 
    )
    dayOption = browser.find_elements(By.XPATH,'//*[text()="%s"]//ancestor::button' %(day))
    #obtengo todos los botones y hago click en el que se puede hacer click
    for day in dayOption:
        if day.is_displayed():
            day.click()
    #obtengo los dos potenciales botones que pueden aparecer y analizo cual de ellos se puede hacer click
    time.sleep(0.2)
    hourOption = browser.find_element(By.XPATH, '//*[@id="picker-popover"]/div[2]/div[3]/div/div/div/div[1]')
    hourOption.click()
    time.sleep(0.2)
    hourOption.click()
    time.sleep(0.2)
  
def findCustomertoEdit(browser):
        #Los nuevos usuarios aparecen con el campo "FECHA ULTIMO CONTACTO" vacio, por lo cual no hay que hacer seguimiento de dichos usuarios
        #Por lo tanto al ordenar por fecha, estos usuarios aparecen primero, por lo cual es necesario saber en que fila estan los usuarios no nuevos 
        #de esta manera si hay 4 usuarios nuevos, habria que hacer seguimiento al 5 usuario (siempre y cuando la tabla este ordenada por fecha)
        #este metodo regresara el xpath del componente que el robot tendra que hacer click
        numberofRows = 20
        ##la informacion se muestra desde la posicion 1, (0 es para la cabecera)
        WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[1]/td[12]'))
        )

        for i in range(1, numberofRows + 1):
            selectField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[%s]/td[12]' % (i))
            if selectField.text != '-':
                return ('//*[@id="root"]/div/div[2]/div/div/div[2]/table/tbody/tr[%s]' % (i))
        #print('TODAS LOS CLIENTES QUE SE MUESTRAN EN LA TABLA SON NUEVOS')
        return ''

def sendInfoWhatsApp(browser, phone, messages, dirImages):
    ##este metodo solo funciona para enviar 3 fotos que se encuentren en dirImages
    ##dirImages: direccion de la carpeta raiz de las imagenes
    ##messages: lista que contiene todos los mensajes que se enviaran
    ##phone: numero de telefono al cual enviar la informacion
    ##browser: la instancia del navegador en el cual esta trabajando el robot

    #cambio a la nueva ventana que se abrio automaticamente
    
    #phone = '+593993055278'
    phoneformatted = CF.formatPhoneNumber(phone)

    ##verifico que sea un numero de celular con +593 para quitarle
    if phoneformatted != None:
        browser.get('https://web.whatsapp.com/send?l=es&phone=%s&text=' %(phoneformatted.lstrip('+'))) 

        #espero a que la aplicacion se haya cargado correctamente
        try:
            WebDriverWait(browser, 60).until(
                EC.any_of(
                    #lanza un error si se detecta el popup que indica que se ingreso un numero invalido
                    CF.raise_error_if_text_is_present_in_element((By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div/div/div'), 'OK'),
                    EC.all_of(
                        #espero a que el cuadro de texto para enviar mensajes
                        EC.visibility_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')),   
                        #espero a que el popup "Cargando mensajes" se haya terminado de cargar
                        EC.invisibility_of_element_located((By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div'))
                    )
                )
            )
        except Exception as e:
            print('ERROR: ES PROBABLE QUE LA CONEXION SEA MUY LENTA, O HAYA INGRESADO UN NUMERO INVALIDO... ENVÍE MANUALMENTE LAS IMAGENES Y EJECUTE NUEVAMENTE EL ROBOT...')
            print('Numero telefonico pendiente de envio de Informacion: '+phone)
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            return False
        #obtengo la caja de mensajes
        messageBoxText = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
        for msg in messages:
            messageBoxText.send_keys(msg)
            messageBoxText.send_keys(Keys.ENTER)
            time.sleep(2)
        #boton para enviar imagenes
        sendFileButton = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div')
        sendFileButton.click()
        inputImages = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'))
        )

        time.sleep(1)
        ##obtengo el path de todas las imagenes en la carpeta Imagenes/FotosTrivo/Lucia
        imageInput = ''
        listDirImages = os.listdir(dirImages)
        for image in listDirImages:
            imageInput += ''+ dirImages +"\\"+ image + '\n'
        
        #busco el imput para enviar los archivos y los coloco
        inputImages.send_keys(imageInput.strip())
        #boton para confirmar el envio
        sendImageButton = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div'))
        )
        sendImageButton.click()

        time.sleep(4)
        ##espero a que se haya enviado la imagen, y cierro la pestaña de whatsapp
        ##obtengo el div del chat, el cual tiene todos los divs de los mensajes (la cantidad de divs internos es la cantidad de mensajes cargados en la web)
        chatContainer = browser.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/div[2]')
        childrenChatContainer = len(chatContainer.find_elements(By.XPATH,'*'))
        positionMessagesContainer = '3' if childrenChatContainer == 3 else '2'
        messagesContainer = browser.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/div[2]/div[%s]' %(positionMessagesContainer))
        messages = messagesContainer.find_elements(By.XPATH,'*')
        
        ##sepero a que las imagenes se hayan enviado
        try:    
            WebDriverWait(browser, 30).until(
                CF.allImagesSent(len(listDirImages), len(messages), positionMessagesContainer)
            )
        except: 
            print('NO SE PUDO ENVIAR LAS IMAGENES, ENVÍE MANUALMENTE LAS IMAGENES Y EJECUTE NUEVAMENTE EL ROBOT...')
            print('Numero telefonico pendiente de envio de Informacion: '+phone)
            print('LOG:')
            print(len(listDirImages), len(messages))
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            browser.quit()
            return False

        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return True

    else:
        print('SE ENCONTRO UN NUMERO DE TELEFONO INVALIDO, PROGRAMAR LA LOGICA PRRO')
        print('Numero telefonico pendiente de envio de Informacion: '+phone)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return False

def scheduleTask(browser, mensaje, diasDeEspera):
    #SECCION DE AGENDAMIENTO DE NUEVA TAREA
    #mensaje: es el titulo de la tarea
    #diasDeEspera: son los dias de espera (si se necesita la tarea para de aqui a 15 dias, se colocara el numero 15)
    #=============================================================================================
    #=============================================================================================
    titleInput = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[1]/div/input'))
    )
    titleInput.send_keys(mensaje)
    time.sleep(0.2)
    dateField = browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[3]/div/div/input')
    dateField.click()
    time.sleep(0.1)
    
    #espero a que el datepicker se muestre en el dom
    WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.XPATH,'//*[@id="picker-popover"]/div[2]'))                
    )
    #selecciono la fecha
    selectDateInDatePicker(browser, CF.addDays(diasDeEspera))
    #click en el boton de agendar
    #espero a que se pueda hacer click y a que el datapicker haya desaparecido
    WebDriverWait(browser, 30).until(
        EC.all_of(
            (EC.element_to_be_clickable((By.XPATH,'/html/body/div[5]/div[2]/div/div[3]/button[1]'))),                 
            (EC.invisibility_of_element_located((By.XPATH,'//*[@id="picker-popover"]/div[2]')))
        )
    )
    createTaskButton = browser.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[3]/button[1]')
    createTaskButton.click()
    #click en el boton de confirmar
    #espero a que sea visible y se pueda hacer click
    WebDriverWait(browser, 30).until(
        EC.all_of(
            (EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div[2]/div/div[3]/button[2]'))),                 
            (EC.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div[2]/div/div[3]/button[2]')))
        )
    )
    confirmTask = browser.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div[3]/button[2]')
    confirmTask.click()
    #=============================================================================================
    #=============================================================================================

def fillObservations(browser, observation):
    interactionsList = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div/div/div/div')
    interactionsList.click()
    observationOption = browser.find_element(By.XPATH, observation.xpath)
    observationOption.click()
    textArea = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[3]/div[3]/div/div/textarea')
    textArea.send_keys(observation.message)
    addObservationButton = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[3]/div[4]/button') 
    addObservationButton.click()
    time.sleep(1)
    WebDriverWait(browser, 30).until(
        EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div[2]/div[8]/div[1]/div/*[name()="svg"]'))
    )

def doTracktoCustomer(browser, xpathOfCustomer, hasLead, messagesTemplate, xpathDictionary):

    #obtengo la campania o proyecto en el que el cliente esta instcrito
    campania = browser.find_element(By.XPATH, '%s/td[4]' % (xpathOfCustomer)).text

    #hago click en el cliente que mas tiempo le tengo olvidado
    editUser = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '%s/td[2]/*[name()="svg"]' % (xpathOfCustomer)))
    )
    editUser.click()

    #espero a que cargue el formulario
    siguientesAccionesButton = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[2]/div/button'))
    )
    WebDriverWait(browser, 30).until(
        EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/div[2]/div/div/div/div[2]/div[8]/div[1]/div/*[name()="svg"]'))
    )
    
    #obtengo el nombre del cliente
    name = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div[1]/h4').text
    #obtengo el numero de celular del cliente
    phoneNumber = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div[2]/a/h6').text.strip()
    
    #avanzo a la siguiente paguina mediante el boton "SIGUIENTES ACCIONES"
    siguientesAcciones = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[2]/div/table/tbody/tr/td[2]/div/button')
    siguientesAccionesButton.click()

    #espero que termine de cargar la paguina (que desaparezca el loadbutton) y que se pueda dar click en el boton
    continueButton = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div/button' %('10' if hasLead else '9')))
    )
    WebDriverWait(browser, 30).until(
        EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/*[name()="svg"]'))
    )
    
    ##lleno los datos del cuestinoario y continuo con la siguiente paguina
    #muestro las opciones
    selectField = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div[2]/div/div/div/div' %('3' if hasLead else '2'))
    selectField.click()
    #selecciono la opcion de seguimiento
    time.sleep(0.3)
    selectFieldSecondOption = WebDriverWait(browser, 30).until(
         EC.element_to_be_clickable((By.XPATH, xpathDictionary.LI_seguimientoInfoInicialEnviada))
    )
    selectFieldSecondOption.click()
    #copio el mensaje que se enviara al whatsapo
    messageField = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div[2]/div[2]/div[2]/div' %('3' if hasLead else '2')))
    )  
    #guardo el mensaje
    messages = messagesTemplate[:]
    messages[0] = messageField.text
    for index, message in enumerate(messages):
        #en el primer mensaje, coloco nombre y apellido, si hay demas mensajes, solo coloco el nombre
        if index > 0:
            messages[index] = message.replace('XXXX', name.split()[0])
        else:
            messages[index] = message.replace('XXXX', name)

    #click en el boton para continuar (Esto abre whatsapp en una nueva ventana)
    continueButton.click()
    #confirmar que deseo continuar
    WebDriverWait(browser, 30).until(
        EC.all_of(
            (EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[2]'))),                 ## CONFIRMAR (USAR ESTA INSTRUCCION)
            (EC.visibility_of_element_located((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[2]')))
        )
        #EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[1]'))                  ## CANCELAR
    )
    confirmButton = browser.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[2]')
    #confirmButton = browser.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/button[1]')              ## CANCELAR

    confirmButton.click()

    #pyautogui.hotkey('ctrl', 't')                               ##BORRAR ESTA INSTRUCCION           
    #envio info por whatsapp
    browser.switch_to.window(browser.window_handles[1])
    pyautogui.hotkey('ctrl', 'w')
    browser.switch_to.window(browser.window_handles[0])
    pyautogui.hotkey('ctrl', 't')
    browser.switch_to.window(browser.window_handles[1])

    folderRelativeImages = 'Trivo\\%s' %(xpathDictionary.getFolder(campania)) if xpathDictionary.name=="Trivo" else xpathDictionary.name
    folderAbsoluteImages = '%s\\CRM\\%s' %(os.path.expanduser("~"), folderRelativeImages)
    
    infoSend = sendInfoWhatsApp(browser, phoneNumber, messages, folderAbsoluteImages)
    if infoSend:
        #antes de regresar, Agrego una tarea nueva para una semana
        newTaskButton = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[%s]/div/*[name()="svg"]' %('9' if hasLead else '8')))
        )
        newTaskButton.click()
        #SECCION DE AGENDAMIENTO DE NUEVA TAREA
        scheduleTask(browser, 'Seguimiento', 14)
    #regreso una paguina
    goBackFirst = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/button'))
    )
    goBackFirst.click()
    
    ##espero a que el cuestinoario se cargue
    WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[1]/button'))                
    )
    WebDriverWait(browser, 30).until(
        EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[2]/div[8]/div[1]/div/*[name()="svg"]'))
    )
    
    #Observaciones 
    observations = [
        Observation("nota", 'Seguimiento.')
    ]
    ##analizo si envio imagenes o videos
    listDirImages = os.listdir(folderAbsoluteImages)
    print(listDirImages)
    if any(file.endswith((".mp4", ".MP4")) for file in os.listdir(folderAbsoluteImages)):
        observations.append(Observation("whatsapp", 'Video de %s' %(xpathDictionary.getFolder(campania).title())))
    if any(file.endswith((".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG")) for file in os.listdir(folderAbsoluteImages)):
        observations.append(Observation("whatsapp", 'Imagen de %s' %(xpathDictionary.getFolder(campania).title())))
    observations.append(Observation("nota", 'Esperando contestación.'))

    #si se envio por whatsapp la info, procedo a llenar las observaciones
    if infoSend:
        for observation in observations:
            fillObservations(browser, observation)
    #regreso a donde inicie (A la tabla de clientes)
    goBackTable = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div[1]/button')
    goBackTable.click()
    
    WebDriverWait(browser, 30).until(
        EC.invisibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div/div/*[name()="svg"]'))
    )

def login(browser, projectObject):
    print('se inicia sesion en '+projectObject.name)
    browser.get('https://admin.trivo.com.ec/login/'+projectObject.name.lower())

    elementToWait = WebDriverWait(browser, 30).until(
        EC.any_of(
            (EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/header/div/a/img'))),
            (EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div/div/div/h1')))
        )
    )
    tag_name = elementToWait.tag_name

    if tag_name == 'h1':
        #en el caso de que no este iniciada la sesion, simplemente la inicia
        iniciarSesion(browser, projectObject)
        #espero a que el elemento se haya ido del dom (es para el robot de trivo, ya que necesita abrir otra pestaña)
        WebDriverWait(browser, 30).until(
            EC.invisibility_of_element(elementToWait)
        )
    elif tag_name == 'img':
        #si la sesion esta iniciada, 
        #verifico que este en la sesion correcta
        srcLogo = browser.find_element(By.XPATH, '//*[@id="root"]/div/header/div/a/img').get_attribute('src')
        if srcLogo != projectObject.srcLogo:
            print('La sesión está en otro proyecto')
            logoutButton = browser.find_element(By.XPATH, '//*[@id="root"]/div/header/div/button[2]')
            logoutButton.click()
            login(browser, projectObject)





    
    

    