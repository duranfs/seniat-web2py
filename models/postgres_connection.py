import psycopg2
import os
from dotenv import load_dotenv
from gluon.http import HTTP  # Importar HTTP para manejar errores

def get_postgresql_connection(host, database, port, user=None, password=None, timeout=10):
    """
    Establece conexión con una base de datos PostgreSQL remota
    
    Args:
        host (str): IP o nombre del servidor remoto
        database (str): Nombre de la base de datos
        port (int): Puerto de conexión (5432 es el default de PostgreSQL)
        user (str): Usuario (opcional, puede venir de .env)
        password (str): Contraseña (opcional, puede venir de .env)
        timeout (int): Timeout en segundos para la conexión
        
    Returns:
        connection: Objeto de conexión a PostgreSQL
        
    Raises:
        HTTP: Si no se puede establecer la conexión
    """
    load_dotenv()
    
    # Obtener credenciales de .env si no se proporcionan
    pg_user = user or os.getenv('POSTGRES_USER')
    pg_pass = password or os.getenv('POSTGRES_PASSWORD')
    
    if not all([host, database, pg_user, pg_pass]):
        raise HTTP(500, "Faltan parámetros de conexión para PostgreSQL")
    
    try:
        connection = psycopg2.connect(
            host=host,
            database=database.lower(), #nombre de la base de datos en minúsculas
            user=pg_user,
            password=pg_pass,
            port=port,
            connect_timeout=timeout,
            options=f'-c statement_timeout={timeout*1000}'  # Timeout en ms
        )
        return connection
        
    except psycopg2.OperationalError as e:
        raise HTTP(500, f"Error de conexión a PostgreSQL en {host}:{port} - {str(e)}")
    except Exception as e:
        raise HTTP(500, f"Error inesperado al conectar a PostgreSQL: {str(e)}")