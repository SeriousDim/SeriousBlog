# -*- coding: utf-8 -*-
from app import my_app, db
from app.models import User, Post

if __name__ == "__main__":
    my_app.run(debug=False, threaded=True)