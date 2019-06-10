from flask import render_template
from app import my_app, db

@my_app.errorhandler(404)
def error404(error):
    return render_template("error.html", number=404, description="Страница не найдена"), 404
    
@my_app.errorhandler(500)
def error500(error):
    db.session.rollback()
    return render_template("error.html", number=500, description="Внутренняя ошибка сервера. Извините\nИзменения отменены"), 500