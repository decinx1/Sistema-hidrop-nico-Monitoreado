import pymysql
from datetime import datetime

def conectar_bd():
    return pymysql.connect(
        host='192.168.136.38',
        user='sensorrasp',
        password='Rasp1234!',
        database='hydroponia',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )