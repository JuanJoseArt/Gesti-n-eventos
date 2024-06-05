from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '123456'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_eventos'

mysql = MySQL(app)

# Rutas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Eventos")
    if result_value > 0:
        eventos = cur.fetchall()
        return render_template('index.html', eventos=eventos)
    return render_template('index.html')

@app.route('/consul_usuario')
def index_usuario():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Usuarios")
    if result_value > 0:
        usuarios = cur.fetchall()
        return render_template('consulta_usuario.html', usuarios=usuarios)
    return render_template('consulta_usuario.html')

@app.route('/add_evento', methods=['GET', 'POST'])
def add_evento():
    if request.method == 'POST':
        evento_details = request.form
        nombre = evento_details['nombre']
        descripcion = evento_details['descripcion']
        fecha = evento_details['fecha']
        ubicacion = evento_details['ubicacion']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Eventos(nombre, descripcion, fecha, ubicacion) VALUES(%s, %s, %s, %s)", 
                    (nombre, descripcion, fecha, ubicacion))
        mysql.connection.commit()
        cur.close()
        flash('Evento Agregado Satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('evento_add.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_details = request.form
        nombre = user_details['nombre']
        email = user_details['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Usuarios(nombre, email) VALUES(%s, %s)", (nombre, email))
        mysql.connection.commit()
        cur.close()
        flash('Usuario Agregado Satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_add.html')

@app.route('/edit_evento/<int:id>', methods=['GET', 'POST'])
def edit_evento(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Eventos WHERE id = %s", [id])
    evento = cur.fetchone()
    if request.method == 'POST':
        evento_details = request.form
        nombre = evento_details['nombre']
        descripcion = evento_details['descripcion']
        fecha = evento_details['fecha']
        ubicacion = evento_details['ubicacion']
        cur.execute("UPDATE Eventos SET nombre = %s, descripcion = %s, fecha = %s, ubicacion = %s WHERE id = %s", 
                    (nombre, descripcion, fecha, ubicacion, id))
        mysql.connection.commit()
        cur.close()
        flash('Evento actualizado satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('evento_edit.html', evento=evento)

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE id = %s", [id])
    usuario = cur.fetchone()
    if request.method == 'POST':
        user_details = request.form
        nombre = user_details['nombre']
        email = user_details['email']
        
        cur.execute("UPDATE Usuarios SET nombre = %s, email = %s WHERE id = %s", 
                    (nombre, email, id))
        mysql.connection.commit()
        cur.close()
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_edit.html', usuario=usuario)

@app.route('/delete_evento/<int:id>', methods=['POST'])
def delete_evento(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Eventos WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Evento eliminado satisfactoriamente')
    return redirect(url_for('index'))

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Usuarios WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Usuario eliminado satisfactoriamente')
    return redirect(url_for('index_usuario'))

@app.route('/participaciones')
def participaciones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.id, u.nombre as usuario_nombre, e.nombre as evento_nombre, p.rol "
                "FROM Participaciones p "
                "JOIN Usuarios u ON p.id_usuario = u.id "
                "JOIN Eventos e ON p.id_evento = e.id")
    participaciones1 = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Eventos")
    eventos1 = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Usuarios")
    usuarios1 = cur.fetchall()

    cur.close()
    return render_template('participaciones.html', participaciones=participaciones1, eventos=eventos1, usuarios=usuarios1)

@app.route('/participaciones/agregar', methods=['GET', 'POST'])
def agregar_participacion():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        id_evento = request.form['id_evento']
        rol = request.form['rol']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Participaciones (id_usuario, id_evento, rol) VALUES (%s, %s, %s)",
                    (id_usuario, id_evento, rol))
        mysql.connection.commit()
        cur.close()
        flash('Participación agregada satisfactoriamente')
        return redirect(url_for('participaciones'))
    return render_template('participaciones_add.html')

@app.route('/edit_participacion/<int:id>', methods=['GET', 'POST'])
def edit_participacion(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Participaciones WHERE id = %s", [id])
    participacion = cur.fetchone()

    cur.execute("SELECT id, nombre FROM Eventos")
    eventos1 = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Usuarios")
    usuarios1 = cur.fetchall()

    if request.method == 'POST':
        participacion_details = request.form
        id_usuario = participacion_details['id_usuario']
        id_evento = participacion_details['id_evento']
        rol = participacion_details['rol']
        
        cur.execute("UPDATE Participaciones SET id_usuario = %s, id_evento = %s, rol = %s WHERE id = %s", 
                    (id_usuario, id_evento, rol, id))
        mysql.connection.commit()
        cur.close()
        flash('Participación actualizada satisfactoriamente')
        return redirect(url_for('participaciones'))
    return render_template('edit_participacion.html', participacion=participacion, eventos=eventos1, usuarios=usuarios1)

if __name__ == '__main__':
    app.run(debug=True)
