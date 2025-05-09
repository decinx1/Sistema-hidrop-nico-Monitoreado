# conexion_cliente.py

import pymysql
from datetime import datetime

def obtener_datos_por_fecha(fecha_str):
    try:
        conexion = pymysql.connect(
            host='192.168.0.116',
            user='sensorrasp',
            password='Rasp1234!',
            database='hydroponia',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.Cursor  # Usa DictCursor si quieres resultados con nombres de columna
        )

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
        print("Error al conectar con la base de datos:", err)
        return None
