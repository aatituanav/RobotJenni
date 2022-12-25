from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.model.Observation import Observation
from src.model.ProjectXPath import XPathByProject
from selenium.webdriver.common.by import By

import src.customFunctions.customFunctions as CF
import src.operations.operations as operations
import pyautogui
import time
import sys
import os


def startPromonsaRobot(browser):

    print('robot Promonsa Iniciado')
    #abrir la paguina
    browser.get('https://admin.trivo.com.ec/login/promonsa')

    messagesTemplate = ['']
    observations = [
        Observation("whatsapp", 'Seguimiento.'),
        Observation("whatsapp", 'Video de Promonsa.'),
        Observation("nota", 'Esperando contestación.'),
    ]

    

    
    operations.orderDataTableByLastContact(browser)

    srcLogo = browser.find_element(By.XPATH, '//*[@id="root"]/div/header/div/a/img').get_attribute('src')
    if srcLogo != 'https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1615475557832-lg.png':
        print('ACTUALMENTE LA SESIÓN ESTÁ INICIADA EN OTRO PROYECTO... CAMBIE LA SESION E INICIE EL ROBOT NUEVAMENTE')
        browser.quit()
        return

    while True:
        #obtengo el xpath de la fila del cliente que lleva mas tiempo sin interacciones
        xpath = operations.findCustomertoEdit(browser)
        xpathDictionary = XPathByProject('promonsa')
        ### NOTA IMPORTANTE
        ### En una parte del cuestionario, los clientes que tienen sector definido (eso se ve en la tabla con un signo '-'), se les muestra una opcion extra (en la primera posicion)
        ### La opcion es "ASIGNAR LEAD", la cual va en la primera posicion del cuestionario
        ### por lo que se valida en todos los componentes para evitar dar click en otro componente, simplemente se accede a una posicion menos
        hasLead = (browser.find_element(By.XPATH, '%s/td[7]' % (xpath)).text) != '-'
        #obtengo la fecha de ultimo contacto
        lastDateContact =  browser.find_element(By.XPATH, '%s/td[12]' % (xpath)).text
        #verifico que el la ultima fecha de contacto sea mayor a n dias, caso contrario paro de hacer seguimiento
        if not CF.validDateforContinue(lastDateContact, 50):
            break
            
        operations.doTracktoCustomer(browser, xpath, hasLead, messagesTemplate, observations, xpathDictionary)