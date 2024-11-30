import json
import mysql.connector
from PyQt6.QtGui import QImage
import numpy as np
import cv2
import imageio.v2 as imageio

data= {}
data["credenciales"] = []
data["credenciales"].append({"usuario": "us1", "contrasena": "bio123" })
data["credenciales"].append({"usuario": "us2", "contrasena": "789" })
data["credenciales"].append({"usuario": "us3", "contrasena": "123" })
with open("Usuario.json","w") as file:
    json.dump(data,file, indent=4)
    
SERVER = 'localhost'
USER = 'informatica_2'
PASSWD = 'bio123'
DB = 'base_datos'
cnx = mysql.connector.connect(user=USER , password=PASSWD , host=SERVER , database=DB )
cursor = cnx.cursor()

class Sistema:
    def __init__(self):
        self.__usuario = self.obtener_usuario()
        self.__password = self.obtener_contraseña()
        self._dic_info = {} 
        self.__data = None
        
    def obtener_usuario(self):
        with open("Usuario.json") as file:
            data= json.load(file)
            lista=[]
            for credencial in data["credenciales"]:
                lista.append(credencial["usuario"])
            return lista
    
    def obtener_contraseña(self):
        with open("Usuario.json") as file:
            data= json.load(file)
            lista=[]
            for credencial in data["credenciales"]:
                lista.append(credencial["contrasena"])
            return lista
    
    def set_usuario(self, u):
        self.__usuario = u
    
    def set_password(self, p):
        self.__password = p
    
    def validar_login(self, u, p):
        return (u in self.__usuario) and (p in self.__password)
        
    def cargar_info(self,x):
        self._dic_info[x[0]] = x[1]

        lista = self._dic_info[x[0]]
        
        sql_insert = """INSERT  INTO  datos_pacientes(INDICE,FECHA, SEXO,PART_CUERPO, PESO)  
                        VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(sql_insert,(None,lista[0],lista[1], lista[2], lista[3]))
        cnx.commit()
        
    def validar_info(self,info):
        return info[0] in self._dic_info

    def imagen_default(self, imagen):
        img = cv2.imread(imagen)
        return self.convertir_a_qimage(img)
    
    def convertir_a_qimage(self, img):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        q_img = QImage(img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return q_img.rgbSwapped()
    
    def img_erosionar(self, imagen, num):
        img= cv2.imread(imagen)
        media=np.mean(img)
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,imgB = cv2.threshold(imga,media,255, cv2.THRESH_BINARY)
        kernel = np.ones((num,num), np.uint8)   #Tamaño del kernel peersonalizado
        imaEro = cv2.erode(imgB, kernel, iterations=1)
        return self.convertir_a_qimage(imaEro)
        
    def img_dilatar(self,imagen,num):
        img= cv2.imread(imagen)
        media=np.mean(img)
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        _,imgB = cv2.threshold(imga,media,255, cv2.THRESH_BINARY)
        kernel = np.ones((num,num), np.uint8)   #Tamaño del kernel peersonalizado
        imaDil = cv2.dilate(imgB, kernel, iterations=1)
        return self.convertir_a_qimage(imaDil)
    
    def img_apertura(self,imagen,num):
        img= cv2.imread(imagen)
        media=np.mean(img)
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,imgB = cv2.threshold(imga,media,255, cv2.THRESH_BINARY)
        kernel = np.ones((num,num), np.uint8)
        imaOp2=cv2.morphologyEx(imgB, cv2.MORPH_OPEN, kernel, iterations = 1)
        return self.convertir_a_qimage(imaOp2)
    
    def img_cierre(self,imagen,num):
        img= cv2.imread(imagen)
        media=np.mean(img)
        imga = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,imgB = cv2.threshold(imga,media,255, cv2.THRESH_BINARY)
        kernel = np.ones((num,num), np.uint8)
        imaOp3=cv2.morphologyEx(imgB, cv2.MORPH_CLOSE, kernel, iterations = 1)
        return self.convertir_a_qimage (imaOp3)
    
    def asignar_data(self,data):
        self.__data = data 
        self.__filas = self.__data.shape[0] 
        self.__columnas = self.__data.shape[1]  
    
    def devolver_segmento(self, x_min, x_max):
        if x_min >= x_max:
            return None
        return self.__data[:, x_min-1:x_max]
    
    
    
    
    
    
    
    

    