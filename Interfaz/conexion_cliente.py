# conexion_cliente.py

import pymysql
from datetime import datetime

def conectar_bd():
    return pymysql.connect(
        host='192.168.0.121',
        user='sensorrasp',
        password='Rasp1234!',
        database='hydroponia',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

def obtener_datos_por_fecha(fecha_str):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = """
            SELECT id, sensor, valor, fecha
            FROM lecturas
            WHERE DATE(fecha) = %s
        """
        cursor.execute(consulta, (fecha_str,))
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except pymysql.MySQLError as err:
        print("Error al obtener datos por fecha:", err)
        return None

def obtener_todas_las_fechas_y_datos():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "SELECT id, sensor, valor, fecha FROM lecturas"
        cursor.execute(consulta)
        filas = cursor.fetchall()

        resultados = {}
        for fila in filas:
            fecha_str = fila[3].strftime("%Y-%m-%d")
            if fecha_str not in resultados:
                resultados[fecha_str] = []
            resultados[fecha_str].append(fila)

        cursor.close()
        conexion.close()
        return resultados
    except pymysql.MySQLError as err:
        print("Error al obtener todos los datos:", err)
        return None

