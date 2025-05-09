#Descargar pip install mysql-connector-python y pip install mysql-connector
import mysql.connector
from mysql.connector import Error

def conectar_db ():
    try:
        conexion = mysql.connector.connect(
            host="localhost",      # Nombre del host
            user="root",           # Usuario de MySQL
            password="",           # Contraseña de MySQL 
            database="conector_db "   # Nombre de la base de datos
        )
        
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

# Prueba la conexión
if __name__ == "__main__":
    conexion = conectar_db ()
    if conexion:
        conexion.close()