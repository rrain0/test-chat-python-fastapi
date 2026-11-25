from datetime import timedelta

from shared.utils.datetimes.parse_duration import parse_duration


def duration(duration_str: str) -> timedelta:
    return timedelta(milliseconds=parse_duration(duration_str))
