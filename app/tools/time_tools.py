from datetime import datetime, timedelta


def now_in_milliseconds() -> int:
    return int(datetime.now().timestamp() * 1000)


def now_in_seconds() -> int:
    return int(datetime.now().timestamp())


def in_one_month() -> int:
    next_month = datetime.now() + timedelta(days=30)
    return int(next_month.timestamp())
