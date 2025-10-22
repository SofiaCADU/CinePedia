# base/controllers/comentarios.py

from flask import Blueprint, request, redirect, url_for, flash, session
from base.models.comentario import Comentario
from base.models.pelicula import Pelicula
from base.controllers.usuarios import login_requerido

bp = Blueprint('comentarios', __name__, url_prefix='/comentarios')

@bp.route('/crear/<int:pelicula_id>', methods=['POST'])
@login_requerido
def crear_comentario(pelicula_id):
    # Verificar que la película existe
    pelicula = Pelicula.obtener_uno(pelicula_id)
    if not pelicula:
        flash("Película no encontrada.", "warning")
        return redirect(url_for('peliculas.index'))
    
    # Verificar que el usuario NO sea el creador de la película
    if pelicula.usuario_id == session['usuario_id']:
        flash("No puedes comentar tu propia película.", "warning")
        return redirect(url_for('peliculas.mostrar_pelicula', pelicula_id=pelicula_id))
    
    # Validar el comentario
    if not Comentario.validar_comentario(request.form):
        return redirect(url_for('peliculas.mostrar_pelicula', pelicula_id=pelicula_id))
    
    # Guardar el comentario
    data = {
        'pelicula_id': pelicula_id,
        'usuario_id': session['usuario_id'],
        'contenido': request.form.get('contenido')
    }
    Comentario.guardar(data)
    flash("¡Comentario agregado con éxito!", "success")
    return redirect(url_for('peliculas.mostrar_pelicula', pelicula_id=pelicula_id))

@bp.route('/eliminar/<int:comentario_id>', methods=['POST'])
@login_requerido
def eliminar_comentario(comentario_id):
    # Obtener el comentario
    comentario = Comentario.obtener_uno(comentario_id)
    if not comentario:
        flash("Comentario no encontrado.", "warning")
        return redirect(url_for('peliculas.index'))
    
    # Verificar que el usuario sea el dueño del comentario
    if comentario.usuario_id != session['usuario_id']:
        flash("No tienes permiso para eliminar este comentario.", "warning")
        return redirect(url_for('peliculas.mostrar_pelicula', pelicula_id=comentario.pelicula_id))
    
    # Eliminar el comentario
    pelicula_id = comentario.pelicula_id
    Comentario.borrar(comentario_id)
    flash("Comentario eliminado con éxito.", "success")
    return redirect(url_for('peliculas.mostrar_pelicula', pelicula_id=pelicula_id))