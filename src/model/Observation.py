class Observation:
    def __init__(self, observationType, message):   
        self.message = message
        if observationType == 'nota':
            self.xpath = '//*[@id="menu-"]/div[2]/ul/li[1]'
        elif observationType == 'llamada':
            self.xpath = '//*[@id="menu-"]/div[2]/ul/li[2]'
        elif observationType == 'whatsapp':
            self.xpath = '//*[@id="menu-"]/div[2]/ul/li[3]'
        elif observationType == 'email':
            self.xpath = '//*[@id="menu-"]/div[2]/ul/li[4]'
        elif observationType == 'personal':
            self.xpath = '//*[@id="menu-"]/div[2]/ul/li[5]'
        else:
            print('OBSERVACION NO VALIDA, O NO SE ENCUENTRA PROGRAMADA')
            self.xpath = ''


