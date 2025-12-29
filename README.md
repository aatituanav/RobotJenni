# RobotJenni - Documentación Técnica Completa

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Requisitos del Sistema](#requisitos-del-sistema)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Arquitectura del Sistema](#arquitectura-del-sistema)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Componentes Principales](#componentes-principales)
8. [Flujo de Trabajo](#flujo-de-trabajo)
9. [Configuración de Proyectos](#configuración-de-proyectos)
10. [Guía de Uso](#guía-de-uso)
11. [Detalles Técnicos](#detalles-técnicos)
12. [Solución de Problemas](#solución-de-problemas)
13. [Mantenimiento y Extensión](#mantenimiento-y-extensión)

---

## Descripción General

**RobotJenni** es un robot de automatización para la gestión de leads en CRM inmobiliario. Diseñado específicamente para automatizar el proceso de seguimiento de clientes potenciales en proyectos inmobiliarios, el robot integra WhatsApp Web con el sistema CRM de Trivo (admin.trivo.com.ec) para enviar mensajes personalizados, imágenes y videos, además de registrar todas las interacciones automáticamente.

### Propósito
El robot automatiza el trabajo manual y repetitivo de:
- Identificar clientes que requieren seguimiento
- Enviar mensajes personalizados por WhatsApp
- Adjuntar material promocional (imágenes/videos)
- Registrar observaciones en el CRM
- Agendar tareas de seguimiento

### Proyectos Soportados
1. **Lucia** - Seguimiento cada 50 días
2. **Trivo** - Seguimiento cada 15 días (múltiples sub-campañas)
3. **Promonsa** - Seguimiento cada 50 días

---

## Características Principales

### 1. Gestión Automática de Leads
- Identificación automática de clientes sin contacto reciente
- Ordenamiento de leads por fecha de último contacto
- Priorización basada en días de inactividad

### 2. Integración con WhatsApp
- Envío automático de mensajes personalizados
- Adjuntar hasta 3 archivos (imágenes/videos)
- Verificación de entrega de mensajes
- Soporte para múltiples formatos: PNG, JPG, JPEG, MP4

### 3. Gestión de CRM
- Login automático en Trivo CRM
- Navegación automática de formularios
- Registro de observaciones (nota, llamada, whatsapp, email, personal)
- Agendamiento de tareas de seguimiento (14-18 días)

### 4. Validación y Seguridad
- Validación de números telefónicos en múltiples formatos
- Protección con contraseña
- Gestión de sesiones persistentes
- Detección de números inválidos

### 5. Gestión Multi-Proyecto
- Configuración específica por proyecto
- Mapeo de campañas a carpetas de recursos
- Credenciales independientes por proyecto
- XPath personalizados por proyecto

---

## Requisitos del Sistema

### Software Requerido
```
Python 3.11+
Google Chrome (última versión)
ChromeDriver compatible con la versión de Chrome instalada
```

### Dependencias Python
```
selenium==4.7.2
python-dotenv==0.21.0
PyAutoGUI==0.9.53
auto-py-to-exe (para compilación)
```

### Requisitos Adicionales
- Conexión a Internet estable
- WhatsApp Web configurado y funcional
- Cuenta activa en admin.trivo.com.ec
- Permisos de administrador en Windows (para acceso a carpetas de usuario)

---

## Instalación y Configuración

### 1. Instalación de Dependencias

```bash
# Clonar o descargar el repositorio
cd RobotJenni

# Instalar dependencias
pip install selenium==4.7.2
pip install python-dotenv==0.21.0
pip install PyAutoGUI==0.9.53
```

### 2. Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Email para login en CRM
EMAIL=tu_email@ejemplo.com

# Contraseña de protección de la aplicación
PASSWORD=tu_contraseña_aplicacion

# Contraseñas específicas por proyecto
PASSWORD_LUCIA=contraseña_proyecto_lucia
PASSWORD_TRIVO=contraseña_proyecto_trivo
PASSWORD_PROMONSA=contraseña_proyecto_promonsa
```

### 3. Estructura de Carpetas de Recursos

Crear las siguientes carpetas en la ubicación del usuario:

```
C:\Users\<TuUsuario>\CRM\
├── Lucia\              # Máximo 3 archivos (imágenes/videos)
├── Promonsa\           # Máximo 3 archivos (imágenes/videos)
└── Trivo\
    ├── DIAMOND GARDEN\
    ├── APARTAT\
    ├── BOTANIQO\
    ├── DISTRICT\
    ├── IBAGARI\
    ├── MAGIC\
    ├── TERRALTA\
    └── NATIVA\         # Carpeta por defecto
```

**IMPORTANTE**: Cada carpeta debe contener máximo 3 archivos de imagen o video.

### 4. Configuración de ChromeDriver

Colocar el archivo `chromedriver.exe` en la raíz del proyecto. Asegurarse de que la versión coincida con la versión de Chrome instalada.

Verificar versión de Chrome:
```
chrome://version/
```

Descargar ChromeDriver correspondiente desde: https://chromedriver.chromium.org/

---


## Componentes Principales

### 1. main.py (58 líneas)

**Propósito**: Punto de entrada de la aplicación.

**Funcionalidades**:
- Protección con contraseña
- Menú de selección de proyecto
- Configuración de ChromeDriver
- Inicialización del navegador con persistencia de sesión
- Validación de periodo de prueba (hasta 2023-02-26)

**Configuración del Navegador**:
```python
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=%s' % (userdata))  # Persistencia de sesión
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)  # Navegador no se cierra
```

**Flujo**:
1. Cargar variables de entorno
2. Solicitar contraseña
3. Mostrar menú de proyectos
4. Iniciar navegador Chrome
5. Ejecutar robot del proyecto seleccionado

---

### 2. operations.py (449 líneas)

Contiene la lógica principal de automatización compartida entre todos los proyectos.

#### Funciones Principales:

##### `login(browser, projectObject)`
**Propósito**: Autenticación en Trivo CRM.

**Parámetros**:
- `browser`: Instancia de WebDriver
- `projectObject`: Objeto ProjectXPath con credenciales

**Flujo**:
1. Navegar a URL de login del proyecto
2. Verificar si ya existe sesión activa
3. Validar que la sesión sea del proyecto correcto
4. Iniciar sesión si es necesario

**Manejo de Sesiones**:
- Detecta logo del proyecto para validar sesión activa
- Cierra sesión si está en proyecto incorrecto
- Recursivo: re-llama a login si necesita cambiar de proyecto

---

##### `orderDataTableByLastContact(browser)`
**Propósito**: Ordenar tabla de clientes por fecha de último contacto.

**Técnica**:
- Doble click en el encabezado "Última Fecha de Contacto"
- Ordena de más antiguo a más reciente
- Espera hasta 30 segundos para que la tabla sea clickeable

---

##### `findCustomertoEdit(browser)`
**Propósito**: Encuentra el primer cliente que requiere seguimiento.

**Lógica**:
- Los clientes nuevos tienen campo "FECHA ULTIMO CONTACTO" vacío (mostrado como "-")
- Estos clientes nuevos se saltan
- Retorna el XPath del primer cliente con fecha de contacto válida
- Analiza hasta 20 filas de la tabla

**Retorno**: XPath del cliente a editar, o string vacío si todos son nuevos

---

##### `doTracktoCustomer(browser, xpathOfCustomer, hasLead, messagesTemplate, xpathDictionary)`
**Propósito**: Función principal que ejecuta todo el flujo de seguimiento.

**Parámetros**:
- `xpathOfCustomer`: XPath del cliente en la tabla
- `hasLead`: Boolean que indica si el cliente tiene lead asignado
- `messagesTemplate`: Lista de plantillas de mensaje
- `xpathDictionary`: Objeto ProjectXPath con configuración

**Flujo Completo**:
1. Extraer campaña del cliente
2. Click en botón de editar cliente
3. Esperar carga del formulario
4. Extraer nombre y teléfono del cliente
5. Navegar a formulario de "Siguientes Acciones"
6. Llenar cuestionario seleccionando "Seguimiento"
7. Copiar mensaje del CRM y personalizarlo
8. Enviar información por WhatsApp
9. Agendar nueva tarea de seguimiento (14-18 días)
10. Registrar observaciones en CRM
11. Regresar a tabla de clientes

**Personalización de Mensajes**:
- Primer mensaje: Nombre completo del cliente
- Mensajes subsecuentes: Solo primer nombre
- Reemplaza marcador "XXXX" en plantillas

---

##### `sendInfoWhatsApp(browser, phone, messages, dirImages)`
**Propósito**: Enviar mensajes y archivos multimedia por WhatsApp Web.

**Parámetros**:
- `phone`: Número telefónico (múltiples formatos soportados)
- `messages`: Lista de mensajes a enviar
- `dirImages`: Directorio con imágenes/videos (máximo 3 archivos)

**Flujo**:
1. Formatear número telefónico
2. Abrir WhatsApp Web con URL pre-formateada
3. Esperar carga de la aplicación (timeout: 60 segundos)
4. Detectar errores de número inválido
5. Enviar cada mensaje de la lista
6. Click en botón de adjuntar archivos
7. Seleccionar y enviar todos los archivos de la carpeta
8. Verificar entrega de todos los archivos
9. Cerrar pestaña de WhatsApp

**Manejo de Errores**:
- Detecta popup de número inválido
- Timeout si conexión es muy lenta
- Verifica entrega mediante atributo `aria-label` (Enviado/Entregado)
- Cierra pestaña y retorna `False` si hay error

**Validación de Entrega**:
```python
WebDriverWait(browser, 30).until(
    CF.allImagesSent(len(listDirImages), len(messages), positionMessagesContainer)
)
```

---

##### `scheduleTask(browser, mensaje, diasDeEspera)`
**Propósito**: Agendar tarea de seguimiento en el CRM.

**Parámetros**:
- `mensaje`: Título de la tarea (ej. "Seguimiento")
- `diasDeEspera`:
  - `int`: Días desde hoy para agendar
  - `str`: Fecha específica en formato "YYYY-MM-DD"

**Flujo**:
1. Ingresar título de la tarea
2. Click en campo de fecha
3. Esperar aparición del DatePicker
4. Seleccionar fecha usando `selectDateInDatePicker()`
5. Click en botón "Agendar"
6. Confirmar agendamiento

**Aleatorización**:
En `doTracktoCustomer`, se usa:
```python
scheduleTask(browser, 'Seguimiento', 14 + randrange(5))
```
Esto genera tareas entre 14-18 días para distribuir carga de trabajo.

---

##### `selectDateInDatePicker(browser, date)`
**Propósito**: Navegar y seleccionar fecha en componente DatePicker del CRM.

**Complejidad**: Uno de los métodos más complejos debido a:
- DatePicker con navegación de mes/año
- Elementos duplicados en el DOM
- Validaciones de elementos clickeables

**Parámetros**:
- `date`: Fecha en formato "YYYY-MM-DD"

**Flujo**:
1. Parsear año, mes y día de la fecha
2. Verificar y seleccionar año correcto
3. Calcular diferencia de meses y navegar
4. Esperar que botón "15" sea clickeable (evita duplicados)
5. Seleccionar día correcto entre elementos duplicados
6. Confirmar hora (doble click)

**Truco Técnico**:
```python
# Espera por botón "15" que nunca tiene duplicados
WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.XPATH,'//*[text()="15"]//ancestor::button'))
)
# Luego busca todos los botones del día deseado y click en el visible
dayOption = browser.find_elements(By.XPATH,'//*[text()="%s"]//ancestor::button' %(day))
for day in dayOption:
    if day.is_displayed():
        day.click()
        break
```

---

##### `fillObservations(browser, observation)`
**Propósito**: Registrar observación en el CRM.

**Parámetros**:
- `observation`: Objeto Observation con tipo y mensaje

**Flujo**:
1. Click en lista de tipos de interacción
2. Seleccionar tipo de observación (xpath del objeto)
3. Escribir mensaje en textarea
4. Click en botón "Agregar Observación"
5. Esperar que el loader desaparezca

**Tipos de Observación**:
- `nota`: Notas generales
- `llamada`: Registro de llamadas
- `whatsapp`: Mensajes de WhatsApp
- `email`: Correos enviados
- `personal`: Visitas personales

---

### 3. customFunctions.py (161 líneas)

Biblioteca de funciones utilitarias.

#### Funciones Principales:

##### `formatPhoneNumber(phoneNumber)`
**Propósito**: Normalizar números telefónicos a formato internacional.

**Formatos Soportados**:
```
096-905-8836        → +593969058836
0969058836          → +593969058836
+593969058836       → +593969058836  (sin cambios)
+5930969058836      → +593969058836  (corrige error de 0 extra)
+593 99 493 8897    → +593994938897  (elimina espacios)
```

**Lógica**:
1. Eliminar guiones, espacios y trim
2. Si tiene '+' y 13 caracteres → OK
3. Si tiene '+' y 14 caracteres → Eliminar 0 extra
4. Si tiene 10 caracteres → Agregar +593 y quitar primer 0
5. Otro caso → `None` (número inválido)

---

##### `validDateforContinue(date, days)`
**Propósito**: Validar si un cliente requiere seguimiento.

**Parámetros**:
- `date`: Fecha de último contacto (formato "YYYY-MM-DD")
- `days`: Días de espera antes de seguimiento

**Lógica**:
```python
curentDate = datetime.now()
dateLastContact = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=days)
return dateLastContact <= curentDate
```

**Ejemplo**:
- Último contacto: 2023-01-01
- Días de espera: 15
- Fecha objetivo: 2023-01-16
- Hoy: 2023-01-20
- Resultado: `True` (ya pasaron más de 15 días)

---

##### `addDays(daysAdded)`
**Propósito**: Calcular fecha futura desde hoy.

**Parámetro**:
- `daysAdded`: Número de días a agregar

**Retorno**: String con fecha en formato "YYYY-MM-DD"

**Uso**:
```python
scheduleTask(browser, 'Seguimiento', addDays(14))
```

---

##### `allImagesSent(numberOfImagesSent, numberOfElements, positionMessagesContainer)`
**Propósito**: Custom Expected Condition para Selenium que verifica entrega de imágenes.

**Parámetros**:
- `numberOfImagesSent`: Cantidad de archivos enviados
- `numberOfElements`: Total de mensajes en el chat
- `positionMessagesContainer`: Posición del contenedor de mensajes (2 o 3)

**Retorna**: Función `_predicate(driver)` que Selenium evalúa repetidamente

**Lógica Interna**:
1. Itera sobre los últimos N mensajes (N = imágenes enviadas)
2. Para cada mensaje, busca el span con atributo `aria-label`
3. Verifica que contenga "Enviado" o "Entregado"
4. Si todos los mensajes están entregados → `True`
5. Si alguno falta o hay error → `False`

**XPath Dinámico**:
```python
xpath = '//*[@id="main"]/div[2]/div/div[2]/div[%s]/div[%s]/div/div/div[1]/div[1]/div/div[2]/div/div/span'
       %(positionMessagesContainer, numberOfElements - i)
```

---

##### `resource_path(relative_path)`
**Propósito**: Resolver rutas de recursos para PyInstaller.

**Problema**:
- En desarrollo: Archivos están en estructura de carpetas normal
- En ejecutable (.exe): PyInstaller extrae archivos a carpeta temporal `_MEIPASS`

**Solución**:
```python
try:
    base_path = sys._MEIPASS  # Ruta temporal de PyInstaller
except Exception:
    base_path = os.path.abspath(".")  # Ruta actual en desarrollo
return os.path.join(base_path, relative_path)
```

**Uso**:
```python
load_dotenv(dotenv_path=cf.resource_path('.env'))
driver_service = Service(executable_path=cf.resource_path('chromedriver.exe'))
```

---

### 4. ProjectXPath.py

**Propósito**: Configuración centralizada por proyecto.

#### Clase `XPathByProject`

**Atributos**:
```python
self.name           # Nombre del proyecto
self.email          # Email de login
self.password       # Contraseña del proyecto
self.srcLogo        # URL del logo (validación de sesión)
self.folder         # Diccionario de campaña → carpeta (solo Trivo)
self.LI_seguimientoInfoInicialEnviada  # XPath específico
```

**Mapeo de Campañas (Trivo)**:
```python
self.folder = {
    "Campaña Diamond Garden": "DIAMOND GARDEN",
    "Campaña Foret": "APARTAT",
    "Campaña U&S": "BOTANIQO",
    "Estrella X": "DISTRICT",
    "Oribugardens": "IBAGARI",
    "Campaña AB - Orizzonte": "IBAGARI",
    "Lombardi": "MAGIC",
    "Campaña Bentho": "MAGIC",
    "Campaña Terralta": "TERRALTA"
}
```

**Método `getFolder(projectName)`**:
```python
def getFolder(self, projectName):
    if self.folder == None:
        return self.name  # Lucia o Promonsa
    else:
        try:
            folder = self.folder[projectName]
        except KeyError:
            return "NATIVA"  # Campaña por defecto
        return folder
```

**Uso en doTracktoCustomer**:
```python
folderRelativeImages = 'Trivo\\%s' %(xpathDictionary.getFolder(campania))
                       if xpathDictionary.name=="Trivo"
                       else xpathDictionary.name
```

---

### 5. Observation.py

**Propósito**: Modelo de datos para observaciones del CRM.

```python
class Observation:
    def __init__(self, tipo, mensaje):
        self.tipo = tipo
        self.message = mensaje
        self.xpath = self.getXPath(tipo)

    def getXPath(self, tipo):
        opciones = {
            "nota": '//*[@id="menu-"]/div[2]/ul/li[1]',
            "llamada": '//*[@id="menu-"]/div[2]/ul/li[2]',
            "whatsapp": '//*[@id="menu-"]/div[2]/ul/li[3]',
            "email": '//*[@id="menu-"]/div[2]/ul/li[4]',
            "personal": '//*[@id="menu-"]/div[2]/ul/li[5]'
        }
        return opciones[tipo]
```

**Ejemplo de Uso**:
```python
observations = [
    Observation("nota", 'Seguimiento.'),
    Observation("whatsapp", 'Video de Diamond Garden'),
    Observation("whatsapp", 'Imagen de Diamond Garden'),
    Observation("nota", 'Esperando contestación.')
]

for observation in observations:
    fillObservations(browser, observation)
```

---

## Flujo de Trabajo

### Flujo General del Robot

```
┌─────────────────────────────────────────────────┐
│ 1. INICIO                                       │
│    - Solicitar contraseña                       │
│    - Seleccionar proyecto (1=Lucia, 2=Trivo,    │
│      3=Promonsa)                                │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 2. AUTENTICACIÓN                                │
│    - Navegar a admin.trivo.com.ec/login/{proj}  │
│    - Verificar sesión existente                 │
│    - Login si es necesario                      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 3. PREPARACIÓN DE TABLA                         │
│    - Ordenar por "Fecha Último Contacto"        │
│    - Doble click en header (más antiguo primero)│
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 4. SELECCIÓN DE CLIENTE                         │
│    - Buscar primer cliente con fecha válida     │
│    - Saltar clientes nuevos (fecha = "-")       │
│    - Obtener XPath del cliente                  │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 5. EXTRACCIÓN DE DATOS                          │
│    - Click en botón editar cliente              │
│    - Esperar carga de formulario                │
│    - Extraer: nombre, teléfono, campaña         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 6. NAVEGACIÓN DE FORMULARIO                     │
│    - Click en "Siguientes Acciones"             │
│    - Seleccionar "Seguimiento - Info Enviada"   │
│    - Copiar mensaje generado por CRM            │
│    - Personalizar con nombre del cliente        │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 7. ENVÍO POR WHATSAPP                           │
│    - Abrir WhatsApp Web en nueva pestaña        │
│    - Formatear número telefónico                │
│    - Enviar mensajes personalizados             │
│    - Adjuntar imágenes/videos (máx. 3)          │
│    - Verificar entrega                          │
│    - Cerrar pestaña de WhatsApp                 │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 8. AGENDAMIENTO DE TAREA                        │
│    - Click en botón "Nueva Tarea"               │
│    - Título: "Seguimiento"                      │
│    - Fecha: 14 + random(0-4) días               │
│    - Confirmar agendamiento                     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 9. REGISTRO DE OBSERVACIONES                    │
│    - Regresar a formulario del cliente          │
│    - Agregar observación: "Seguimiento."        │
│    - Agregar: "Video de {Proyecto}"  (si aplica)│
│    - Agregar: "Imagen de {Proyecto}" (si aplica)│
│    - Agregar: "Esperando contestación."         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 10. RETORNO A TABLA                             │
│     - Click en botón regresar                   │
│     - Esperar carga de tabla de clientes        │
│     - LOOP → Volver al paso 4                   │
└─────────────────────────────────────────────────┘
```

### Flujo Detallado de `sendInfoWhatsApp()`

```
┌─────────────────────────────────────────────────┐
│ INPUT: phone, messages[], dirImages             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 1. Formatear número telefónico                  │
│    - Eliminar espacios y guiones                │
│    - Convertir a formato +593XXXXXXXXX          │
│    - Validar formato correcto                   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 2. Abrir WhatsApp Web                           │
│    URL: https://web.whatsapp.com/send?          │
│         l=es&phone=593XXXXXXXXX&text=           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 3. Esperar Carga (timeout: 60s)                 │
│    VALIDAR UNO DE:                              │
│    A) Popup "Número Inválido" → ERROR           │
│    B) Caja de texto visible + popup carga gone  │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │ ¿ERROR?           │
        │ (número inválido) │
        └───┬───────────┬───┘
          SI│           │NO
            ▼           ▼
    ┌──────────┐   ┌─────────────────────────┐
    │ ABORTAR  │   │ 4. Enviar Mensajes      │
    │ return   │   │    FOR msg in messages: │
    │ False    │   │      - send_keys(msg)   │
    └──────────┘   │      - ENTER            │
                   │      - sleep(2s)        │
                   └─────────┬───────────────┘
                             │
                             ▼
                   ┌─────────────────────────┐
                   │ 5. Adjuntar Archivos    │
                   │    - Click botón clip   │
                   │    - Esperar input file │
                   │    - Enviar paths       │
                   │    - Click enviar       │
                   └─────────┬───────────────┘
                             │
                             ▼
                   ┌─────────────────────────┐
                   │ 6. Verificar Entrega    │
                   │    FOR cada imagen:     │
                   │      - Buscar span      │
                   │      - Leer aria-label  │
                   │      - Validar estado   │
                   └─────────┬───────────────┘
                             │
                   ┌─────────┴─────────┐
                   │ ¿TODOS ENVIADOS?  │
                   └───┬───────────┬───┘
                     SI│           │NO
                       ▼           ▼
              ┌────────────┐  ┌────────────┐
              │ 7. ÉXITO   │  │ 7. ERROR   │
              │ Cerrar tab │  │ Cerrar tab │
              │ return True│  │ return Flse│
              └────────────┘  └────────────┘
```

---

## Configuración de Proyectos

### Lucia

**Características**:
- Seguimiento cada **50 días**
- Carpeta de recursos: `C:\Users\<User>\CRM\Lucia\`
- XPath específico: `//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]`
- Logo: `https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1635263729281-lg.png`

**Configuración**:
```python
xpathDictionary = XPathByProject('lucia')
```

---

### Trivo

**Características**:
- Seguimiento cada **15 días**
- Múltiples sub-campañas con carpetas específicas
- Carpeta base: `C:\Users\<User>\CRM\Trivo\`
- XPath específico: `//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[35]`
- Logo: `https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1585002874423-lg.png`

**Mapeo de Campañas**:
| Campaña en CRM | Carpeta de Recursos |
|----------------|---------------------|
| Campaña Diamond Garden | DIAMOND GARDEN |
| Campaña Foret | APARTAT |
| Campaña U&S | BOTANIQO |
| Estrella X | DISTRICT |
| Oribugardens | IBAGARI |
| Campaña AB - Orizzonte | IBAGARI |
| Lombardi | MAGIC |
| Campaña Bentho | MAGIC |
| Campaña Terralta | TERRALTA |
| Otras campañas | NATIVA (default) |

**Configuración**:
```python
xpathDictionary = XPathByProject('trivo')
folder = xpathDictionary.getFolder("Campaña Diamond Garden")  # → "DIAMOND GARDEN"
```

---

### Promonsa

**Características**:
- Seguimiento cada **50 días**
- Carpeta de recursos: `C:\Users\<User>\CRM\Promonsa\`
- XPath específico: `//*[@id="menu-Enviar whatsapp"]/div[2]/ul/li[3]`
- Logo: `https://s3.us-east-2.amazonaws.com/media.trivo.com.ec/Companies/1615475557832-lg.png`

**Configuración**:
```python
xpathDictionary = XPathByProject('promonsa')
```

---

## Guía de Uso

### Uso desde Código Fuente

```bash
# 1. Activar entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env (ver sección Instalación)

# 4. Preparar carpetas de recursos con imágenes/videos

# 5. Ejecutar
python main.py
```

**Interacción**:
```
CONTRASEÑA:
[ingresar contraseña definida en .env]

JELOU, A CUAL PROYECTO DESEAS HACER SEGUIMIENTO?
Opcion 1: Lucia
Opcion 2: Trivo
Opcion 3: Promonsa
[ingresar número de opción]
```

---

### Uso del Ejecutable

```bash
# 1. Navegar a la carpeta output/
cd output

# 2. Ejecutar main.exe
main.exe
```

**Nota**: El ejecutable incluye todas las dependencias excepto ChromeDriver, que debe estar en la misma carpeta.

---

### Compilar a Ejecutable

```bash
# Instalar auto-py-to-exe
pip install auto-py-to-exe

# Ejecutar GUI
auto-py-to-exe

# Configuración recomendada:
# - Script: main.py
# - Onefile: Yes
# - Console: Console Based
# - Icon: (opcional)
# - Additional Files:
#     chromedriver.exe
#     .env
```

**Alternativa con PyInstaller directo**:
```bash
pyinstaller --onefile --add-data ".env;." --add-data "chromedriver.exe;." main.py
```

---

## Detalles Técnicos

### Gestión de Sesiones de Chrome

El robot utiliza el perfil de usuario de Chrome para mantener sesiones persistentes:

```python
userdata = '%s\\AppData\\Local\\Google\\Chrome\\User Data' %(os.path.expanduser("~"))
options.add_argument('--user-data-dir=%s' % (userdata))
```

**Consideraciones**:
- Solo funciona si Chrome no está abierto
- Si Chrome está abierto, usar perfil temporal o cerrar Chrome primero

---