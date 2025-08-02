from datetime import datetime, timezone


def int_to_datetime(value: int | float, tz=timezone.utc) -> datetime:
    if not isinstance(value, (int, float)):
        raise ValueError("Value isn't a number (epoch time).")

    length = len(str(int(value)))
    if length > 13:
        raise ValueError("Timestamp unvalid.")
    divisor = 1000 if length > 10 else 1
    return datetime.fromtimestamp(value / divisor, tz=tz)
