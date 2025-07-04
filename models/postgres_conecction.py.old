import psycopg2
import os
from dotenv import load_dotenv
from gluon.http import HTTP
from contextlib import contextmanager

load_dotenv()  # Cargar variables una vez al inicio

@contextmanager
def get_postgresql_connection(host, database, port, user=None, password=None, timeout=10):
    """
    Context manager para conexiones PostgreSQL que garantiza su cierre automático.
    
    Uso:
    with get_postgresql_connection(...) as conn:
        # usar conn aquí
    # La conexión se cierra automáticamente al salir del bloque
    
    Args:
        host (str): IP o nombre del servidor remoto
        database (str): Nombre de la base de datos
        port (int): Puerto de conexión
        user (str): Usuario (opcional)
        password (str): Contraseña (opcional)
        timeout (int): Timeout en segundos
        
    Yields:
        psycopg2.connection: Objeto de conexión
        
    Raises:
        HTTP: Si hay errores de conexión
    """
    pg_user = user or os.getenv('POSTGRES_USER')
    pg_pass = password or os.getenv('POSTGRES_PASSWORD')
    
    if not all([host, database, pg_user, pg_pass]):
        raise HTTP(500, "Faltan parámetros de conexión para PostgreSQL")
    
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            database=database.lower(),
            user=pg_user,
            password=pg_pass,
            port=port,
            connect_timeout=timeout,
            options=f'-c statement_timeout={timeout*1000}'
        )
        yield conn
    except psycopg2.OperationalError as e:
        raise HTTP(500, f"Error de conexión a PostgreSQL en {host}:{port} - {str(e)}")
    except Exception as e:
        raise HTTP(500, f"Error inesperado al conectar a PostgreSQL: {str(e)}")
    finally:
        if conn is not None:
            conn.close()  # Garantiza el cierre de la conexión