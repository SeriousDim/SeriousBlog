from flask import render_template
from app import db
from app.errors import bp

@bp.errorhandler(404)
def error404(error):
    return render_template("errors/error.html", number=404, description="Страница не найдена"), 404
    
@bp.errorhandler(500)
def error500(error):
    db.session.rollback()
    return render_template("errors/error.html", number=500, description="Внутренняя ошибка сервера. Извините<br>Изменения отменены"), 500