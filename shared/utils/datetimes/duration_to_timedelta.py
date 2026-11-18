from datetime import timedelta

from shared.utils.datetimes.parse_duration import parse_duration


def duration_to_timedelta(duration: str) -> timedelta:
    return timedelta(milliseconds=parse_duration(duration))