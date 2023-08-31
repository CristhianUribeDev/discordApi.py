from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)


def get_db():
    conn = psycopg2.connect(host='192.168.18.50',
                            dbname='postgres',
                            user='postgres',
                            password='123456@')
    return conn

@app.route('/')
def index():
    return "API FLASK IS UP!"

@app.route('/permitidos',methods=['POST'])
def obtenerPermitidos():
    conn = get_db()
    cursor = conn.cursor()
    query = "select n_coduser from dcuser where c_estper='P'"
    cursor.execute(query)
    rows = dictfetchall(cursor)
    cursor.close()
    conn.close()
    return rows


@app.route('/update_user',methods=['POST'])
def update_user():
    conn = get_db()
    cursor = conn.cursor()
    # Valor a verificar
    data = request.get_json()
    valor_verificar = data['userid']

    # Consulta para verificar si el registro existe
    consulta_verificacion = "SELECT * FROM dcuser WHERE N_CODUSER = %s"
    cursor.execute(consulta_verificacion, (valor_verificar,))
    existe_registro = cursor.fetchone()

    if existe_registro:
        print("El registro ya existe en la base de datos.")
        actualizacion = "UPDATE dcuser set C_NOMUSER = %s , C_ESTPER = %s where N_CODUSER = %s"
        cursor.execute(actualizacion, (data['nombre'],data['eleccion'],data['userid'],))
        conn.commit()

    else:
        # Insertar el registro si no existe
        consulta_insercion = "INSERT INTO dcuser (N_CODUSER,C_NOMUSER,C_ESTPER) VALUES (%s,%s,%s)"
        cursor.execute(consulta_insercion, (data['userid'],data['nombre'],data['eleccion'],))
        conn.commit()
        print("Registro insertado con éxito.")

    cursor.close()
    conn.close()
    return {"message": "¡Usuario actualizado con éxito!" }

@app.route('/dcuser',methods=['POST'])
def listar_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    data = request.get_json()
    query = "SELECT * FROM dcuser WHERE n_coduser = %s"
    condition_value = data['userid']
    cursor.execute(query, (condition_value,))
    rows = dictfetchall(cursor)
    cursor.close()
    conn.close()
    return rows


def dictfetchall(cursor):
    """
    Retorna los resultados de una consulta como una lista de diccionarios.
    Cada fila es un diccionario con nombres de columna como claves.
    """
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)