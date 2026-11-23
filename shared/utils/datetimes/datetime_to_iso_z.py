from datetime import datetime, timezone


# Outputs in format yyyy-MM-ddThh:mm:ss.SSSZ
def datetime_to_iso_z(dt: datetime):
    # If no timezone, then treat as UTC and set UTC
    if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
    # Else convert to UTC
    else: dt = dt.astimezone(timezone.utc)

    # timespec="milliseconds" gives exactly 3 digits of milliseconds (.000, .120 etc.)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
