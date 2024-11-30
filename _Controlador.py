from _Modelo import *
from _Vista import *
from PyQt6.QtWidgets import QApplication  
import sys 

class Coordinador:    
    def __init__(self, vista, modelo):
        self.__mi_vista= vista
        self.__mi_modelo= modelo
    
    def validar_login(self, u,p):   
        return self.__mi_modelo.validar_login(u,p)
    
    def enviar_info(self,x):
        self.__mi_modelo.cargar_info(x)
    
    def validar_info(self,x):
        return self.__mi_modelo.validar_info(x)
    
    def img_conextion(self, imagen):
        return self.__mi_modelo.imagen_default(imagen)
    
    def img_erosion_conex(self,imagen,kernel):
        return self.__mi_modelo.img_erosionar(imagen, kernel)
    
    def img_dilatacion_conex(self,imagen,kernel):
        return self.__mi_modelo.img_dilatar(imagen,kernel)

    def img_apertura_conex(self,imagen,kernel):
        return self.__mi_modelo.img_apertura(imagen,kernel)
    
    def img_cierre_conex(self,imagen,kernel):
        return self.__mi_modelo.img_cierre(imagen,kernel)
    
    def gif_conex(self,imagen):
        return self.__mi_modelo.gif(imagen)
    
    def pasar_informacion(self,data):
        self.__mi_modelo.asignar_data(data)

    def devolver_segmento(self, x_min, x_max):
        return self.__mi_modelo.devolver_segmento(x_min, x_max)
    
    
    
        

#Codigo cliente
def main():
    app= QApplication(sys.argv) #app de QApplication es donde irá toda la interfaz, sys.argv ayuda a entender por medio de argumentos las operaciones que haga el usuario desde el sistema operativo
    vista= VentanaInicial()
    modelo= Sistema()
    coordinador= Coordinador(vista, modelo)
    vista.setControlador(coordinador)
    vista.show()
    sys.exit(app.exec())


if __name__== "__main__":
    main()