from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Libro

# Connect to Database and create database session
engine = create_engine('sqlite:///libros.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()






@app.route("/termino")
def termino():
    return render_template("terminos.html")

@app.route("/nos")
def nos():
    return render_template("nosotros.html")

# landing page that will display all the books in our database
# This function will operate on the Read operation.
@app.route('/')
@app.route('/libros')
def mostrarLibros():
    libros = session.query(Libro).all()
    return render_template('libros.html', libros=libros)


# This will let us Create a new book and save it in our database
@app.route('/libros/nuevo/', methods=['GET', 'POST'])
def nuevoLibro():
    if request.method == 'POST':
        nuevoLibro = Libro(titulo=request.form['nombre'],
                       autor=request.form['autor'],
                       genero=request.form['genero'])
        session.add(nuevoLibro)
        session.commit()
        return redirect(url_for('mostrarLibros'))
    else:
        return render_template('nuevoLibro.html')


# This will let us Update our books and save it in our database
@app.route("/libros/<int:libro_id>/editar/", methods=['GET', 'POST'])
def editarLibro(libro_id):
    libroEditado = session.query(Libro).filter_by(id=libro_id).one()
    if request.method == 'POST':
        if request.form['nombre']:
            libroEditado.titulo = request.form['nombre']
            libroEditado.autor = request.form['autor']
            libroEditado.genero = request.form['genero']
            session.commit()
        return redirect(url_for('mostrarLibros'))
    else:
        return render_template('editarLibro.html', libro=libroEditado)


# This will let us Delete our book
@app.route('/libros/<int:libro_id>/eliminar/', methods=['GET', 'POST'])
def eliminarLibro(libro_id):
    libroAEliminar = session.query(Libro).filter_by(id=libro_id).one()
    if request.method == 'POST':
        session.delete(libroAEliminar)
        session.commit()
        return redirect(url_for('mostrarLibros', libro_id=libro_id))
    else:
        return render_template('eliminarLibro.html', libro=libroAEliminar)


"""
api functions
"""
from flask import jsonify


def obtener_libros():
    libros = session.query(Libro).all()
    return jsonify(libros=[b.serialize for b in libros])


def obtener_libro(libro_id):
    libros = session.query(Libro).filter_by(id=libro_id).one()
    return jsonify(libros=libros.serialize)


def crearUnNuevoLibro(titulo, autor, genero):
    libroagregado = Libro(titulo=titulo, autor=autor, genero=genero)
    session.add(libroagregado)
    session.commit()
    return jsonify(Libro=libroagregado.serialize)


def actualizarLibro(id, titulo, autor, genero):
    libroEditado = session.query(Libro).filter_by(id=id).one()
    if not titulo:
        libroEditado.titulo = titulo
    if not autor:
        libroEditado.autor = autor
    if not genero:
        libroEditado.genero = genero
    session.add(libroEditado)
    session.commit()
    return 'Se actualizó el libro con el id %s' % id


def eliminarUnLibro(id):
    libroAEliminar = session.query(Libro).filter_by(id=id).one()
    session.delete(libroAEliminar)
    session.commit()
    return 'Se eliminó el libro con el id %s' % id


@app.route('/')
@app.route('/librosApi', methods=['GET', 'POST'])
def funcionLibros():
    if request.method == 'GET':
        return obtener_libros()
    elif request.method == 'POST':
        titulo = request.args.get('titulo', '')
        autor = request.args.get('autor', '')
        genero = request.args.get('genero', '')
        return crearUnNuevoLibro(titulo, autor, genero)


@app.route('/librosApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def funcionLibrosId(id):
    if request.method == 'GET':
        return obtener_libro(id)

    elif request.method == 'PUT':
        titulo = request.args.get('titulo', '')
        autor = request.args.get('autor', '')
        genero = request.args.get('genero', '')
        return actualizarLibro(id, titulo, autor, genero)

    elif request.method == 'DELETE':
        return eliminarUnLibro(id)


if __name__ == '__main__':
    app.run(debug=True)