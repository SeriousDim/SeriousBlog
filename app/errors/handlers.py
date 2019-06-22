from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']

@bp.errorhandler(404)
def error404(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template("errors/error.html", number=404, description="Страница не найдена"), 404
    
@bp.errorhandler(500)
def error500(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template("errors/error.html", number=500, description="Внутренняя ошибка сервера. Извините<br>Изменения отменены"), 500