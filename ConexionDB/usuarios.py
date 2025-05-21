import bcrypt
from ConexionDB.conexion import conectar_bd


def registrar_usuario(nombre_usuario, correo, telefono, contraseña):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            # Generar hash de la contraseña
            hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

            # Insertar en la base de datos
            sql = """
            INSERT INTO usuarios (nombre_usuario, correo, telefono, contraseña_hash)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre_usuario, correo, telefono, hash_contraseña))
            conexion.commit()
            return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False
    finally:
        conexion.close()


def verificar_credenciales(usuario_input, contraseña_input):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            # Buscar por nombre_usuario o correo
            sql = """
            SELECT contraseña_hash FROM usuarios
            WHERE nombre_usuario = %s OR correo = %s
            """
            cursor.execute(sql, (usuario_input, usuario_input))
            resultado = cursor.fetchone()

            if resultado:
                hash_guardado = resultado[0]
                # Verificar contraseña
                return bcrypt.checkpw(contraseña_input.encode('utf-8'), hash_guardado.encode('utf-8'))
            return False
    except Exception as e:
        print(f"Error en la verificación: {e}")
        return False
    finally:
        conexion.close()
