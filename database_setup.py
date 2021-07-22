import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# We will add classes here
class Libro(Base):
    __tablename__ = 'libro'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(250), nullable=False)
    autor = Column(String(250), nullable=False)
    genero = Column(String(250))

    @property
    def serialize(self):
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'genero': self.genero,
            'id': self.id,
        }


# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///libros.db')
Base.metadata.create_all(engine)
