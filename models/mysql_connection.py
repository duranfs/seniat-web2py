# models/mysql_connection.py
import sys
import os
from dotenv import load_dotenv
from gluon.http import HTTP

# Cargar variables de entorno solo una vez
load_dotenv()

# Intentar importar PyMySQL y compatibilidad con MySQLdb
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    mysql_available = True
except ImportError:
    mysql_available = False
    pymysql = None

def get_mysql_connection(host, database, port=3306, user=None, password=None, timeout=10):
    """
    Establece conexión con MySQL/MariaDB usando PyMySQL.
    Usa variables de entorno MYSQL_USER y MYSQL_PASSWORD si user/password no se proveen.
    """
    if not mysql_available:
        raise HTTP(500, "PyMySQL no está instalado. Ejecuta: pip install pymysql")
    
    mysql_user = user or os.getenv('MYSQL_USER')
    mysql_pass = password or os.getenv('MYSQL_PASSWORD')
    
    if not all([host, database, mysql_user, mysql_pass]):
        raise HTTP(500, "Faltan parámetros de conexión: host, database, usuario o contraseña")
    
    try:
        connection = pymysql.connect(
            host=host,
            user=mysql_user,
            password=mysql_pass,
            database=database.lower(),
            port=int(port),
            connect_timeout=timeout,
            autocommit=True,
            charset='utf8mb4'
        )
        return connection
        
    except Exception as e:
        # Registrar error completo en consola o log
        print(f"[DEBUG] Error completo al conectar a MySQL en {host}:{port}: {repr(e)}")
        # Levantar un 500 genérico para el navegador
        raise HTTP(500, f"Error de conexión a MySQL en {host}:{port}")
