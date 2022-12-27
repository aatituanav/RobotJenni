from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import sys
import os


def allImagesSent(numberOfImagesSent, numberOfElements):
    #este metodo veridica que todas las imagenes enviadas se hayan enviado o recibido
    #print('SE HARA UNA VALIDACION DE LAS IMAGESNES')
    #este es el xpath del span que muestra las palomitas de enviado o recibido
    def _predicate(driver):
        text = [' Enviado ', ' Entregado ']
        try:
            #print(numberOfImagesSent, numberOfElements)
            for i in range(numberOfImagesSent):
                #print(i)
                xpath = '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[%s]/div/div/div[1]/div[1]/div/div[2]/div/div/span' %(numberOfElements - i)
                #print('--------------------------------------------------------')
                #print(xpath)
                element_text = driver.find_element(By.XPATH, xpath).get_attribute('aria-label')
                #print(element_text)
                if element_text is None:
                    #print('se regesara none')
                    return False
                if not element_text in text:
                    #print('se regesara Falso')
                    return False
            #print('se regresara true')
            return True
        except Exception as e:
            #print(e)
            return False

    return _predicate

def texts_to_be_presents_in_element_attribute(locator, attribute_, text_):
    """
    An expectation for checking if any of text are present in the element's attribute.
    locator, attribute, text
    """
    
    def _predicate(driver):
        try:
            print('--------------------------------------------------------')
            print(locator)
            element_text = driver.find_element(*locator).get_attribute(attribute_)
            if element_text is None:
                return False
            return  element_text in text_
        except:
            return False

    return _predicate

def raise_error_if_text_is_present_in_element(locator, text_):
    """lanza un error si encuentra un texto en un componente
    """
    def _predicate(driver):
        try:
            element_text = driver.find_element(*locator).text
            if text_ == element_text:
                raise Exception("invalido")
            else:
                return False
        except Exception as e:
            if (len(e.args)>0):
                if e.args[0] == 'invalido':
                    raise Exception("EL TELEFONO ES INVALIDO!!!")
            else:
                return False

    return _predicate


def formatPhoneNumber(phoneNumber):
    #obtiene un numero y si esta en formato 09##### lo regresa a formato +593###
    #formatos admitidos
    #   096-905-8836
    #   0969058836
    #   +593969058836
    phoneNumber = phoneNumber.replace('-','').strip()
    if phoneNumber.find('+') != -1 and len(phoneNumber) == 13:
        return phoneNumber
    elif len(phoneNumber) == 10:
        return '+593' + phoneNumber[1:]
    else:
        return None
    

def validDateforContinue(date, days):
    #solo acepta fechas menores a n dias 
    curentDate = datetime.now()
    dateLastContact = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=days)
    if dateLastContact <= curentDate:
        return True
    else:
        return False


def addDays(daysAdded):
    #dateFormatted = datetime.strptime(date, "%Y-%m-%d")
    return (datetime.now() + timedelta(days=daysAdded)).strftime("%Y-%m-%d")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
