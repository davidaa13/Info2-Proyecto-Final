# Importaciones necesarias
from _Modelo import *  # Importa la lógica del modelo definida en otro archivo
from _Vista import *  # Importa la lógica de la interfaz de usuario desde otro archivo
from PyQt6.QtWidgets import QApplication  # Para crear aplicaciones de escritorio con PyQt
import sys  # Proporciona acceso a funciones del sistema operativo, como argumentos de línea de comandos

# Clase Coordinador: actúa como intermediario entre la Vista y el Modelo
class Coordinador:    
    def __init__(self, vista, modelo):
        """
        Constructor que inicializa el coordinador con una vista y un modelo.
        """
        self.__mi_vista = vista  # Referencia a la instancia de la vista
        self.__mi_modelo = modelo  # Referencia a la instancia del modelo
    
    def validar_login(self, u, p):   
        """
        Valida las credenciales de inicio de sesión enviándolas al modelo.
        """
        return self.__mi_modelo.validar_login(u, p)
    
    def enviar_info(self, x):
        """
        Envía información al modelo para que sea procesada o almacenada.
        """
        self.__mi_modelo.cargar_info(x)
    
    def validar_info(self, x):
        """
        Verifica si cierta información ya está almacenada en el modelo.
        """
        return self.__mi_modelo.validar_info(x)
    
    def img_conextion(self, imagen):
        """
        Solicita al modelo la imagen predeterminada en formato QImage.
        """
        return self.__mi_modelo.imagen_default(imagen)
    
    def img_erosion_conex(self, imagen, kernel):
        """
        Aplica una operación de erosión sobre la imagen utilizando el modelo.
        """
        return self.__mi_modelo.img_erosionar(imagen, kernel)
    
    def img_dilatacion_conex(self, imagen, kernel):
        """
        Aplica una operación de dilatación sobre la imagen utilizando el modelo.
        """
        return self.__mi_modelo.img_dilatar(imagen, kernel)

    def img_apertura_conex(self, imagen, kernel):
        """
        Aplica una operación de apertura sobre la imagen utilizando el modelo.
        """
        return self.__mi_modelo.img_apertura(imagen, kernel)
    
    def img_cierre_conex(self, imagen, kernel):
        """
        Aplica una operación de cierre sobre la imagen utilizando el modelo.
        """
        return self.__mi_modelo.img_cierre(imagen, kernel)
    
    def pasar_informacion(self, data):
        """
        Asigna datos al modelo para que puedan ser utilizados posteriormente.
        """
        self.__mi_modelo.asignar_data(data)

    def devolver_segmento(self, x_min, x_max):
        """
        Solicita un segmento de los datos cargados al modelo.
        """
        return self.__mi_modelo.devolver_segmento(x_min, x_max)
    

# Código cliente
def main():
    """
    Función principal que inicializa la aplicación.
    """
    app = QApplication(sys.argv)  # Crea una instancia de la aplicación PyQt, donde toda la interfaz vivirá
    #sys.argv los argumentos que son las operaciones del cliente se pasan a la interfaz
    # argv es lo que se hace desde el sistema operativo como dar clic, como escribir, que son argumentos que se pasan al aplicativo, es decir la interfaz
    
    #Se instancia el MVC
    vista = VentanaInicial()  # Instancia de la ventana principal, clase definida en _Vista
    modelo = Sistema()  # Instancia del modelo definida en _Modelo
    coordinador = Coordinador(vista, modelo)  # Instancia del coordinador que conecta la vista y el modelo
    
    vista.setControlador(coordinador)  # Conecta la vista al coordinador
    vista.show()  # Muestra la ventana principal
    sys.exit(app.exec())  # Inicia el bucle de eventos de la aplicación y asegura un cierre limpio

# Punto de entrada del programa
if __name__ == "__main__":
    main()  # Llama a la función principal si el script se ejecuta directamente