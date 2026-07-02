from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if "usuario_id" not in session:

            print("usuario não logado")

            flash("Faça login para continuar.", "error")

            return redirect(url_for("admin.login"))

        print("usuario logado")
        return func(*args, **kwargs)

    return decorated_function