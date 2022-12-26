
from dotenv import load_dotenv
import os

class XPathByProject:
    #todos los cuestionarios son los mismos, solo que algunos difieren el lugar donde se encuentra la misma informacion 
    def __init__(self, project):
        load_dotenv()
        self.email = os.getenv("EMAIL")  
        if project == 'trivo':
            self.name = 'Trivo'
            self.password = os.getenv("PASSWORD_TRIVO")  
            self.srcLogo = 'https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1585002874423-lg.png'
            self.LI_seguimientoInfoInicialEnviada = '//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[34]'
        elif project == 'lucia':
            self.name = 'Lucia'
            self.password = os.getenv("PASSWORD_LUCIA") 
            self.srcLogo = 'https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1635263729281-lg.png'
            self.LI_seguimientoInfoInicialEnviada = '//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]'
        elif project == 'promonsa':
            self.name = 'Promonsa'
            self.password = os.getenv("PASSWORD_PROMONSA") 
            self.srcLogo = 'https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1615475557832-lg.png'
            self.LI_seguimientoInfoInicialEnviada = '//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]'


