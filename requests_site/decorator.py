from functools import wraps
from threading import Thread

from flask import abort
from flask_login import current_user


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            abort(403)
        return func(*args, **kwargs)

    return wrapper


def run_async(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper