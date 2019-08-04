from datetime import datetime


def date_bounds(date_range):
    start, end = date_range.split('-')

    if start:
        start = start.strip()
        start = datetime.strptime(start, '%d.%m.%Y %H:%M')

    if end:
        end = end.strip()
        end = datetime.strptime(end, '%d.%m.%Y %H:%M')

    return start, end
