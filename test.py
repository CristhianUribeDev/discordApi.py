import psycopg2

try:
    # Establecer la conexión a la base de datos
    connection = psycopg2.connect(
        host="192.168.18.50",
        dbname="postgres",
        user="postgres",
        password="123456@"
    )

    # Crear un cursor para realizar consultas
    cursor = connection.cursor()

    # Ejecutar una consulta simple para confirmar la conexión
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]

    # Imprimir la versión de PostgreSQL
    print("Conexión exitosa a PostgreSQL. Versión:", version)

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()

except psycopg2.Error as e:
    print("Error al conectar a PostgreSQL:", e)