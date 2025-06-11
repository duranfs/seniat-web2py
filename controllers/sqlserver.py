import time
from datetime import datetime
import json  # Añade esta línea al inicio del archivo


def index():
    # Obtener conexión

    connection = get_sqlserver_connection("172.16.132.53", "Liquidacion",  puerto=1433, controlador='ODBC Driver 17 for SQL Server')
    
    try:
        # Consulta para obtener los últimos errores
        sql = """
        SELECT @@SERVERNAME, @@version, @@SERVICENAME, @@MAX_CONNECTIONS, @@OPTIONS
        """
        
        cursor = connection.cursor()
        cursor.execute(sql)
        
        # Obtener nombres de columnas
        columns = [col[0] for col in cursor.description]
        
        # Obtener todos los registros
        rows = cursor.fetchall()
        
        return dict(columns=columns, rows=rows, error=None)
        
    except Exception as e:
        return dict(error=str(e))
        
    finally:
        if connection:
            connection.close()

