# base/models/comentario.py

from base.config.mysqlconnection import connectToMySQL
from flask import flash

DB_NAME = 'certificación_sofia'

class Comentario:
    def __init__(self, data):
        self.id = data.get('id')
        self.pelicula_id = data.get('pelicula_id')
        self.usuario_id = data.get('usuario_id')
        self.contenido = data.get('contenido')
        self.create_at = data.get('create_at') or data.get('created_at')
        self.update_at = data.get('update_at') or data.get('updated_at')
        # Datos del usuario que hizo el comentario (si vienen del JOIN)
        self.usuario_nombre = data.get('usuario_nombre')
        self.usuario_apellido = data.get('usuario_apellido')

    @classmethod
    def obtener_por_pelicula(cls, pelicula_id):
        """Obtiene todos los comentarios de una película con información del usuario"""
        query = """
            SELECT c.*, u.nombre as usuario_nombre, u.apellido as usuario_apellido
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.pelicula_id = %(pelicula_id)s
            ORDER BY c.create_at DESC;
        """
        data = {'pelicula_id': pelicula_id}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        comentarios = []
        if results:
            for row in results:
                comentarios.append(cls(row))
        return comentarios

    @classmethod
    def guardar(cls, form):
        """Guarda un nuevo comentario"""
        query = """
            INSERT INTO comentarios (pelicula_id, usuario_id, contenido, create_at, update_at)
            VALUES (%(pelicula_id)s, %(usuario_id)s, %(contenido)s, NOW(), NOW());
        """
        return connectToMySQL(DB_NAME).query_db(query, form)

    @classmethod
    def borrar(cls, comentario_id):
        """Elimina un comentario"""
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        data = {'id': comentario_id}
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def obtener_uno(cls, comentario_id):
        """Obtiene un comentario específico"""
        query = "SELECT * FROM comentarios WHERE id = %(id)s LIMIT 1;"
        data = {'id': comentario_id}
        result = connectToMySQL(DB_NAME).query_db(query, data)
        if result and len(result) > 0:
            return cls(result[0])
        return None

    @staticmethod
    def validar_comentario(form):
        """Valida los datos del comentario"""
        is_valid = True
        contenido = form.get('contenido') or ''
        if not contenido or len(contenido.strip()) < 3:
            flash('El comentario debe tener al menos 3 caracteres', 'comentario_error')
            is_valid = False
        return is_valid