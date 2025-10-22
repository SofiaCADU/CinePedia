# base/models/pelicula.py

from base.config.mysqlconnection import connectToMySQL
from flask import flash

DB_NAME = 'certificación_sofia'

class Pelicula:
    def __init__(self, data):
        self.id = data.get('id')
        self.usuario_id = data.get('usuario_id')
        self.titulo = data.get('titulo')
        self.sinopsis = data.get('sinopsis')
        self.director = data.get('director')
        self.fecha = data.get('fecha_estreno') or data.get('fecha_estreno')
        self.create_at = data.get('create_at') or data.get('created_at')
        self.update_at = data.get('update_at') or data.get('updated_at')

    @classmethod
    def obtener_todos(cls):
        query = "SELECT id, usuario_id, titulo, sinopsis, director, fecha_estreno, create_at, update_at FROM peliculas ORDER BY create_at DESC;"
        results = connectToMySQL(DB_NAME).query_db(query)
        peliculas = []
        if results:
            for row in results:
                peliculas.append(cls(row))
        return peliculas

    @classmethod
    def obtener_uno(cls, pelicula_id):
        query = "SELECT id, usuario_id, titulo, sinopsis, director, fecha_estreno, create_at, update_at FROM peliculas WHERE id = %(id)s LIMIT 1;"
        data = {'id': pelicula_id}
        result = connectToMySQL(DB_NAME).query_db(query, data)
        if result and len(result) > 0:
            return cls(result[0])
        return None

    @classmethod
    def guardar(cls, form):
        query = "INSERT INTO peliculas (usuario_id, titulo, sinopsis, director, fecha_estreno, create_at, update_at) VALUES (%(usuario_id)s, %(titulo)s, %(sinopsis)s, %(director)s, %(fecha_estreno)s, NOW(), NOW());"
        return connectToMySQL(DB_NAME).query_db(query, form)

    @classmethod
    def actualizar(cls, data):
        query = "UPDATE peliculas SET titulo=%(titulo)s, sinopsis=%(sinopsis)s, director=%(director)s, fecha_estreno=%(fecha_estreno)s, update_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def borrar(cls, pelicula_id):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        data = {'id': pelicula_id}
        return connectToMySQL(DB_NAME).query_db(query, data)

    @staticmethod
    def validar_pelicula(form, pelicula_id=None):
        is_valid = True
        titulo = form.get('titulo') or ''
        if not titulo or len(titulo.strip()) < 3:
            flash('El título de la película debe tener al menos 3 caracteres', 'pelicula_error')
            is_valid = False
        else:
            if pelicula_id:
                query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s AND id != %(id)s;"
                data = {'titulo': titulo, 'id': pelicula_id}
            else:
                query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s;"
                data = {'titulo': titulo}
            
            result = connectToMySQL(DB_NAME).query_db(query, data)
            if result and len(result) >= 1:
                flash('Error, esta película ya fue creada, inténtalo de nuevo', 'pelicula_error')
                is_valid = False
        
        sinopsis = form.get('sinopsis') or ''
        if not sinopsis or len(sinopsis.strip()) < 3:
            flash('La sinopsis de la película debe tener al menos 3 caracteres', 'pelicula_error')
            is_valid = False
        director = form.get('director') or ''
        if not director or len(director.strip()) < 3:
            flash('El director de la película debe tener al menos 3 caracteres', 'pelicula_error')
            is_valid = False
        return is_valid