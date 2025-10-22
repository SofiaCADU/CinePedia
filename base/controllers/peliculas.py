# base/controllers/peliculas.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
from base.models.pelicula import Pelicula
from base.controllers.usuarios import login_requerido

bp = Blueprint('peliculas', __name__, url_prefix='/peliculas')

@bp.route('/')
@bp.route('/dashboard')
@login_requerido
def index():
    peliculas = Pelicula.obtener_todos()
    return render_template('dashboard.html', peliculas=peliculas)

@bp.route('/nueva', methods=['GET', 'POST'])
@login_requerido
def nueva_pelicula():
    if request.method == 'POST':
        if not Pelicula.validar_pelicula(request.form):
            return render_template('nueva_pelicula.html', form=request.form)
        data = {
            'usuario_id': session['usuario_id'],
            'titulo': request.form.get('titulo'),
            'sinopsis': request.form.get('sinopsis'),
            'director': request.form.get('director'),
            'fecha_estreno': request.form.get('fecha_estreno'),
        }
        Pelicula.guardar(data)
        flash("¡Película guardada con éxito!", "success")
        return redirect(url_for('peliculas.index'))
    return render_template('nueva_pelicula.html')

@bp.route('/<int:pelicula_id>')
@login_requerido
def mostrar_pelicula(pelicula_id):
    pelicula = Pelicula.obtener_uno(pelicula_id)
    if not pelicula:
        flash("Película no encontrada.", "warning")
        return redirect(url_for('peliculas.index'))
    
    from base.models.comentario import Comentario
    comentarios = Comentario.obtener_por_pelicula(pelicula_id)
    
    return render_template('mostrar_pelicula.html', pelicula=pelicula, comentarios=comentarios)

@bp.route('/<int:pelicula_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_pelicula(pelicula_id):
    pelicula = Pelicula.obtener_uno(pelicula_id)
    if not pelicula:
        flash("Película no encontrada para editar.", "warning")
        return redirect(url_for('peliculas.index'))

    if pelicula.usuario_id != session['usuario_id']:
        flash("No tienes permiso para editar esta película.", "warning")
        return redirect(url_for('peliculas.index'))

    if request.method == 'POST':
        if not Pelicula.validar_pelicula(request.form, pelicula_id):
            return render_template('editar_pelicula.html', pelicula=pelicula, form=request.form)
        data = {
            'id': pelicula_id,
            'titulo': request.form.get('titulo'),
            'sinopsis': request.form.get('sinopsis'),
            'director': request.form.get('director'),
            'fecha_estreno': request.form.get('fecha_estreno'),
        }
        Pelicula.actualizar(data)
        flash("Película actualizada con éxito.", "success")
        return redirect(url_for('peliculas.mostrar_pelicula', pelicula_id=pelicula_id))

    return render_template('editar_pelicula.html', pelicula=pelicula)

@bp.route('/<int:pelicula_id>/actualizar', methods=['POST'])
@login_requerido
def actualizar_pelicula(pelicula_id):
    return editar_pelicula(pelicula_id)

@bp.route('/<int:pelicula_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_pelicula(pelicula_id):
    pelicula = Pelicula.obtener_uno(pelicula_id)
    if not pelicula:
        flash("Película no encontrada.", "warning")
        return redirect(url_for('peliculas.index'))
    
    if pelicula.usuario_id != session['usuario_id']:
        flash("No tienes permiso para eliminar esta película.", "warning")
        return redirect(url_for('peliculas.index'))
    
    Pelicula.borrar(pelicula_id)
    flash("Película eliminada con éxito", "success")
    return redirect(url_for('peliculas.index'))