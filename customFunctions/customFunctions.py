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


def formatPhoneNumber(phoneNumber):
    #obtiene un numero y si esta en formato 09##### lo regresa a formato +593###
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

    
