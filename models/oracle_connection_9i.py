from gluon.contrib.pymysql import connect
import cx_Oracle

def get_oracle_connection_9i(ip, service_name, puerto,  ver):
  # Configurar conexión Oracle
    if ver == 9:
        dsn = cx_Oracle.makedsn(
            host=ip,
            port=puerto,
            sid=service_name
            )
    else:
        dsn = cx_Oracle.makedsn(
            host=ip,
            port=puerto,
            service_name=service_name
            )
    try:
        connection = cx_Oracle.connect(
            user='faduran',
            password='Caracas2024',
            dsn=dsn,
            encoding='UTF-8'
        )
        return connection
    except Exception as e:
        raise HTTP(500, f"No se pudo conectar a Oracle: {str(e)}")

