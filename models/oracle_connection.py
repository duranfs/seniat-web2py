from gluon.contrib.pymysql import connect
import cx_Oracle
import os
from dotenv import load_dotenv

def get_oracle_connection(ip, service_name, puerto, ver):
    # Configurar conexión Oracle
    
    CONNECTION_TIMEOUT = 5  # Aumentado para entornos lentos
    QUERY_TIMEOUT = 5

    load_dotenv()
    oracle_user = os.getenv('ORACLE_USER')  # Valor por defecto solo para desarrollo
    oracle_pass = os.getenv('ORACLE_PASSWORD')
    
    if ver == 9:
        dsn = cx_Oracle.makedsn(host=ip, port=puerto, sid=service_name)
    else:
        dsn = cx_Oracle.makedsn(host=ip, port=puerto, service_name=service_name)
    

    try:
        connection = cx_Oracle.connect(user=oracle_user, password=oracle_pass, dsn=dsn, encoding='UTF-8')
        return connection

    except Exception as e:
        raise HTTP(500, f"No se pudo conectar a Oracle: {str(e)}")


def get_oracle_connection_9i(ip, service_name, puerto):
    # Configurar conexión Oracle
    load_dotenv()
    oracle_user = os.getenv('ORACLE_USER')  # Valor por defecto solo para desarrollo
    oracle_pass = os.getenv('ORACLE_PASSWORD')
    dsn = cx_Oracle.makedsn(
        host=ip,
        port=puerto,
        sid=service_name,
        #service_name=service_name
        )
    try:
        connection = cx_Oracle.connect(
            user=oracle_user,
            password=oracle_pass,
            dsn=dsn,
            encoding='UTF-8'
        )
        return connection
    except Exception as e:
        raise HTTP(500, f"No se pudo conectar a Oracle 9i: {str(e)}")


