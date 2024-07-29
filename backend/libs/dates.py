import datetime

UTC = datetime.timezone.utc


def get_utcnow() -> datetime.datetime:
    """Helper to addresses two issues:
    - the fact datetimes are timezone-naive by default
    - the fact we can't mock datetime.utcnow() because it is a built-in written in C
    """
    return datetime.datetime.now(tz=UTC)


def seconds_to_hms(seconds):
    """Convert seconds to hours, minutes, seconds."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
