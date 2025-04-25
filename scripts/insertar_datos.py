import mysql.connector
from mysql.connector import Error

config = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'admin',  
    'database': 'BioNetDB'
}

def conectar_mysql():
    """Conectar a MySQL"""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("Conexión exitosa a MySQL")
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def insertar_datos(conn):
    """Insertar datos en la tabla resultados_examenes"""
    cursor = conn.cursor()
    query = """
    INSERT IGNORE INTO resultados_examenes (laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen)
    VALUES
    (1, 1001, 'Hemoglobina', '13.5', '2024-04-20'),
    (1, 1002, 'Glucosa', '95', '2024-04-20');
    """
    
    try:
        cursor.execute(query)
        conn.commit()  
        print("Datos insertados correctamente")
    except Error as e:
        print(f"Error al insertar datos: {e}")

def consultar_datos(conn):
    """Consultar datos de las tablas"""
    cursor = conn.cursor()
    query = "SELECT * FROM resultados_examenes;"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Resultados en la tabla 'resultados_examenes':")
    for row in rows:
        print(row)

    query_log = "SELECT * FROM log_cambios_resultados;"
    cursor.execute(query_log)
    log_rows = cursor.fetchall()
    print("\nLog de cambios:")
    for log in log_rows:
        print(log)

if __name__ == "__main__":
    conn = conectar_mysql()
    
    if conn:
        insertar_datos(conn)
        
        consultar_datos(conn)
        
        conn.close()
