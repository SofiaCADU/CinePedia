from flask import Flask, render_template
import os
from datetime import datetime, date
from base.controllers.usuarios import bp as usuarios_bp
from base.controllers.peliculas import bp as peliculas_bp
from base.controllers import comentarios

def format_date(value, format='%Y-%m-%d'):
    if value is None:
        return ""
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime(format)
            except ValueError:
                continue
        return value
    if isinstance(value, (datetime, date)):
        return value.strftime(format)
    return str(value)

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DEBUG=os.environ.get("FLASK_DEBUG", "1") in ("1", "true", "True"),
    )

    app.register_blueprint(usuarios_bp)
    app.register_blueprint(peliculas_bp)
    app.register_blueprint(comentarios.bp)
    app.add_template_filter(format_date, "format_date")

    @app.route('/')
    def index():
        return render_template('auth.html')

    return app