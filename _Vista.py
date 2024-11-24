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

class Eje_sagital(FigureCanvas):
    def __init__(self, parent, archivo, carpeta, numero):
        super().__init__(Figure())
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.numero_imagen= numero

        # Llama al método para mostrar la imagen en el widget
        self.mostrar_en_qt(archivo, carpeta)
        
    def mostrar_en_qt(self, archivo_dicom, carpeta):
        # Convierte el archivo DICOM a QImage
        slices = [pydicom.dcmread(carpeta + '/' + s) for s in os.listdir(carpeta)]
        slices.sort(key = lambda x: int(x.ImagePositionPatient[0]))
        volumen = np.stack([s.pixel_array for s in slices])
        volumen = volumen.astype(np.int16)
        self.ax.imshow(volumen[self.numero_imagen-1,:,:],cmap="gray", aspect='auto') 
        self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])  # Configura el objeto Axes para ocupar todo el espacio
        self.draw()
        
class Eje_coronal(FigureCanvas):
    def __init__(self, parent, archivo, carpeta,numero):
        super().__init__(Figure())
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.numero_imagen= numero
        
        # Llama al método para mostrar la imagen en el widget
        self.mostrar_en_qt(archivo, carpeta)
        
    def mostrar_en_qt(self, archivo_dicom, carpeta):
        # Convierte el archivo DICOM a QImage
        slices = [pydicom.dcmread(carpeta + '/' + s) for s in os.listdir(carpeta)]
        slices.sort(key = lambda x: int(x.ImagePositionPatient[0]))
        #HALLAMOS UN APROXIMADO DE LA PROPORCION DE CADA EJE PARA USAR EL SLIDER
        pixel_spacing=slices[0].PixelSpacing
        slice_thickness=slices[0].SliceThickness
        proporcion_filas = float(slice_thickness)/ float(pixel_spacing[1])
        proporcion_columnas =float(slice_thickness)/ float(pixel_spacing[0])
        proporciones=(proporcion_filas,proporcion_columnas)
        valores = tuple(int(math.floor(coord)) for coord in proporciones) #Los valores hallados se usan para la posicion del eje
        
        volumen = np.stack([s.pixel_array for s in slices])
        volumen = volumen.astype(np.int16)
        valor=(self.numero_imagen-1)*valores[0]
        self.ax.imshow(volumen[:,:,valor], cmap="gray",aspect="auto")  
        self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])  # Configura el objeto Axes para ocupar todo el espacio
        self.draw()
        
class Eje_axial(FigureCanvas):
    def __init__(self, parent, archivo, carpeta,numero):
        super().__init__(Figure())
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.numero_imagen= numero
        self.mostrar_en_qt(archivo, carpeta)
        
    def mostrar_en_qt(self, archivo_dicom, carpeta): 
        slices = [pydicom.dcmread(carpeta + '/' + s) for s in os.listdir(carpeta)]
        slices.sort(key = lambda x: int(x.ImagePositionPatient[0]))
        #HALLAMOS UN APROXIMADO DE LA PROPORCION DE CADA EJE PARA USAR EL SLIDER
        pixel_spacing=slices[0].PixelSpacing
        slice_thickness=slices[0].SliceThickness
        proporcion_filas = float(slice_thickness)/ float(pixel_spacing[1])
        proporcion_columnas =float(slice_thickness)/ float(pixel_spacing[0])
        proporciones=(proporcion_filas,proporcion_columnas)
        valores = tuple(int(math.floor(coord)) for coord in proporciones) #Los valores hallados se usan para la posicion del eje
        volumen = np.stack([s.pixel_array for s in slices])
        volumen = volumen.astype(np.int16)
        valor=(self.numero_imagen-1)*valores[0]
        self.ax.imshow(volumen[:,valor,:], cmap="gray", aspect='auto') 
        self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])  # Configura el objeto Axes para ocupar todo el espacio
        self.draw()
        
class VentanaInicial(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_inicial.ui",self)
        self.setWindowTitle("MED-ANALYZE")
        self.setup()

    def setControlador(self,c):
        self._controlador= c
        
    def setup(self):
        self.iniciar.clicked.connect(self.iniciar_programa)
    
    def iniciar_programa(self):
        v_login=VentanaLogin(self._controlador,self)
        self.hide()
        v_login.show()

class VentanaLogin(QDialog):
    def __init__(self, c, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_login.ui", self)
        self.setWindowTitle("Inicio de sesión")
        self._controlador = c
        self.setup()
        
    def setup(self):
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_rechazar)
        
    def opcion_aceptar(self):
        usuario = self.user.text()
        password = self.passw.text()
        validacion = self._controlador.validar_login(usuario, password)
        
        if validacion:
            text = "¡Bienvenido al programa!"
            QMessageBox.information(self, "Login", text, QMessageBox.StandardButton.Ok)
            
            # Abrimos la ventana de imágenes si se autentica el usuario
            self.abrir_ventana_menu()
            self.user.setText("")
            self.passw.setText("")
        
        else:
            text = "¡Datos de acceso incorrectos!"
            QMessageBox.warning(self, "Alerta", text, QMessageBox.StandardButton.Ok)
            
    def opcion_rechazar(self):
        self.user.setText("")
        self.passw.setText("")
        
    def abrir_ventana_menu(self):
        v_menu = VentanaMenu(self)
        self.hide()
        v_menu.show()
        
class VentanaMenu(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("ventana_menu.ui", self)
        self.setWindowTitle("Menú principal")
        self.__ventanaprincipal = ppal
        self.setup()
        
    def setup(self):
        self.img_med.clicked.connect(self.mostrar_imgmed)
        self.cont.clicked.connect(self.mostrar_cont)
        self.sen_fis.clicked.connect(self.mostrar_senfis)
        self.cerrar.clicked.connect(self.mostrar_inicio)
        
    def mostrar_imgmed(self):
        carpeta=QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        archivos_dicom = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.dcm')]
        
        # Verifica si hay archivos DICOM en la carpeta
        if not archivos_dicom:
            text="No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            message= QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
        else:
            v_imgmed=Ventana_imgmed(archivos_dicom, carpeta, self.__ventanaprincipal, self)
            self.hide() 
            v_imgmed.show() 
        
    def mostrar_cont(self):
        carpeta=QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        lista_archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(('.jpg','.png'))]
        if not lista_archivos:
            text="No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            message= QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
        else:
            v_cont=VentanaCont(lista_archivos,carpeta,self.__ventanaprincipal,self)
            self.hide() 
            v_cont.show()
        
        
    def mostrar_senfis(self):
        try:
            mat, _ = QFileDialog.getOpenFileName(self, "Abrir señal", "", "Todos los archivos (*);;Archivos mat (*.mat);;Python (*.py)")

            if not mat.endswith('.mat'):
                text="No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo"
                message= QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)
            else:
                v_senfis=Ventana_senfis(mat, self.__ventanaprincipal, self)
                self.hide() 
                v_senfis.show() 

        except FileNotFoundError:
            text="No se encontraron los archivos requeridos, por favor verifique el tipo de archivo e intente de nuevo."
            message= QMessageBox.critical(self, "Alerta!", text, QMessageBox.StandardButton.Ok)  
    
    def mostrar_inicio (self):
        text="¿Está seguro que desea cerrar sesión?"
        message= QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if message== QMessageBox.StandardButton.Yes:
            self.close()
            self.__ventanaprincipal.show()
                            
class Ventana_imgmed(QDialog):   
    def __init__(self, archivos, carpeta, ppal=None, sec= None):
        super().__init__(ppal)              
        loadUi("ventana_imgmed.ui", self)    
        self.setWindowTitle("Imágenes Médicas")
        self.__ventanaprincipal = ppal
        self.__ventanaSec= sec
        self.archivos = archivos
        self.carpeta = carpeta
        self.valor_actual.setText("1")
        self.setup()
        self.graficar_eje_sag()
        self.graficar_eje_co()
        self.graficar_eje_ax()
            
    def setup(self):
        self.cerrar.clicked.connect(self.mostrar_inicio)
        self.volver.clicked.connect(self.menu)
        self.slider.setMinimum(1)
        self.slider.setMaximum(len(self.archivos))
        self.slider.setValue(1)
        self.slider.valueChanged.connect(self.ver_valor)
        self.info_im.clicked.connect(self.abrir_info)
        self.slider.valueChanged.connect(self.graficar_eje_sag)
        self.slider.valueChanged.connect(self.graficar_eje_co)
        self.slider.valueChanged.connect(self.graficar_eje_ax)
        self.valor_maximo.setText(str(len(self.archivos)))
    
    def graficar_eje_sag(self):
        layout = self.eje_sagital.layout() or QVBoxLayout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self.grafico = Eje_sagital(self.eje_sagital, self.archivos, self.carpeta, self.slider.value())
        layout.addWidget(self.grafico)

        self.eje_sagital.setLayout(layout)
          
    def graficar_eje_co(self):
        layout = self.eje_coronal.layout() or QVBoxLayout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self.grafico = Eje_coronal(self.eje_coronal, self.archivos, self.carpeta,self.slider.value())
        layout.addWidget(self.grafico)
        self.eje_coronal.setLayout(layout)
        
    def graficar_eje_ax(self):
        layout = self.eje_axial.layout() or QVBoxLayout()
    
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self.grafico = Eje_axial(self.eje_axial, self.archivos, self.carpeta, self.slider.value())
        layout.addWidget(self.grafico)
        self.eje_axial.setLayout(layout)
         
    def ver_valor(self):
        self.valor_actual.setText(str(self.slider.value()))
        
    def abrir_info(self): 
        v_info=VentanaInfo_img(self.archivos,self.carpeta,self.slider.value(), self, self.__ventanaprincipal)
        v_info.show()
        
    def menu (self):
        self.close()
        self.__ventanaSec.show()
          
    def mostrar_inicio (self):
        text="¿Está seguro que desea cerrar sesión?"
        message= QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if message== QMessageBox.StandardButton.Yes:
            self.close()
            self.__ventanaprincipal.show()
            
class VentanaInfo_img(QDialog):
    def __init__(self, archivos,carpeta, indice, ppal=None, ventana_main=None):
        super().__init__(ppal)
        loadUi("ventana_paciente.ui",self)
        self.setWindowTitle("Información de paciente")
        self.indice=indice
        self.archivos=archivos
        self.carpeta=carpeta
        self.ventana_main=ventana_main
        
        self.setup()
        
    def setup(self):
        self.volver.clicked.connect(self.close)
        self.guardar.clicked.connect(self.save)
        self.cuerpo.setText(self.info("BodyPartExamined"))
        self.sexo.setText(self.info("PatientSex"))
        self.peso.setText(str(self.info("PatientWeight")))
        self.fecha.setText(f'{str(self.info("AcquisitionDate"))[:4]}/ {str(self.info("AcquisitionDate"))[4:6]}/ {str(self.info("AcquisitionDate"))[6:]}')

    def info(self,caracteristica):
        imagen_dicom = pydicom.dcmread(os.path.join(self.carpeta, self.archivos[self.indice-1]))
        x= getattr(imagen_dicom, caracteristica, "N.A")
        if x == "":
            return "No existe"
        else:
            return x
    
    def save(self): 
        lista=[self.fecha.text(),self.sexo.text(), self.cuerpo.text(), self.peso.text()]
        info = (self.carpeta,lista)
        validacion= self.ventana_main._controlador.validar_info(info)
        if validacion:
            text="La información de esta imagen ya se encuentra en la base de datos"
            message=QMessageBox.warning(self, "Error",text,QMessageBox.StandardButton.Ok)
        
        else:
            text="Información guardada en la base de datos con éxito"
            message=QMessageBox.information(self, "Guardar información",text,QMessageBox.StandardButton.Ok)
            self.ventana_main._controlador.enviar_info(info)

class VentanaCont(QMainWindow):
    def __init__(self,archivos,carpeta,ppal=None, sec= None, ):
        super().__init__(ppal)
        loadUi("ventana_contador.ui",self)
        self.setWindowTitle("Contador en imagenes")
        self.__ventanaprincipal= ppal
        self.__ventanaSec= sec
        self.archivos=archivos
        self.carpeta=carpeta
        self.setup()
        
        
    def setup(self):
        self.cerrar.clicked.connect(self.mostrar_inicio)
        self.volver.clicked.connect(self.menu)
        self.rest.clicked.connect(self.cargar_default)
        self.apert.clicked.connect(self.cargar_apertura)
        self.erosion.clicked.connect(self.cargar_erosion)
        self.dilat.clicked.connect(self.cargar_dilatacion)
        self.cierre.clicked.connect(self.cargar_cierre)
        for archivo in self.archivos:
            self.comboBox.addItem(archivo)
        self.cargar_inicial()
    
    def cargar_inicial(self):
        if self.comboBox.count() > 0:
            self.comboBox.setCurrentIndex(0)
            self.cargar_default()
            self.comboBox.currentIndexChanged.connect(self.cargar_default)
            
    def cargar_default(self):
        archivo_seleccionado = self.comboBox.currentText()
        ruta_completa = os.path.join(self.carpeta+'/'+archivo_seleccionado)
        imagen_procesada = self.__ventanaprincipal._controlador.img_conextion(ruta_completa)
        self.mostrar_imagen(imagen_procesada)
            
    def mostrar_imagen(self, imagen):
        pixmap = QPixmap.fromImage(imagen)
        pixmap = pixmap.scaled(self.img.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.img.setPixmap(pixmap)

    def cargar_dilatacion(self):
        if self.num_kernel.value()==0:
            text="Por favor seleccione una dimensión de Kernel válida"
            message= QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta+'/'+archivo_seleccionado)
            imagen_procesada = self.__ventanaprincipal._controlador.img_dilatacion_conex(ruta_completa,int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)
    
    def cargar_erosion(self):
        if self.num_kernel.value()==0:
            text="Por favor seleccione una dimensión de Kernel válida"
            message= QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta+'/'+archivo_seleccionado)
            imagen_procesada = self.__ventanaprincipal._controlador.img_erosion_conex(ruta_completa,int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)
    
    def cargar_apertura(self):
        if self.num_kernel.value()==0:
            text="Por favor seleccione una dimensión de Kernel válida"
            message= QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta+'/'+archivo_seleccionado)
            imagen_procesada = self.__ventanaprincipal._controlador.img_apertura_conex(ruta_completa,int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)

    def cargar_cierre(self):
        if self.num_kernel.value()==0:
            text="Por favor seleccione una dimensión de Kernel válida"
            message= QMessageBox.warning(self, "Error", text, QMessageBox.StandardButton.Ok)
        else:
            archivo_seleccionado = self.comboBox.currentText()
            ruta_completa = os.path.join(self.carpeta+'/'+archivo_seleccionado)
            imagen_procesada = self.__ventanaprincipal._controlador.img_cierre_conex(ruta_completa,int(self.num_kernel.value()))
            self.mostrar_imagen(imagen_procesada)  

    def menu (self):
        self.close()
        self.__ventanaSec.show()
          
    def mostrar_inicio (self):
        text="¿Está seguro que desea cerrar sesión?"
        message= QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if message== QMessageBox.StandardButton.Yes:
            self.close()
            self.__ventanaprincipal.show()
            
            
class Graficas_Senales(FigureCanvas):

    def __init__(self, parent= None,width=6, height=5, dpi=100):

            self.__fig = Figure(figsize=(width, height), dpi=dpi)
            self.__axis = self.__fig.add_subplot(111)
            FigureCanvas.__init__(self,self.__fig)

    def graficar_senal(self, datos, matriz, min,max):
        self.__axis.clear()
        for c in range(datos.shape[0]):
            etiqueta = f'Canal {c+1}'
            self.__axis.plot(matriz[c,:]+c*2500, label=etiqueta)
            self.__axis.set_xlim(min, max)
        self.__axis.legend(loc ='right')
        self.__axis.set_xlabel('Señales')
        self.__axis.set_ylabel('Datos')
        self.__axis.set_title('Gráfica Señal')
        self.draw()  

    def graficarCanal(self, matriz, arreglo, min, max):
        self.__axis.clear()
        if 1 <= arreglo <= matriz.shape[0]:
            self.__axis.plot(matriz[arreglo - 1, :])  
            self.__axis.set_xlim(min, max)
            self.__axis.set_xlabel("Señal")
            self.__axis.set_ylabel("Datos")
            self.__axis.set_title("Gráfica Canales")
            self.__axis.legend([f"Canal {arreglo}"])
            self.draw()

        else:
            print(f"Índice de canal {arreglo} fuera de rango. Debe estar entre 1 y {matriz.shape[0]}.")
        
class Ventana_senfis(QDialog):
    def __init__(self,ruta_mat, ppal=None, sec= None):
        super().__init__(ppal)              
        loadUi("ventana_senales.ui", self)    
        self.setWindowTitle("Archivos .MAT")
        self.__ventanaPadre = ppal
        self.__ventanaSec= sec
        self.__mat = ruta_mat
        self.__x_min = 0
        self.__x_max = 1500
        self.__canal = 1
        self.__matriz = np.zeros((1,1))
        self.setup()

    def setup(self):

        llaves_dic = self.cargar_senal().keys()
        llaves = list(llaves_dic)
        for llave in llaves:
            self.llaves.addItem(llave)
        if len(llaves) == 1:
            self.llaves.setCurrentIndex(0)
            self.mostrar_matriz()
        self.llaves.currentIndexChanged.connect(self.mostrar_matriz)
        layout_2 = QVBoxLayout()
        self.grafica_canales.setLayout(layout_2)
        self.__graf_señales = Graficas_Senales(self.grafica_canales, width=5, height=4, dpi=100)
        layout_2.addWidget(self.__graf_señales)
        self.num_canal.hide()
        self.canales.hide()
        self.todos.hide()
        self.canal.hide()
        self.label_6.show()
        self.graficar.hide()
        self.p_min.setPlaceholderText("Numero minimo")
        self.p_max.setPlaceholderText("Numero maximo")
        self.p_min.editingFinished.connect(self.validar_min_max)
        self.p_max.editingFinished.connect(self.validar_min_max)
        if self.__ventanaPadre is not None and self.__ventanaPadre._controlador is not None:
            self.todos.clicked.connect(self.grafSeg)
            self.canal.clicked.connect(self.grafCanal)
        self.canales.hide() 
        self.cerrar.clicked.connect(self.mostrar_inicio)
        self.volver.clicked.connect(self.menu) 
        self.adelantar_1.hide()
        self.retroceder_1.hide()
        self.adelantar_1.clicked.connect(self.adelantar_senal)
        self.retroceder_1.clicked.connect(self.retroceder_senal)
        self.adelantar_2.hide()
        self.retroceder_2.hide()
        self.adelantar_2.clicked.connect(self.adelantar_canal)
        self.retroceder_2.clicked.connect(self.retroceder_canal)

    def validar_min_max(self):
        minimo_text = self.p_min.text()
        maximo_text = self.p_max.text()
        if (minimo_text and maximo_text) == '':
            self.todos.hide()
            self.canal.hide()
            self.graficar.hide()
        else:
            self.todos.show()
            self.canal.show()

    def cargar_senal(self):

        self.__data = sio.loadmat(self.__mat)
        return self.__data

    def mostrar_matriz(self):
        try:
            llave_array = self.llaves.currentText()
            llave_array = str(llave_array)
            self.__num_array = self.__data[llave_array]
            if self.__num_array.size > 0:
                if len(self.__num_array.shape) == 3:
                    filas, columnas, submatrices = self.__num_array.shape
                    self.__matriz = np.reshape(self.__num_array, (filas, columnas * submatrices), order='F')
                    filas, columnas = self.__matriz.shape
                    self.senal_mat.setRowCount(filas)
                    self.senal_mat.setColumnCount(columnas)
                    for i in range(filas):
                        for j in range(columnas):
                            item = QTableWidgetItem(str(self.__matriz[i, j]))
                            self.senal_mat.setItem(i, j, item)
                    filas_ma = range(self.__matriz.shape[0])
                    for fila in filas_ma:
                        self.canales.addItem(str(fila+1))
                    if len(filas_ma) == 1:
                        self.canales.setCurrentIndex(0)
                        self.selecCanal
                    self.canales.currentIndexChanged.connect(self.mostrar_matriz)
                    self.filas.setText(str(self.__matriz.shape[0]))
                    self.columnas.setText(str(self.__matriz.shape[1]))
                    self.__ventanaPadre._controlador.pasar_informacion(self.__matriz)
                else:
                    self.__matriz = self.__num_array
                    filas, columnas = self.__matriz.shape
                    self.senal_mat.setRowCount(filas)
                    self.senal_mat.setColumnCount(columnas)
                    for i in range(filas):
                        for j in range(columnas):
                            item = QTableWidgetItem(str(self.__matriz[i, j]))
                            self.senal_mat.setItem(i, j, item)
                    filas_ma = range(self.__matriz.shape[0])
                    for fila in filas_ma:
                        self.canales.addItem(str(fila+1))
                    if len(filas_ma) == 1:
                        self.canales.setCurrentIndex(0)
                    self.canales.currentIndexChanged.connect(self.mostrar_matriz)
                    self.filas.setText(str(self.__matriz.shape[0]))
                    self.columnas.setText(str(self.__matriz.shape[1]))
                    self.__ventanaPadre._controlador.pasar_informacion(self.__matriz)
    
        except AttributeError:
            text = f"No es una llave válida, ya que la opción seleccionada no es un arreglo. Intente de nuevo"
            message = QMessageBox.information(self, "Llave inválida", text, QMessageBox.StandardButton.Ok)

    def grafSeg(self):
        self.adelantar_1.show()
        self.retroceder_1.show()
        self.num_canal.hide()
        self.canales.hide()
        self.graficar.hide()   
        self.adelantar_2.hide()
        self.retroceder_2.hide()
        try:
            self.__x_max = int(self.p_maximo.text())
        except (AttributeError, ValueError):
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok)
            
        if self.__x_max > self.__matriz.shape[1]:
            text = "El rango no es válido. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok)
            
        try:
            self.__x_min = int(self.p_minimo.text())
        except (AttributeError, ValueError):
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok)

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
        self.num_canal.show()
        self.canales.show()
        self.graficar.show()
        try:
            self.__x_max = int(self.p_max.text())
        except (AttributeError, ValueError):
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok )
        try:
            self.__x_min = int(self.p_min.text())
        except (AttributeError, ValueError):
            text = "El rango es incorrecto. Intente de nuevo"
            message = QMessageBox.warning(self, "Error de rango", text, QMessageBox.StandardButton.Ok )
        try:
            canal = self.canales.currentText()  # Obtener el texto del comboBox
            self.__canal = int(canal)  # Intentar convertirlo a entero
        except ValueError:
            text = "Seleccione un canal válido."
            QMessageBox.warning(self, "Error de canal", text, QMessageBox.StandardButton.Ok)
            return  # Salir del método si ocurre un error

    
    def menu (self):
        self.close()
        self.__ventanaSec.show()
        
    def mostrar_inicio (self):
        text="¿Está seguro que desea cerrar sesión?"
        message= QMessageBox.question(self, "Cerrar sesión", text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if message== QMessageBox.StandardButton.Yes:
            self.close()
            self.__ventanaPadre.show()
                            
    def retroceder_senal(self):
        if self.__x_min < 2000:
            return
        self.__x_min = self.__x_min - 2000
        self.__x_max = self.__x_max - 2000
        self.__graf_señales.graficar_senal(self.__ventanaPadre._controlador.devolver_segmento(self.__x_min, self.__x_max),self.__matriz, self.__x_min,self.__x_max)

    def adelantar_senal(self):
        self.__x_min = self.__x_min + 2000
        self.__x_max = self.__x_max + 2000
        self.__graf_señales.graficar_senal(self.__ventanaPadre._controlador.devolver_segmento(self.__x_min, self.__x_max),self.__matriz, self.__x_min,self.__x_max)

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
        

            
