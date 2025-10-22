# base/controllers/usuarios.py

import functools # Sirve para decorar funciones
import re
import sys
from flask import Blueprint, render_template, request, redirect, session, flash, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from base.models.usuario import Usuario

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/registrar', methods=['POST'])
def registrar():
    form = request.form
    if not Usuario.validar_usuarios(form):
        return redirect(url_for('index'))

    try:
        password_hash = generate_password_hash(form.get('password'))
        data = {
            'nombre': form.get('nombre'),
            'apellido': form.get('apellido'),
            'email': form.get('email'),
            'password': password_hash
        }
        nuevo_id = Usuario.guardar(data)
        print('DEBUG: nuevo_id ->', nuevo_id, file=sys.stderr)
        session['usuario_id'] = nuevo_id
        flash('¡Usuario registrado!', 'success')
        return redirect(url_for('usuarios.dashboard'))
    except Exception as e:
        err = str(e)
        print('ERROR registrar usuario:', err, file=sys.stderr)
        flash('Error al registrar usuario', 'register')
        return redirect(url_for('index'))

@bp.route('/login', methods=['POST'])
def login():
    form = request.form
    email = form.get('email')
    password = form.get('password')

    usuario = Usuario.obtener_por_email({'email': email})
    if not usuario:
        flash('Usuario o contraseña incorrecta', "login")
        return redirect(url_for('index'))

    if not check_password_hash(usuario.password, password):
        flash('Usuario o contraseña incorrecta', "login")
        return redirect(url_for('index'))

    session['usuario_id'] = usuario.id
    return redirect(url_for('usuarios.dashboard'))

@bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    usuario = Usuario.obtener_por_id({'id': session['usuario_id']})
    # recuperar películas si quieres mostrarlas en dashboard (modelo Pelicula)
    from base.models.pelicula import Pelicula
    peliculas = Pelicula.obtener_todos() if Pelicula else []
    return render_template('dashboard.html', usuario=usuario, peliculas=peliculas)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def cargar_usuario_logueado():
    usuario_id = session.get('usuario_id')
    if usuario_id is None:
        g.user = None
    else:
        g.user = Usuario.obtener_por_id({'id': usuario_id})

def login_requerido(view):
    from functools import wraps
    @wraps(view)
    def vista_envuelta(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    return vista_envuelta