from functools import wraps

from flask import session
from flask.templating import render_template


def login(username, password):
    session["role"] = "admin"


def logout():
    session.pop("role", None)


def requiresAdmin(func):
    @wraps(func)
    def functionWrapper(*args, **kwargs):
        if session.get("role", "guest") == "admin":
            return func(*args, **kwargs)
        return render_template(session.get("role", "guest"), page="index")

    return functionWrapper


def requiresStudent(func):
    @wraps(func)
    def functionWrapper(*args, **kwargs):
        if session.get("role", "guest") == "student":
            return func(*args, **kwargs)
        return render_template(session.get("role", "guest"), page="index")

    return functionWrapper
