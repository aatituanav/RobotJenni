from datetime import datetime, timedelta



def texts_to_be_presents_in_element_attribute(locator, attribute_, text_):
    """
    An expectation for checking if any of text are present in the element's attribute.
    locator, attribute, text
    """
    def _predicate(driver):
        try:
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
    

def dateInRed(date):
    #determina si la fecha ha pasado los
    DateFlag = datetime.now() - timedelta(days=50)
    DateLastContact = datetime.strptime(date, "%Y-%m-%d")
    if DateFlag > DateLastContact:
        print("Hacer seguiniento")
    else:
        print("No hace falta hacer seguimiento")


def addDays(daysAdded):
    #dateFormatted = datetime.strptime(date, "%Y-%m-%d")
    return (datetime.now() + timedelta(days=daysAdded)).strftime("%Y-%m-%d")
