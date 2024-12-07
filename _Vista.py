from PyQt6.QtWidgets import QTableWidgetItem, QVBoxLayout, QMainWindow, QDialog, QFileDialog,QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pydicom
import os
import numpy as np
import math
import scipy.io as sio
from scipy.io import loadmat
from PyQt6.QtCore import Qt
  

###################

# Clase personalizada para visualizar un eje sagital en una figura de Matplotlib
class Eje_sagital(FigureCanvas):
    def __init__(self, parent, archivo, carpeta, numero):
        """
        Constructor de la clase Eje_sagital. Configura el lienzo de Matplotlib y llama al método para mostrar la imagen.

        Args:
        - parent: Referencia al widget padre.
        - archivo: Archivo DICOM a procesar (no parece usarse en el método actual).
        - carpeta: Carpeta donde están los archivos DICOM.
        - numero: Índice de la imagen que se mostrará en el eje sagital.
        """
        # Inicializa la clase base FigureCanvas con un objeto Figure
        super().__init__(Figure())
        
        # Establece el widget padre
        self.setParent(parent)
        
        # Crea un eje dentro de la figura para visualizar la imagen
        self.ax = self.figure.add_subplot(111)
        
        # Almacena el número de la imagen que se desea mostrar
        self.numero_imagen = numero

        # Llama al método para cargar y mostrar la imagen desde la carpeta
        self.mostrar_en_qt(archivo, carpeta)

    def mostrar_en_qt(self, archivo_dicom, carpeta):
        """
        Carga un conjunto de archivos DICOM desde una carpeta, crea un volumen 3D
        y visualiza una imagen específica en el plano sagital.

        Args:
        - archivo_dicom: No se utiliza en el método actual.
        - carpeta: Ruta de la carpeta donde están los archivos DICOM.
        """
        # Carga todos los archivos DICOM de la carpeta en una lista
        slices = [pydicom.dcmread(carpeta + '/' + s) for s in os.listdir(carpeta)]
        
        # Ordena las imágenes DICOM por la posición del paciente en el eje X
        # Esto es crucial para garantizar la correcta alineación del volumen 3D
        slices.sort(key=lambda x: int(x.ImagePositionPatient[0]))
        
        # Crea un volumen 3D apilando los datos de píxeles de todas las imágenes
        volumen = np.stack([s.pixel_array for s in slices])
        
        # Convierte los valores del volumen a tipo int16 para normalizar los datos
        volumen = volumen.astype(np.int16)

        # Muestra la imagen correspondiente al índice `numero_imagen` en el eje Axes
        self.ax.imshow(volumen[self.numero_imagen - 1, :, :], cmap="gray", aspect='auto') 
        
        # Oculta los ejes del gráfico para mejorar la visualización
        self.ax.axis('off')
        
        # Ajusta el objeto Axes para ocupar todo el espacio del lienzo
        self.ax.set_position([0, 0, 1, 1])
        
        # Redibuja la figura para reflejar los cambios
        self.draw()


class Eje_coronal(FigureCanvas):
    def __init__(self, parent, archivo, carpeta, numero):
        """
        Constructor de la clase para inicializar un corte coronal.
        """
        super().__init__(Figure())
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)  # Configura un eje único para la visualización.
        self.numero_imagen = numero  # Índice del corte coronal.
        self.mostrar_en_qt(archivo, carpeta)  # Llama al método para mostrar la imagen.

    def mostrar_en_qt(self, archivo_dicom, carpeta):
        """
        Carga imágenes DICOM desde una carpeta, calcula proporciones espaciales y visualiza un corte coronal.

        Args:
        - archivo_dicom: No se utiliza aquí.
        - carpeta: Ruta de la carpeta que contiene las imágenes DICOM.
        """
        # Carga y ordena las imágenes DICOM en función de su posición en el eje X.
        slices = [pydicom.dcmread(carpeta + '/' + s) for s in os.listdir(carpeta)]
        slices.sort(key=lambda x: int(x.ImagePositionPatient[0]))
        
        # Calcula las proporciones entre el espaciado de píxeles y el grosor de los cortes.
        pixel_spacing = slices[0].PixelSpacing
        slice_thickness = slices[0].SliceThickness
        proporcion_filas = float(slice_thickness) / float(pixel_spacing[1])
        proporcion_columnas = float(slice_thickness) / float(pixel_spacing[0])
        proporciones = (proporcion_filas, proporcion_columnas)
        
        # Convierte las proporciones a enteros para su uso en índices.
        valores = tuple(int(math.floor(coord)) for coord in proporciones)
        
        # Crea un volumen tridimensional a partir de las imágenes.
        volumen = np.stack([s.pixel_array for s in slices]).astype(np.int16)
        
        # Calcula la posición del corte coronal en el volumen.
        valor = (self.numero_imagen - 1) * valores[0]
        
        # Muestra el corte coronal correspondiente.
        self.ax.imshow(volumen[:, :, valor], cmap="gray", aspect="auto")
        self.ax.axis('off')  # Oculta los ejes para una visualización limpia.
        self.ax.set_position([0, 0, 1, 1])  # Configura el eje para ocupar todo el lienzo.
        self.draw()  # Redibuja la figura.
  
        
class Eje_axial(FigureCanvas):
    def __init__(self, parent, archivo, carpeta, numero):
        """
        Constructor de la clase para inicializar un corte axial.
        """
        super().__init__(Figure())
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)  # Configura un eje único para la visualización.
        self.numero_imagen = numero  # Índice del corte axial.
        self.mostrar_en_qt(archivo, carpeta)  # Llama al método para mostrar la imagen.

    def mostrar_en_qt(self, archivo_dicom, carpeta):
        """
        Carga imágenes DICOM desde una carpeta, calcula proporciones espaciales y visualiza un corte axial.

        Args:
        - archivo_dicom: No se utiliza aquí.
        - carpeta: Ruta de la carpeta que contiene las imágenes DICOM.
        """
        # Carga y ordena las imágenes DICOM en función de su posición en el eje X.
        slices = [pydicom.dcmread(carpeta + '/' + s) for s in os.listdir(carpeta)]
        slices.sort(key=lambda x: int(x.ImagePositionPatient[0]))
        
        # Calcula las proporciones entre el espaciado de píxeles y el grosor de los cortes.
        pixel_spacing = slices[0].PixelSpacing
        slice_thickness = slices[0].SliceThickness
        proporcion_filas = float(slice_thickness) / float(pixel_spacing[1])
        proporcion_columnas = float(slice_thickness) / float(pixel_spacing[0])
        proporciones = (proporcion_filas, proporcion_columnas)
        
        # Convierte las proporciones a enteros para su uso en índices.
        valores = tuple(int(math.floor(coord)) for coord in proporciones)
        
        # Crea un volumen tridimensional a partir de las imágenes.
        volumen = np.stack([s.pixel_array for s in slices]).astype(np.int16)
        
        # Calcula la posición del corte axial en el volumen.
        valor = (self.numero_imagen - 1) * valores[0]
        
        # Muestra el corte axial correspondiente.
        self.ax.imshow(volumen[:, valor, :], cmap="gray", aspect="auto")
        self.ax.axis('off')  # Oculta los ejes para una visualización limpia.
        self.ax.set_position([0, 0, 1, 1])  # Configura el eje para ocupar todo el lienzo.
        self.draw()  # Redibuja la figura.
  
        
        
class VentanaInicial(QDialog): #padre QDIalog, esto es una herencia
    """
    QDialog es una clase de PyQt (parte del módulo PyQt6.QtWidgets) que se utiliza para crear ventanas de diálogo en aplicaciones gráficas. Los diálogos son ventanas secundarias que suelen usarse para interactuar con el usuario o mostrar información adicional sin necesidad de interrumpir la aplicación principal.

    """
    
    def __init__(self, ppal=None):
        """
        Constructor de la ventana inicial.
        """
        super().__init__(ppal)  #super es llamar al padre que es QDialog
        loadUi("ventana_inicial.ui", self)  # Carga el diseño desde un archivo `.ui`.
        
        self.setWindowTitle("MED-ANALYZE")  # Establece el título de la ventana.
        self.setup()  # Configura los elementos interactivos.

    def setControlador(self, c):
        """
        Asigna un controlador para gestionar la lógica de la ventana.
        """
        self._controlador = c

    def setup(self):
        """
        Configura los eventos iniciales de la ventana.
        
        """
        #QT maneja señales y conexiones
        # las señales signals son los eventos como hacer click, como presionar una tecla
        # el connect es la conexión a una señal especfícica
        # en este caso , la señal es al dar clic al boton iniciar
        # el connect revise esa señal, y llama a la función iniciar_programa
        self.iniciar.clicked.connect(self.iniciar_programa)  # Conecta el botón "iniciar" a su método correspondiente.

    def iniciar_programa(self):
        """
        Cambia a la ventana de inicio de sesión y oculta la ventana actual.
        """
        v_login = VentanaLogin(self._controlador, self)
        self.hide()  # Oculta la ventana actual.
        v_login.show()  # Muestra la ventana de inicio de sesión.

class VentanaLogin(QDialog): #padre QDIalog, esto es una herencia
    """
    QDialog es una clase de PyQt (parte del módulo PyQt6.QtWidgets) que se utiliza para crear ventanas de diálogo en aplicaciones gráficas. Los diálogos son ventanas secundarias que suelen usarse para interactuar con el usuario o mostrar información adicional sin necesidad de interrumpir la aplicación principal.

    """
    def __init__(self, c, ppal=None):
        """
        Constructor de la clase VentanaLogin.

        Args:
        - c: Controlador para manejar la lógica del login.
        - ppal: Referencia opcional a la ventana principal.
        """
        super().__init__(ppal)
        loadUi("ventana_login.ui", self)  # Carga el diseño desde un archivo .ui.
        self.setWindowTitle("Inicio de sesión")  # Título de la ventana.
        self._controlador = c  # Asigna el controlador.
        self.setup()  # Configura los elementos interactivos.

    def setup(self):
        """
        Conecta los botones de la ventana con las acciones correspondientes.
        recibe una señal el connect, de tipo accepted o rejected
        """
        self.buttonBox.accepted.connect(self.opcion_aceptar)  # Acción para el botón "Aceptar".
        self.buttonBox.rejected.connect(self.opcion_rechazar)  # Acción para el botón "Cancelar".

    def opcion_aceptar(self):
        """
        Valida las credenciales de inicio de sesión.
        """
        usuario = self.user.text()  # Obtiene el texto ingresado en el campo de usuario.
        password = self.passw.text()  # Obtiene el texto ingresado en el campo de contraseña.

        validacion = self._controlador.validar_login(usuario, password)  # Llama al controlador para validar.

        if validacion: #si es verdadero o True
            # Muestra un mensaje de bienvenida si las credenciales son correctas.
            text = "¡Bienvenido al programa!"
            #atributos de MessageBox, Login es el titulo, text es el titulo de la caja
            # y QMessageBox.StandardButton.Ok es el botón que tiene la caja
            QMessageBox.information(self, "Login", text, QMessageBox.StandardButton.Ok)

            # Cambia a la ventana del menú principal.
            self.abrir_ventana_menu()
            self.user.setText("")  # Limpia el campo de usuario.
            self.passw.setText("")  # Limpia el campo de contraseña.
        else:
            # Muestra un mensaje de error si las credenciales son incorrectas.
            text = "¡Datos de acceso incorrectos!"
            QMessageBox.warning(self, "Alerta", text, QMessageBox.StandardButton.Ok)

    def opcion_rechazar(self):
        """
        Limpia los campos de texto y cancela la operación.
        """
        self.user.setText("")  # Limpia el campo de usuario.
        self.passw.setText("")  # Limpia el campo de contraseña.

    def abrir_ventana_menu(self):
        """
        Abre la ventana del menú principal y oculta la ventana de login.
        """
        v_menu = VentanaMenu(self)  # Instancia la ventana del menú.
        self.hide()  # Oculta la ventana actual.
        v_menu.show()  # Muestra la ventana del menú.

        
        
class VentanaMenu(QDialog):
    def __init__(self, ppal=None):
        """
        Constructor de la clase VentanaMenu.

        Args:
        - ppal: Referencia opcional a la ventana principal.
        """
        super().__init__(ppal)
        loadUi("ventana_menu.ui", self)  # Carga el diseño desde un archivo .ui.
        self.setWindowTitle("Menú principal")  # Título de la ventana.
        self.__ventanaprincipal = ppal  # Guarda la referencia a la ventana principal.
        self.setup()  # Configura los elementos interactivos.

    def setup(self):
        """
        Conecta los botones de la ventana con las acciones correspondientes.
        """
        self.img_med.clicked.connect(self.mostrar_imgmed)  # Acción para visualizar imágenes médicas.
        self.cont.clicked.connect(self.mostrar_cont)  # Acción para visualizar contenido multimedia.
        self.sen_fis.clicked.connect(self.mostrar_senfis)  # Acción para abrir señales fisiológicas.
        self.cerrar.clicked.connect(self.mostrar_inicio)  # Acción para cerrar sesión.

    def mostrar_imgmed(self):
        """
        Abre una ventana para visualizar imágenes médicas DICOM.
        """
        

        # Abrir un cuadro de diálogo para que el usuario seleccione una carpeta
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        
        """
        QFileDialog.getExistingDirectory:

Este método de la clase QFileDialog muestra un cuadro de diálogo que permite al usuario seleccionar un directorio (carpeta) desde su sistema de archivos.
self: Es una referencia al objeto actual (en este caso, probablemente una ventana o widget). Este parámetro es necesario para el cuadro de diálogo, ya que indica cuál es la ventana principal de la aplicación.
"Seleccionar Carpeta": Es el título que aparecerá en la ventana del cuadro de diálogo.
"/ruta/inicial": Es la ruta inicial donde se abre el cuadro de diálogo. Es una ruta predeterminada que se mostrará cuando el usuario abra el diálogo, pero el usuario podrá navegar a otras carpetas si lo desea.
El valor que devuelve getExistingDirectory es la ruta completa de la carpeta seleccionada por el usuario. Si el usuario cancela la selección, el valor devuelto será una cadena vacía ("").
        """
        
        # Filtrar los archivos de la carpeta seleccionada para obtener solo los archivos que terminan en '.dcm'
        archivos_dicom = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.dcm')]
        """
        os.listdir(carpeta):

Este método de la librería os devuelve una lista con todos los nombres de archivos y subdirectorios presentes dentro de la carpeta seleccionada (almacenada en la variable carpeta).

archivo for archivo in os.listdir(carpeta) if archivo.endswith('.dcm')

Se está usando una lista por comprensión para crear una nueva lista que contiene solo los archivos que tienen la extensión .dcm.

archivo.endswith('.dcm'): Esta condición verifica si el nombre del archivo termina con la extensión .dcm. La función endswith() devuelve True si el nombre del archivo tiene esta extensión y False si no.

Resultado: La lista archivos_dicom contendrá solo los archivos que tengan la extensión .dcm (comúnmente utilizados para imágenes médicas en formato DICOM). Estos archivos serán los que se utilizarán más adelante en el programa.
        """


        if not archivos_dicom:
            # Muestra un mensaje si no se encuentran archivos DICOM.
            text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
        else:
            # Abre la ventana para mostrar imágenes médicas.
            v_imgmed = Ventana_imgmed(archivos_dicom, carpeta, self.__ventanaprincipal, self)
            self.hide()  # Oculta la ventana actual.
            v_imgmed.show()  # Muestra la ventana de imágenes médicas.

    def mostrar_cont(self):
        """
        Abre una ventana para visualizar contenido multimedia (imágenes .jpg o .png).
        """
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        lista_archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(('.jpg', '.png'))]

        if not lista_archivos:
            # Muestra un mensaje si no se encuentran archivos multimedia.
            text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
        else:
            # Abre la ventana para mostrar el contenido multimedia.
            v_cont = VentanaCont(lista_archivos, carpeta, self.__ventanaprincipal, self)
            self.hide()  # Oculta la ventana actual.
            v_cont.show()  # Muestra la ventana de contenido.

    def mostrar_senfis(self):
        """
        Abre una ventana para cargar y visualizar señales fisiológicas desde un archivo .mat.
        """
        try:
            mat, _ = QFileDialog.getOpenFileName(self, "Abrir señal", "", "Todos los archivos (*);;Archivos mat (*.mat);;Python (*.py)")

            if not mat.endswith('.mat'):
                # Muestra un mensaje si el archivo seleccionado no es válido.
                text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
                QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
            else:
                # Abre la ventana para mostrar señales fisiológicas.
                v_senfis = Ventana_senfis(mat, self.__ventanaprincipal, self)
                self.hide()  # Oculta la ventana actual.
                v_senfis.show()  # Muestra la ventana de señales fisiológicas.

        except FileNotFoundError:
            # Muestra un mensaje si ocurre un error al buscar el archivo.
            text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)

    def mostrar_inicio(self):
        """
        Cierra sesión y regresa a la ventana inicial.
        """
        text = "¿Está seguro que desea cerrar sesión?"
        message = QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if message == QMessageBox.StandardButton.Yes:
            self.close()  # Cierra la ventana actual.
            self.__ventanaprincipal.show()  # Muestra la ventana principal.
       
# Clase para la ventana de inicio de sesión
class VentanaLogin(QDialog):
    def __init__(self, c, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_login.ui", self)  # Carga el diseño de la interfaz desde un archivo .ui
        self.setWindowTitle("Inicio de sesión")
        self._controlador = c  # Controlador para manejar la lógica de negocio
        self.setup()
        
    def setup(self):
        # Conexión de los botones de aceptar y cancelar a sus métodos correspondientes
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_rechazar)
        
    def opcion_aceptar(self):
        usuario = self.user.text()  # Obtiene el texto del campo de usuario
        password = self.passw.text()  # Obtiene el texto del campo de contraseña
        validacion = self._controlador.validar_login(usuario, password)  # Valida las credenciales
        
        if validacion:
            # Si las credenciales son correctas, muestra un mensaje de bienvenida
            text = "¡Bienvenido al programa!"
            QMessageBox.information(self, "Login", text, QMessageBox.StandardButton.Ok)
            # Abre la ventana del menú principal
            self.abrir_ventana_menu()
            # Limpia los campos de usuario y contraseña
            self.user.setText("")
            self.passw.setText("")
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            text = "¡Datos de acceso incorrectos!"
            QMessageBox.warning(self, "Alerta", text, QMessageBox.StandardButton.Ok)
            
    def opcion_rechazar(self):
        # Limpia los campos de texto al cancelar
        self.user.setText("")
        self.passw.setText("")
        
    def abrir_ventana_menu(self):
        # Abre la ventana del menú principal
        v_menu = VentanaMenu(self)
        self.hide()  # Oculta la ventana actual
        v_menu.show()
        

# Clase para el menú principal
class VentanaMenu(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_menu.ui", self)  # Carga la interfaz desde un archivo .ui
        self.setWindowTitle("Menú principal")
        self.__ventanaprincipal = ppal
        self.setup()
        
    def setup(self):
        # Conecta los botones del menú a sus métodos correspondientes
        self.img_med.clicked.connect(self.mostrar_imgmed)
        self.cont.clicked.connect(self.mostrar_cont)
        self.sen_fis.clicked.connect(self.mostrar_senfis)
        self.cerrar.clicked.connect(self.mostrar_inicio)
        
    def mostrar_imgmed(self):
        # Abre un cuadro de diálogo para seleccionar una carpeta
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        # Filtra los archivos con extensión .dcm
        archivos_dicom = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.dcm')]
        
        if not archivos_dicom:
            # Muestra un mensaje de error si no se encuentran archivos DICOM
            text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
        else:
            # Abre la ventana para procesar imágenes médicas
            v_imgmed = Ventana_imgmed(archivos_dicom, carpeta, self.__ventanaprincipal, self)
            self.hide()
            v_imgmed.show()
            
    def mostrar_cont(self):
        # Similar al método anterior, pero para imágenes comunes (.jpg, .png)
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        lista_archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(('.jpg', '.png'))]
        
        if not lista_archivos:
            text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
        else:
            # Abre la ventana para procesar imágenes generales
            v_cont = VentanaCont(lista_archivos, carpeta, self.__ventanaprincipal, self)
            self.hide()
            v_cont.show()
            
    def mostrar_senfis(self):
        # Abre un cuadro de diálogo para seleccionar un archivo .mat
        try:
            mat, _ = QFileDialog.getOpenFileName(self, "Abrir señal", "", "Todos los archivos (*);;Archivos mat (*.mat);;Python (*.py)")
            
            if not mat.endswith('.mat'):
                # Muestra un mensaje de error si el archivo no es un .mat válido
                text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo"
                QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
            else:
                # Abre la ventana para procesar señales físicas
                v_senfis = Ventana_senfis(mat, self.__ventanaprincipal, self)
                self.hide()
                v_senfis.show()
        except FileNotFoundError:
            # Manejo de errores si no se selecciona ningún archivo
            text = "No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
    
    def mostrar_inicio(self):
        # Pregunta al usuario si desea cerrar sesión
        text = "¿Está seguro que desea cerrar sesión?"
        message = QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if message == QMessageBox.StandardButton.Yes:
            self.close()
            self.__ventanaprincipal.show()

# Clase que representa una ventana de imágenes médicas, hereda de QDialog para crear una ventana de diálogo
class Ventana_imgmed(QDialog):   
    def __init__(self, archivos, carpeta, ppal=None, sec= None):
        super().__init__(ppal)  # Llama al constructor de la clase QDialog (ventana base)
        
        # Carga la interfaz de usuario desde un archivo .ui
        loadUi("ventana_imgmed.ui", self)    
        
        # Configura el título de la ventana
        self.setWindowTitle("Imágenes Médicas")
        
        # Asigna los parámetros de las ventanas principales y secundarias
        self.__ventanaprincipal = ppal
        self.__ventanaSec = sec
        
        # Asigna las listas de archivos y carpeta seleccionada
        self.archivos = archivos
        self.carpeta = carpeta
        
        # Configura el valor inicial del texto del valor actual (indicación del valor del slider)
        self.valor_actual.setText("1")
        
        # Llama a la función setup para inicializar componentes y comportamientos
        self.setup()
        
        # Inicializa la visualización de los tres ejes de las imágenes médicas
        self.graficar_eje_sag()
        self.graficar_eje_co()
        self.graficar_eje_ax()

    # Configura los controles y comportamientos de la ventana
    def setup(self):
        # Conecta el botón de cerrar con la función que muestra la ventana de inicio
        self.cerrar.clicked.connect(self.mostrar_inicio)
        
        # Conecta el botón de volver al menú principal con la función 'menu'
        self.volver.clicked.connect(self.menu)
        
        # Establece los valores mínimo y máximo del slider (barra deslizante) para navegar entre los archivos
        self.slider.setMinimum(1)
        self.slider.setMaximum(len(self.archivos))
        
        # Establece el valor inicial del slider en 1 (el primer archivo)
        self.slider.setValue(1)
        
        # Conecta el cambio de valor del slider con la función que actualiza la visualización
        self.slider.valueChanged.connect(self.ver_valor)
        
        # Conecta el botón de información a la función que abre la ventana de detalles
        self.info_im.clicked.connect(self.abrir_info)
        
        # Conecta el cambio de valor del slider con las funciones que actualizan los ejes de las imágenes
        self.slider.valueChanged.connect(self.graficar_eje_sag)
        self.slider.valueChanged.connect(self.graficar_eje_co)
        self.slider.valueChanged.connect(self.graficar_eje_ax)
        
        # Establece el texto que muestra el valor máximo (el número total de archivos)
        self.valor_maximo.setText(str(len(self.archivos)))

    # Función que maneja la actualización del gráfico del eje sagital
    def graficar_eje_sag(self):
        # Si ya existe un layout (diseño), lo toma, si no, crea uno nuevo (QVBoxLayout es un diseño vertical)
        layout = self.eje_sagital.layout() or QVBoxLayout()
        
        # Limpia todos los widgets (elementos) del layout actual
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Crea el gráfico para el eje sagital, usando la clase Eje_sagital, y lo agrega al layout
        self.grafico = Eje_sagital(self.eje_sagital, self.archivos, self.carpeta, self.slider.value())
        layout.addWidget(self.grafico)

        # Establece el layout con el gráfico actualizado
        self.eje_sagital.setLayout(layout)

    # Función que maneja la actualización del gráfico del eje coronal
    def graficar_eje_co(self):
        layout = self.eje_coronal.layout() or QVBoxLayout()

        # Limpia todos los widgets del layout actual
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Crea el gráfico para el eje coronal y lo agrega al layout
        self.grafico = Eje_coronal(self.eje_coronal, self.archivos, self.carpeta, self.slider.value())
        layout.addWidget(self.grafico)

        # Establece el layout con el gráfico actualizado
        self.eje_coronal.setLayout(layout)

    # Función que maneja la actualización del gráfico del eje axial
    def graficar_eje_ax(self):
        layout = self.eje_axial.layout() or QVBoxLayout()
    
        # Limpia todos los widgets del layout actual
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Crea el gráfico para el eje axial y lo agrega al layout
        self.grafico = Eje_axial(self.eje_axial, self.archivos, self.carpeta, self.slider.value())
        layout.addWidget(self.grafico)

        # Establece el layout con el gráfico actualizado
        self.eje_axial.setLayout(layout)

    # Función que actualiza el valor mostrado en la interfaz (el valor actual del slider)
    def ver_valor(self):
        self.valor_actual.setText(str(self.slider.value()))

    # Función que abre una nueva ventana con la información de la imagen seleccionada
    def abrir_info(self):
        # Crea una nueva instancia de VentanaInfo_img, pasando parámetros relevantes
        v_info = VentanaInfo_img(self.archivos, self.carpeta, self.slider.value(), self, self.__ventanaprincipal)
        
        # Muestra la ventana de información
        v_info.show()

    # Función para cerrar la ventana actual y mostrar la ventana de menú (secundaria)
    def menu(self):
        self.close()  # Cierra la ventana actual
        self.__ventanaSec.show()  # Muestra la ventana secundaria

    # Función que pregunta al usuario si está seguro de cerrar sesión
    def mostrar_inicio(self):
        # Mensaje de confirmación antes de cerrar sesión
        text = "¿Está seguro que desea cerrar sesión?"
        message = QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # Si el usuario selecciona "Sí", cierra la ventana y muestra la ventana principal
        if message == QMessageBox.StandardButton.Yes:
            self.close()  # Cierra la ventana actual
            self.__ventanaprincipal.show()  # Muestra la ventana principal

# Clase que representa una ventana para mostrar la información del paciente relacionada con una imagen DICOM, hereda de QDialog.
class VentanaInfo_img(QDialog):
    def __init__(self, archivos, carpeta, indice, ppal=None, ventana_main=None):
        super().__init__(ppal)  # Llama al constructor de QDialog (ventana base)
        
        # Carga la interfaz de usuario desde el archivo .ui
        loadUi("ventana_paciente.ui", self)
        
        # Establece el título de la ventana
        self.setWindowTitle("Información de paciente")
        
        # Inicializa las variables de instancia con los parámetros proporcionados
        self.indice = indice
        self.archivos = archivos
        self.carpeta = carpeta
        self.ventana_main = ventana_main
        
        # Llama a la función setup para configurar los controles de la ventana
        self.setup()

    # Configura las conexiones de los controles de la ventana y los valores iniciales de los campos de texto
    def setup(self):
        # Conecta el botón "volver" para cerrar la ventana cuando se presiona
        self.volver.clicked.connect(self.close)
        
        # Conecta el botón "guardar" con la función que guarda la información
        self.guardar.clicked.connect(self.save)
        
        # Establece los valores de los campos de texto con la información obtenida de los archivos DICOM
        self.cuerpo.setText(self.info("BodyPartExamined"))  # Información sobre la parte del cuerpo examinada
        self.sexo.setText(self.info("PatientSex"))          # Información sobre el sexo del paciente
        self.peso.setText(str(self.info("PatientWeight")))  # Información sobre el peso del paciente
        # Formatea la fecha de adquisición de la imagen y la establece en el campo correspondiente
        self.fecha.setText(f'{str(self.info("AcquisitionDate"))[:4]}/ {str(self.info("AcquisitionDate"))[4:6]}/ {str(self.info("AcquisitionDate"))[6:]}')

    # Función que obtiene información específica de una imagen DICOM dada una característica
    def info(self, caracteristica):
        # Lee el archivo DICOM correspondiente usando la librería pydicom
        imagen_dicom = pydicom.dcmread(os.path.join(self.carpeta, self.archivos[self.indice-1]))
        
        # Intenta obtener la característica solicitada de la imagen DICOM
        # Si no existe, devuelve "N.A"
        x = getattr(imagen_dicom, caracteristica, "N.A")
        
        # Si la característica está vacía, devuelve un mensaje "No existe"
        if x == "":
            return "No existe"
        else:
            return x  # Si la característica existe, la devuelve

    # Función que guarda la información introducida en la ventana de detalles
    def save(self):
        # Crea una lista con la información de la ventana (fecha, sexo, parte del cuerpo, peso)
        lista = [self.fecha.text(), self.sexo.text(), self.cuerpo.text(), self.peso.text()]
        
        # Prepara un conjunto de datos que contiene la ruta de la carpeta y la lista de información
        info = (self.carpeta, lista)
        
        # Valida si la información ya existe en la base de datos a través del controlador de la ventana principal
        validacion = self.ventana_main._controlador.validar_info(info)
        
        if validacion:
            # Si la información ya existe, muestra un mensaje de advertencia
            text = "La información de esta imagen ya se encuentra en la base de datos"
            message = QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            # Si la información no existe, la guarda en la base de datos y muestra un mensaje de éxito
            text = "Información guardada en la base de datos con éxito"
            message = QMessageBox.information(self, "Guardar información", text, QMessageBox.StandardButton.Ok)
            self.ventana_main._controlador.enviar_info(info)  # Envia la información al controlador para su almacenamiento

# Clase que representa una ventana principal para la visualización y procesamiento de imágenes médicas.
class VentanaCont(QMainWindow):
    def __init__(self, archivos, carpeta, ppal=None, sec=None):
        super().__init__(ppal)  # Llama al constructor de QMainWindow (ventana base)
        
        # Carga la interfaz de usuario desde el archivo .ui
        loadUi("ventana_contador.ui", self)
        
        # Establece el título de la ventana
        self.setWindowTitle("Contador en imágenes")
        
        # Inicializa las variables de instancia con los parámetros proporcionados
        self.__ventanaprincipal = ppal
        self.__ventanaSec = sec
        self.archivos = archivos
        self.carpeta = carpeta
        
        # Llama a la función setup para configurar los controles de la ventana
        self.setup()

    # Configura las conexiones de los controles de la ventana
    def setup(self):
        # Conecta el botón "cerrar" para cerrar sesión y mostrar la ventana principal
        self.cerrar.clicked.connect(self.mostrar_inicio)
        
        # Conecta el botón "volver" para volver a la ventana anterior
        self.volver.clicked.connect(self.menu)
        
        # Conecta los botones de procesamiento de imágenes con sus respectivas funciones
        self.rest.clicked.connect(self.cargar_default)
        self.apert.clicked.connect(self.cargar_apertura)
        self.erosion.clicked.connect(self.cargar_erosion)
        self.dilat.clicked.connect(self.cargar_dilatacion)
        self.cierre.clicked.connect(self.cargar_cierre)
        
        # Añade los archivos a un comboBox para que el usuario seleccione un archivo
        for archivo in self.archivos:
            self.comboBox.addItem(archivo)
        
        # Carga la primera imagen de forma predeterminada
        self.cargar_inicial()

    # Carga la imagen predeterminada al abrir la ventana
    def cargar_inicial(self):
        # Si hay elementos en el comboBox, selecciona el primero y carga la imagen correspondiente
        if self.comboBox.count() > 0:
            self.comboBox.setCurrentIndex(0)
            self.cargar_default()
            # Conecta el cambio de índice del comboBox a la función cargar_default
            self.comboBox.currentIndexChanged.connect(self.cargar_default)

    # Carga la imagen seleccionada por el usuario sin ningún procesamiento adicional
    def cargar_default(self):
        archivo_seleccionado = self.comboBox.currentText()
        ruta_completa = os.path.join(self.carpeta, archivo_seleccionado)
        imagen_procesada = self.__ventanaprincipal._controlador.img_conextion(ruta_completa)
        self.mostrar_imagen(imagen_procesada)

    # Muestra la imagen procesada en el QLabel de la ventana
    def mostrar_imagen(self, imagen):
        pixmap = QPixmap.fromImage(imagen)  # Convierte la imagen a un formato que PyQt puede mostrar
        # Redimensiona la imagen para ajustarse al tamaño del QLabel sin distorsionar la relación de aspecto
        pixmap = pixmap.scaled(self.img.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.img.setPixmap(pixmap)  # Establece el pixmap redimensionado en el QLabel

    # Carga la imagen procesada con dilatación usando el valor del kernel proporcionado
    def cargar_dilatacion(self):
        # Verifica si el valor del kernel es mayor que 0
        if self.num_kernel.value() == 0:
            text = "Por favor seleccione una dimensión de Kernel válida"
            message = QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta, archivo_seleccionado)
            # Llama al controlador para realizar la dilatación
            imagen_procesada = self.__ventanaprincipal._controlador.img_dilatacion_conex(ruta_completa, int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)

    # Carga la imagen procesada con erosión usando el valor del kernel proporcionado
    def cargar_erosion(self):
        if self.num_kernel.value() == 0:
            text = "Por favor seleccione una dimensión de Kernel válida"
            message = QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta, archivo_seleccionado)
            # Llama al controlador para realizar la erosión
            imagen_procesada = self.__ventanaprincipal._controlador.img_erosion_conex(ruta_completa, int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)

    # Carga la imagen procesada con apertura usando el valor del kernel proporcionado
    def cargar_apertura(self):
        if self.num_kernel.value() == 0:
            text = "Por favor seleccione una dimensión de Kernel válida"
            message = QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta, archivo_seleccionado)
            # Llama al controlador para realizar la apertura
            imagen_procesada = self.__ventanaprincipal._controlador.img_apertura_conex(ruta_completa, int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)

    # Carga la imagen procesada con cierre usando el valor del kernel proporcionado
    def cargar_cierre(self):
        if self.num_kernel.value() == 0:
            text = "Por favor seleccione una dimensión de Kernel válida"
            message = QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta, archivo_seleccionado)
            # Llama al controlador para realizar el cierre
            imagen_procesada = self.__ventanaprincipal._controlador.img_cierre_conex(ruta_completa, int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)

    # Función que cierra la ventana y muestra la ventana secundaria (secundaria)
    def menu(self):
        self.close()  # Cierra la ventana actual
        self.__ventanaSec.show()  # Muestra la ventana secundaria

    # Muestra un mensaje de confirmación para cerrar sesión
    def mostrar_inicio(self):
        text = "¿Está seguro que desea cerrar sesión?"
        message = QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if message == QMessageBox.StandardButton.Yes:
            self.close()  # Cierra la ventana
            self.__ventanaprincipal.show()  # Muestra la ventana principal

        
class Graficas_Senales(FigureCanvas):

    def __init__(self, parent=None, width=6, height=5, dpi=100):
        # Inicializa una figura de matplotlib y su eje
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        self.__axis = self.__fig.add_subplot(111)  # Añade un único eje a la figura
        FigureCanvas.__init__(self, self.__fig) 
        
        #FigureCanvas, permite dibujar en QT las gráficas de Matplotlib

    def graficar_senal(self, datos, matriz, min, max):
        """
        Dibuja todas las señales en el rango especificado.
        :param datos: matriz completa
        :param matriz: Matriz con las señales. Segmento de datos extraído (no usado en esta implementación). Está en 2D, canal-señal
        :param min: Límite inferior del eje x.
        :param max: Límite superior del eje x.
        """
        self.__axis.clear()  # Limpia el eje antes de dibujar
        for c in range(matriz.shape[0]):  # Itera por cada canal (fila en la matriz)
            etiqueta = f'Canal {c+1}'
            self.__axis.plot(matriz[c, :], label=etiqueta) 
        self.__axis.set_xlim(min, max)
        self.__axis.legend(loc='right')
        self.__axis.set_xlabel('Señales')
        self.__axis.set_ylabel('Datos')
        self.__axis.set_title('Gráfica Señal')
        self.draw()  # Actualiza el gráfico

    def graficarCanal(self, matriz, arreglo, min, max):
        """
        Dibuja una señal específica (canal) en el rango dado.
        :param matriz: Matriz con las señales.
        :param arreglo: Índice del canal a graficar (1-indexado).
        :param min: Límite inferior del eje x.
        :param max: Límite superior del eje x.
        """
        self.__axis.clear()
        if 1 <= arreglo <= matriz.shape[0]:  # Valida que el canal exista
            self.__axis.plot(matriz[arreglo - 1, :])  # Graficar la fila correspondiente
            self.__axis.set_xlim(min, max)
            self.__axis.set_xlabel("Señal")
            self.__axis.set_ylabel("Datos")
            self.__axis.set_title("Gráfica Canales")
            self.__axis.legend([f"Canal {arreglo}"])
            self.draw()
        else:
            # Mensaje de error si el índice del canal está fuera de rango
            print(f"Índice de canal {arreglo} fuera de rango. Debe estar entre 1 y {matriz.shape[0]}.")

class Ventana_senfis(QDialog):
    def __init__(self, ruta_mat, ppal=None, sec=None):
        super().__init__(ppal)  # Llama al constructor de la clase base QDialog.
        loadUi("ventana_senales.ui", self)  # Carga el archivo de interfaz .ui para configurar la ventana.
        self.setWindowTitle("Archivos .MAT")  # Establece el título de la ventana.
        self.__ventanaPadre = ppal  # Guarda la referencia a la ventana principal (padre).
        self.__ventanaSec = sec  # Guarda la referencia a la ventana secundaria.
        self.__mat = ruta_mat  # Guarda la ruta del archivo .mat.
        self.__x_min = 0  # Establece el valor mínimo del eje x para la visualización de señales.
        self.__x_max = 1500  # Establece el valor máximo del eje x.
        self.__canal = 1  # Establece el canal por defecto.
        self.__matriz = np.zeros((1, 1))  # Inicializa una matriz vacía.
        self.setup()  # Llama al método setup para inicializar elementos de la ventana.

    def setup(self):
        llaves_dic = self.cargar_senal().keys()  # Obtiene las llaves (nombres de las señales) del archivo .mat.
        llaves = list(llaves_dic)  # Convierte las llaves a una lista.
        for llave in llaves:  # Itera sobre las llaves y las añade al comboBox `llaves`.
            self.llaves.addItem(llave)
        if len(llaves) == 1:  # Si solo hay una llave en el archivo .mat, selecciona esa por defecto.
            self.llaves.setCurrentIndex(0)
            self.mostrar_matriz()  # Muestra la matriz correspondiente a la llave seleccionada.
        self.llaves.currentIndexChanged.connect(self.mostrar_matriz)  # Conecta el cambio de selección de la lista de llaves a la función `mostrar_matriz`.
        layout_2 = QVBoxLayout()  # Crea un layout vertical para mostrar la gráfica.
        self.grafica_canales.setLayout(layout_2)  # Establece este layout en el widget de la gráfica.
        self.__graf_señales = Graficas_Senales(self.grafica_canales, width=5, height=4, dpi=100)  # Crea el objeto para graficar señales.
        layout_2.addWidget(self.__graf_señales)  # Añade el gráfico al layout.
        self.todos.hide()  # Oculta el botón 'todos' inicialmente.
        self.label_6.show()  # Muestra la etiqueta `label_6`.
        self.p_min.setPlaceholderText("Número minimo")  # Establece el texto de marcador de posición en el campo de número mínimo.
        self.p_max.setPlaceholderText("Número maximo")  # Establece el texto de marcador de posición en el campo de número máximo.
        self.p_min.editingFinished.connect(self.validar_min_max)  # Conecta la edición del campo `p_min` a la función de validación.
        self.p_max.editingFinished.connect(self.validar_min_max)  # Conecta la edición del campo `p_max` a la función de validación.
        if self.__ventanaPadre is not None and self.__ventanaPadre._controlador is not None:  # Si la ventana principal y su controlador existen.
            self.todos.clicked.connect(self.grafSeg)  # Conecta el clic del botón 'todos' a la función `grafSeg`.
        self.cerrar.clicked.connect(self.mostrar_inicio)  # Conecta el clic del botón 'cerrar' a la función `mostrar_inicio`.
        self.volver.clicked.connect(self.menu)  # Conecta el clic del botón 'volver' a la función `menu`.
        self.adelantar_1.hide()  # Oculta los botones de adelantar/retrasar señales al principio.
        self.retroceder_1.hide()  # Oculta los botones de adelantar/retrasar señales.
        self.adelantar_1.clicked.connect(self.adelantar_senal)  # Conecta el clic del botón 'adelantar_1' a la función `adelantar_senal`.
        self.retroceder_1.clicked.connect(self.retroceder_senal)  # Conecta el clic del botón 'retroceder_1' a la función `retroceder_senal`.
        self.adelantar_2.hide()  # Oculta los botones de adelantar/retrasar canales al principio.
        self.retroceder_2.hide()  # Oculta los botones de adelantar/retrasar canales.
        self.adelantar_2.clicked.connect(self.adelantar_canal)  # Conecta el clic del botón 'adelantar_2' a la función `adelantar_canal`.
        self.retroceder_2.clicked.connect(self.retroceder_canal)  # Conecta el clic del botón 'retroceder_2' a la función `retroceder_canal`.

    def validar_min_max(self):
        minimo_text = self.p_min.text()  # Obtiene el texto ingresado en el campo mínimo.
        maximo_text = self.p_max.text()  # Obtiene el texto ingresado en el campo máximo.
        if (minimo_text and maximo_text) == '':  # Si ambos campos están vacíos, oculta el botón 'todos'.
            self.todos.hide()
        else:
            self.todos.show()  # Si los campos no están vacíos, muestra el botón 'todos'.

    def cargar_senal(self):
        self.__data = sio.loadmat(self.__mat)  # Carga el archivo .mat usando SciPy.
        return self.__data  # Devuelve los datos cargados del archivo.

    def mostrar_matriz(self):
        try:
            llave_array = self.llaves.currentText()  # Obtiene la llave seleccionada del comboBox.
            llave_array = str(llave_array)  # Convierte la llave a cadena de texto.
            self.__num_array = self.__data[llave_array]  # Obtiene la señal asociada a la llave seleccionada.
            if self.__num_array.size > 0:  # Si la señal tiene datos.
                if len(self.__num_array.shape) == 3:  # Si la señal tiene 3 dimensiones (filas, columnas, submatrices).
                    filas, columnas, submatrices = self.__num_array.shape  # Obtiene las dimensiones de la señal.
                    self.__matriz = np.reshape(self.__num_array, (filas, columnas * submatrices), order='F')  # Remodela la matriz de la señal.
                    filas, columnas = self.__matriz.shape  # Obtiene las nuevas dimensiones después del cambio de forma.
                    self.senal_mat.setRowCount(filas)  # Establece el número de filas en la tabla.
                    self.senal_mat.setColumnCount(columnas)  # Establece el número de columnas en la tabla.
                    for i in range(filas):  # Llena la tabla con los valores de la matriz.
                        for j in range(columnas):
                            item = QTableWidgetItem(str(self.__matriz[i, j]))
                            self.senal_mat.setItem(i, j, item)
                    filas_ma = range(self.__matriz.shape[0])  # Crea un rango de filas para los canales.
                    self.canales.clear()  # Limpia los elementos del comboBox de canales.
                    for fila in filas_ma:  # Añade las filas al comboBox de canales.
                        self.canales.addItem(str(fila + 1))
                    if len(filas_ma) == 1:  # Si solo hay un canal, lo selecciona por defecto.
                        self.canales.setCurrentIndex(0)
                    self.canales.currentIndexChanged.connect(self.mostrar_matriz)  # Conecta el cambio de canal a la función `mostrar_matriz`.
                    self.filas.setText(str(self.__matriz.shape[0]))  # Muestra el número de filas en el campo correspondiente.
                    self.columnas.setText(str(self.__matriz.shape[1]))  # Muestra el número de columnas en el campo correspondiente.
                    self.__ventanaPadre._controlador.pasar_informacion(self.__matriz)  # Pasa la matriz al controlador de la ventana principal.
                else:  # Si la señal tiene 2 dimensiones (filas, columnas).
                    self.__matriz = self.__num_array  # Asigna la señal directamente a la matriz.
                    filas, columnas = self.__matriz.shape  # Obtiene las dimensiones de la señal.
                    self.senal_mat.setRowCount(filas)  # Establece el número de filas en la tabla.
                    self.senal_mat.setColumnCount(columnas)  # Establece el número de columnas en la tabla.
                    for i in range(filas):  # Llena la tabla con los valores de la matriz.
                        for j in range(columnas):
                            item = QTableWidgetItem(str(self.__matriz[i, j]))
                            self.senal_mat.setItem(i, j, item)
                    filas_ma = range(self.__matriz.shape[0])  # Crea un rango de filas para los canales.
                    self.canales.clear()  # Limpia los elementos del comboBox de canales.
                    for fila in filas_ma:  # Añade las filas al comboBox de canales.
                        self.canales.addItem(str(fila + 1))
                    if len(filas_ma) == 1:  # Si solo hay un canal, lo selecciona por defecto.
                        self.canales.setCurrentIndex(0)
                    self.canales.currentIndexChanged.connect(self.mostrar_matriz)  # Conecta el cambio de canal a la función `mostrar_matriz`.
                    self.filas.setText(str(self.__matriz.shape[0]))  # Muestra el número de filas en el campo correspondiente.
                    self.columnas.setText(str(self.__matriz.shape[1]))  # Muestra el número de columnas en el campo correspondiente.
                    self.__ventanaPadre._controlador.pasar_informacion(self.__matriz)  # Pasa la matriz al controlador de la ventana principal.
        except KeyError:
            QMessageBox.warning(self, "Llave no encontrada", "La llave seleccionada no existe.")  # Muestra un mensaje de advertencia si no se encuentra la llave.
            print("Llave no encontrada", "La llave seleccionada no existe.")
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"Ocurrió un error: {str(e)}")  # Muestra un mensaje de error inesperado.
            print("Error inesperado", f"Ocurrió un error: {e}")

    # El código continúa de manera similar con las funciones de graficado, navegación y manejo de eventos.
    
    def grafSeg(self):
        self.adelantar_1.show()
        self.retroceder_1.show()
        self.adelantar_2.hide()
        self.retroceder_2.hide()
        
        try:
            self.__x_max = int(self.p_max.text())
        except Exception as e:
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok)
            print("GRAF: ", e)
            
        if self.__x_max > self.__matriz.shape[1]:
            text = "El rango no es válido. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok)
            
        try:
            self.__x_min = int(self.p_min.text())
        except  Exception as e:
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok)
            print("GRAF: ", e)

        try:
            self.__graf_señales.graficar_senal(self.__ventanaPadre._controlador.devolver_segmento(self.__x_min, self.__x_max),self.__matriz, self.__x_min,self.__x_max)
        except (AttributeError, ValueError):
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Rango inválido", text, QMessageBox.StandardButton.Ok)
     
    def grafCanal(self):
        self.adelantar_2.show()
        self.retroceder_2.show()
        self.adelantar_1.hide()
        self.retroceder_1.hide()
        
        try:
            self.__x_max = int(self.p_max.text())
        except Exception as e:
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok )
            print("GRAF: ", e)
        try:
            self.__x_min = int(self.p_min.text())
        except  Exception as e:
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok )
            print("GRAF: ", e)
        try:
            canal = self.canales.currentText()  # Obtener el texto del comboBox
            self.__canal = int(canal)  # Intentar convertirlo a entero
        except  Exception as e:
            text = "Seleccione un canal válido."
            QMessageBox.warning(self, "Error de canal", text, QMessageBox.StandardButton.Ok)
            print("GRAF: ", e)
            return  # Salir del método si ocurre un error


    def retroceder_senal(self):
        if self.__x_min < 2000:
            return
        self.__x_min = self.__x_min - 2000
        self.__x_max = self.__x_max - 2000
        try:
            self.__graf_señales.graficar_senal(self.__ventanaPadre._controlador.devolver_segmento(self.__x_min, self.__x_max),self.__matriz, self.__x_min,self.__x_max)
        except Exception as e:
            print(e, "excepcion")
        
    def adelantar_senal(self):
        self.__x_min = self.__x_min + 2000
        self.__x_max = self.__x_max + 2000
        
        try:
            self.__graf_señales.graficar_senal(self.__ventanaPadre._controlador.devolver_segmento(self.__x_min, self.__x_max),self.__matriz, self.__x_min,self.__x_max)
        except Exception as e:
            print(e, "excepcion")
        
    def retroceder_canal(self):
        if self.__x_min < 2000:
            return
        self.__x_min = self.__x_min - 2000
        self.__x_max = self.__x_max - 2000
        self.__graf_señales.graficarCanal(self.__matriz,self.__canal, self.__x_min, self.__x_max)

    def adelantar_canal(self):
        self.__x_min = self.__x_min + 2000
        self.__x_max = self.__x_max + 2000
        self.__graf_señales.graficarCanal(self.__matriz,self.__canal, self.__x_min, self.__x_max)
            
    def mostrar_inicio(self):
        # Función para volver a la ventana principal
        try:
            self.close()  # Cierra la ventana actual
            if self.__ventanaPadre is not None:
                self.__ventanaPadre.show()  # Muestra la ventana principal
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al volver a la ventana principal: {str(e)}")  # Si ocurre un error

    def menu(self):
        # Función para ir al menú principal
        try:
            self.__ventanaSec.show()  # Muestra la ventana secundaria
            self.close()  # Cierra la ventana actual
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al ir al menú: {str(e)}")  # Si ocurre un error

    def keyPressEvent(self, event):
        if event.key() == 16777220 or event.key() == 16777221:  # Códigos de Enter/Return
            event.ignore()  # Esto evita que el evento de Enter cierre la ventana
            self.grafSeg()
        else:
            super().keyPressEvent(event)
        

            
