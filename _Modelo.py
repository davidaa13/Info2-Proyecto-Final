# Importación de bibliotecas necesarias
import json  # Para manejar archivos JSON
import mysql.connector  # Para conectarse y manipular bases de datos MySQL
from PyQt6.QtGui import QImage  # Para manejar imágenes en formato PyQt
import numpy as np  # Para realizar operaciones matemáticas y de matrices
import cv2  # Para procesamiento de imágenes
import imageio.v2 as imageio  # Para leer y escribir imágenes

# Creación de un archivo JSON con credenciales de usuario
data = {}
data["credenciales"] = [
    {"usuario": "us1", "contrasena": "bio123"},
    {"usuario": "us2", "contrasena": "789"},
    {"usuario": "us3", "contrasena": "123"}
]
# Guarda las credenciales en un archivo JSON
with open("Usuario.json", "w") as file:
    json.dump(data, file, indent=4)

# Configuración de la conexión a la base de datos
SERVER = 'localhost'  # Dirección del servidor
USER = 'informatica_2'  # Usuario de la base de datos
PASSWD = 'bio123'  # Contraseña
DB = 'base_datos'  # Nombre de la base de datos
cnx = mysql.connector.connect(user=USER, password=PASSWD, host=SERVER, database=DB)
cursor = cnx.cursor()  # Inicializa un cursor para ejecutar comandos SQL

# Clase principal para manejar las funcionalidades del sistema
class Sistema:
    def __init__(self):
        # Inicializa las propiedades privadas y carga datos desde el archivo JSON
        self.__usuario = self.obtener_usuario()  # Lista de usuarios
        self.__password = self.obtener_contraseña()  # Lista de contraseñas
        self._dic_info = {}  # Diccionario para almacenar información cargada
        self.__data = None  # Matriz de datos (inicialmente vacía)
    
    def obtener_usuario(self):
        """
        Carga los nombres de usuario desde el archivo JSON.
        """
        with open("Usuario.json") as file:
            data = json.load(file)
            return [credencial["usuario"] for credencial in data["credenciales"]]
    
    def obtener_contraseña(self):
        """
        Carga las contraseñas desde el archivo JSON.
        """
        with open("Usuario.json") as file:
            data = json.load(file)
            return [credencial["contrasena"] for credencial in data["credenciales"]]
    
    def set_usuario(self, u):
        """
        Establece un nuevo valor para el usuario.
        """
        self.__usuario = u
    
    def set_password(self, p):
        """
        Establece un nuevo valor para la contraseña.
        """
        self.__password = p
    
    def validar_login(self, u, p):
        """
        Valida si las credenciales proporcionadas coinciden con las almacenadas.
        
        retorna True si las validaciones son iguales
        """
        return (u in self.__usuario) and (p in self.__password)
        
    def cargar_info(self, x):
        """
        Carga información al diccionario local y la inserta en la base de datos.
        """
        self._dic_info[x[0]] = x[1]  # Agrega la información al diccionario
        # x[0] se refiere a la clave en el diccionario, poro ejemplo fecha
        #x[1] se refiere al valor d esa clave, por ejemplo la fecha
        lista = self._dic_info[x[0]] 
        
        # Inserta la información en la base de datos
        sql_insert = """INSERT INTO datos_pacientes (INDICE, FECHA, SEXO, PART_CUERPO, PESO)  
                        VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert, (None, lista[0], lista[1], lista[2], lista[3]))
        cnx.commit()  # Confirma los cambios en la base de datos
        
    def validar_info(self, info):
        """
        Valida si una clave existe en el diccionario de información.
        """
        return info[0] in self._dic_info

    def imagen_default(self, imagen):
        """
        Carga una imagen por defecto y la convierte a formato QImage.
        """
        img = cv2.imread(imagen)  # Carga la imagen desde el archivo, usando OpenCV. La imagen se lee como una matriz (array) de numpy.
        return self.convertir_a_qimage(img)  # Convierte la imagen cargada en formato numpy a un objeto QImage para PyQt.

    def convertir_a_qimage(self, img):
        """
        Convierte una imagen de OpenCV (numpy array) a formato QImage.
        """
        if len(img.shape) == 2:  # Si la imagen es en escala de grises (tiene solo 2 dimensiones: alto y ancho)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)  # Convierte la imagen de escala de grises a RGB para poder mostrarla en color.
        h, w, ch = img.shape  # Obtiene las dimensiones de la imagen: altura (h), ancho (w) y número de canales de color (ch).
        bytes_per_line = ch * w  # Calcula el número de bytes por línea, necesario para el formato QImage.
        q_img = QImage(img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)  # Crea un objeto QImage a partir de los datos de la imagen, el tamaño y el formato.
        return q_img.rgbSwapped()  # Invierte el orden de los colores de BGR (usado por OpenCV) a RGB (usado por PyQt).

    def img_erosionar(self, imagen, num):
        """
        Aplica la operación de erosión a una imagen.
        """
        img = cv2.imread(imagen)  # Carga la imagen desde el archivo.
        media = np.mean(img)  # Calcula el brillo promedio de la imagen, usado para binarizarla más adelante.
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises.
        _, imgB = cv2.threshold(imga, media, 255, cv2.THRESH_BINARY)  # Aplica un umbral binario a la imagen de acuerdo al brillo promedio (en escala de grises).
        kernel = np.ones((num, num), np.uint8)  # Crea un kernel (matriz) de erosión de tamaño `num x num` con valores 1.
        imaEro = cv2.erode(imgB, kernel, iterations=1)  # Aplica la operación de erosión a la imagen binaria.
        return self.convertir_a_qimage(imaEro)  # Convierte el resultado de la erosión a formato QImage para mostrarlo en PyQt.

    def img_dilatar(self, imagen, num):
        """
        Aplica la operación de dilatación a una imagen.
        """
        img = cv2.imread(imagen)  # Carga la imagen desde el archivo.
        media = np.mean(img)  # Calcula el brillo promedio de la imagen para usarlo en la binarización.
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises.
        _, imgB = cv2.threshold(imga, media, 255, cv2.THRESH_BINARY)  # Aplica el umbral binario a la imagen.
        kernel = np.ones((num, num), np.uint8)  # Crea un kernel de dilatación de tamaño `num x num` con valores 1.
        imaDil = cv2.dilate(imgB, kernel, iterations=1)  # Aplica la operación de dilatación a la imagen binaria.
        return self.convertir_a_qimage(imaDil)  # Convierte la imagen dilatada a formato QImage.

    def img_apertura(self, imagen, num):
        """
        Aplica la operación de apertura (erosión seguida de dilatación).
        """
        img = cv2.imread(imagen)  # Carga la imagen desde el archivo.
        media = np.mean(img)  # Calcula el brillo promedio de la imagen, utilizado en el umbral binario.
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises.
        _, imgB = cv2.threshold(imga, media, 255, cv2.THRESH_BINARY)  # Aplica un umbral binario a la imagen.
        kernel = np.ones((num, num), np.uint8)  # Crea un kernel para la operación de apertura de tamaño `num x num`.
        imaOp2 = cv2.morphologyEx(imgB, cv2.MORPH_OPEN, kernel, iterations=1)  # Aplica la operación de apertura (erosión seguida de dilatación) a la imagen binaria.
        return self.convertir_a_qimage(imaOp2)  # Convierte la imagen resultante a formato QImage.

    def img_cierre(self, imagen, num):
        """
        Aplica la operación de cierre (dilatación seguida de erosión).
        """
        img = cv2.imread(imagen)  # Carga la imagen desde el archivo.
        media = np.mean(img)  # Calcula el brillo promedio para binarizar la imagen.
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises.
        _, imgB = cv2.threshold(imga, media, 255, cv2.THRESH_BINARY)  # Aplica el umbral binario a la imagen.
        kernel = np.ones((num, num), np.uint8)  # Crea un kernel para la operación de cierre de tamaño `num x num`.
        imaOp3 = cv2.morphologyEx(imgB, cv2.MORPH_CLOSE, kernel, iterations=1)  # Aplica la operación de cierre (dilatación seguida de erosión) a la imagen binaria.
        return self.convertir_a_qimage(imaOp3)  # Convierte la imagen resultante a formato QImage.

    
    def asignar_data(self, data):
        """
        Asigna una matriz de datos al sistema.
        """
        self.__data = data  # Matriz de datos
        self.__filas = self.__data.shape[0]  # Número de filas
        self.__columnas = self.__data.shape[1]  # Número de columnas
    
    def devolver_segmento(self, x_min, x_max):
        """
        Devuelve un segmento de la matriz de datos entre las columnas especificadas.
        """
        if x_min >= x_max:
            return None  # Retorna None si el rango no es válido
        return self.__data[:, x_min-1:x_max]  # Retorna el segment