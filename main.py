# -*- coding: utf-8 -*-
from app import create_app, db
from app.models import User, Post
from app.main.email import send_message

application = create_app()

if __name__ == "__main__":
    application.run(debug=True, threaded=True)