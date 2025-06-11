from gluon.contrib.pymysql import connect
import pyodbc  # Requerido para conexiones a SQL Server
import os
from dotenv import load_dotenv

# Funciones para conexión a SQL Server
def get_sqlserver_connection(servidor, base_datos, puerto=1433, controlador='ODBC Driver 17 for SQL Server'):
    # Configurar conexión sqlserver
    load_dotenv()
    usuario = os.getenv('SQLSERVER_USER')  # Valor por defecto solo para desarrollo
    password = os.getenv('SQLSERVER_PASSWORD')
    """
    Establece conexión con una base de datos SQL Server
    
    Parámetros:
        servidor (str): Nombre del servidor o dirección IP
        base_datos (str): Nombre de la base de datos
        usuario (str): Usuario para la conexión
        contrasena (str): Contraseña del usuario
        puerto (int): Puerto de conexión (por defecto: 1433)
        controlador (str): Controlador ODBC a usar (por defecto: ODBC Driver 17 for SQL Server)
    
    Retorna:
        pyodbc.Connection: Objeto de conexión
    
    Lanza:
        HTTP: Si ocurre un error durante la conexión
    """
    try:
        cadena_conexion = (
            f"DRIVER={{{controlador}}};"
            f"SERVER={servidor},{puerto};"
            f"DATABASE={base_datos};"
            f"UID={usuario};"
            f"PWD={password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=30;"
        )
        
        conexion = pyodbc.connect(cadena_conexion)
        return conexion
    except Exception as e:
        raise HTTP(500, f"No se pudo conectar a SQL Server: {str(e)}")

def probar_conexion_sqlserver():
    """
    Función de prueba para verificar la conexión a SQL Server
    """
    try:
        # Ejemplo de parámetros - debes modificarlos con tus credenciales reales
        conn = get_sqlserver_connection(
            servidor='tu_servidor',
            base_datos='tu_base_de_datos',
            usuario='tu_usuario',
            contrasena='tu_contrasena'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        fila = cursor.fetchone()
        conn.close()
        return f"Conexión exitosa a SQL Server. Versión: {fila[0]}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"