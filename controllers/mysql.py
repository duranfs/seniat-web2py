# applications/seniat_python3/test_mysql_detailed_pymysql.py
import sys
import socket
sys.path.append('C:/web2py_312')

def test_mysql_detailed():
    """Prueba detallada de conexión MySQL usando PyMySQL"""
    print("=== DIAGNÓSTICO DETALLADO MySQL (PyMySQL) ===")
    
    # Parámetros de conexión (ajusta estos valores)
    host = "172.17.17.97"  # La IP que respondió al ping
    port = 3306
    user = "faduran"          # Cambia por tu usuario
    password = "Caracas2024"  # Cambia por tu password
    database = "rrhh_com_ve_php"
    
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    print(f"Usuario: {user}")
    print(f"Base de datos: {database}")
    
    # 1. Verificar conectividad de red
    print("\n1. Verificando conectividad de red...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print("✅ Puerto 3306 accesible")
        else:
            print(f"❌ Puerto 3306 cerrado o inaccesible (error: {result})")
        sock.close()
    except Exception as e:
        print(f"❌ Error de socket: {e}")
    
    # 2. Verificar si PyMySQL está instalado
    print("\n2. Verificando instalación de PyMySQL...")
    try:
        import pymysql
        print("✅ PyMySQL instalado")
    except ImportError:
        print("❌ PyMySQL NO instalado")
        print("Ejecuta: pip install pymysql")
        return False
    
    # 3. Intentar conexión directa
    print("\n3. Intentando conexión directa...")
    try:
        import pymysql
        
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connect_timeout=10
        )
        
        print("✅ Conexión directa exitosa!")
        
        # Hacer una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION(), NOW(), USER()")
        result = cursor.fetchone()
        
        print(f"   MySQL Version: {result[0]}")
        print(f"   Current Time: {result[1]}")
        print(f"   Current User: {result[2]}")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"❌ Error operacional: {e}")
        print("   Verifica usuario/contraseña o que MySQL esté ejecutándose")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    return False

if __name__ == "__main__":
    test_mysql_detailed()
