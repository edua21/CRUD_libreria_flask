from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Let's import our Book and Base classes from our database_setup.py file
from database_setup import Libro, Base

# bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
engine = create_engine('sqlite:///libros.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.
session = DBSession()

# Create

libroUno = Libro(titulo="Yo Robor", autor="Isaac Asimov", genero="Ciencia Ficcion")
session.add(libroUno)
session.commit()

# Read

session.query(Libro).all()
session.query(Libro).first()

# Update
editarLibro = session.query(Libro).filter_by(id=1).one()
editarLibro.autor = "Isaac Asimov"
session.add(editarLibro)
session.commit()

# Delete

libroAEliminar = session.query(Libro).filter_by(titulo='Yo Robor').one()
session.delete(libroAEliminar)
session.commit()
