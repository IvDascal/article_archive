from datetime import datetime
from functools import wraps

from flask import url_for, flash, g
from werkzeug.utils import redirect


def date_bounds(date_range):
    start, end = date_range.split('-')

    if start:
        start = start.strip()
        start = datetime.strptime(start, '%d.%m.%Y %H:%M')

    if end:
        end = end.strip()
        end = datetime.strptime(end, '%d.%m.%Y %H:%M')

    return start, end


def check_permission(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user and g.user.is_admin:
            return func(*args, **kwargs)
        else:
            flash('Permission denied')
            return redirect(url_for('index'))

    return wrapper
