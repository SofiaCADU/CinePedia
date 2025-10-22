# base/models/usuario.py

from base.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DB_NAME = 'certificación_sofia'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password = data.get('password')
        self.create_at = data.get('create_at') or data.get('created_at')
        self.update_at = data.get('update_at') or data.get('updated_at')

    @classmethod
    def guardar(cls, form):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password, create_at, update_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());
        """
        nuevo_id = connectToMySQL(DB_NAME).query_db(query, form)
        return nuevo_id

    @staticmethod
    def validar_usuarios(form):
        is_valid = True
        if len(form.get('nombre', '')) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if len(form.get('apellido', '')) < 2:
            flash('El apellido debe tener al menos 2 caracteres', "register")
            is_valid = False
        if not EMAIL_REGEX.match(form.get('email', '')):
            flash('Email inválido', "register")
            is_valid = False
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL(DB_NAME).query_db(query, {'email': form.get('email', '')})
        if result and len(result) >= 1:
            flash('Correo ya registrado', "register")
            is_valid = False
        if len(form.get('password', '')) < 3:
            flash('La contraseña debe tener al menos 3 caracteres.', "register")
            is_valid = False
        if form.get('password', '') != form.get('confirm', ''):
            flash('Las contraseñas no coinciden.', "register")
            is_valid = False
        return is_valid

    @classmethod
    def obtener_por_email(cls, form):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        params = form if isinstance(form, dict) else {'email': form}
        result = connectToMySQL(DB_NAME).query_db(query, params)
        if result and len(result) >= 1:
            return cls(result[0])
        return None

    @classmethod
    def obtener_por_id(cls, id_data):
        data = id_data if isinstance(id_data, dict) else {'id': id_data}
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if results and len(results) > 0:
            return cls(results[0])
        return None