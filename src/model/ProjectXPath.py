class XPathByProject:
    #todos los cuestionarios son los mismos, solo que algunos difieren el lugar donde se encuentra la misma informacion 
    def __init__(self, project):   
        if project == 'trivo':
            self.name = 'Trivo'
            self.LI_seguimientoInfoInicialEnviada = '//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[34]'
        elif project == 'lucia':
            self.name = 'Lucia'
            self.LI_seguimientoInfoInicialEnviada = '//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]'


