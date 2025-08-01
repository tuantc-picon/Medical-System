from datetime import datetime, timezone


def int_to_datetime(value: int, tz=timezone.utc) -> datetime:
    if not isinstance(value, int):
        raise ValueError("Value isn't int (epoch time).")

    length = len(str(value))
    if length > 13:
        raise ValueError("Timestamp unvalid.")

    if length > 10:
        # milliseconds
        return datetime.fromtimestamp(value / 1000, tz=tz)
    else:
        # seconds
        return datetime.fromtimestamp(value, tz=tz)
