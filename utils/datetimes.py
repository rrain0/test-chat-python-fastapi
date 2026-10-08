import datetime
import re



def now() -> datetime.datetime:
  return datetime.datetime.now(datetime.timezone.utc)



def parse_duration(duration_str: str) -> float | int:
    if not duration_str:
        raise ValueError("Duration string cannot be empty")

    # Регулярное выражение для поиска целых и дробных чисел
    pattern = re.compile(
        r'^'
        r'(?:(?P<w>\d+(?:\.\d+)?)w)?'
        r'(?:(?P<d>\d+(?:\.\d+)?)d)?'
        r'(?:(?P<h>\d+(?:\.\d+)?)h)?'
        r'(?:(?P<m>\d+(?:\.\d+)?)m)?'
        r'(?:(?P<s>\d+(?:\.\d+)?)s)?'
        r'(?:(?P<ms>\d+(?:\.\d+)?)ms)?'
        r'$'
    )

    match = pattern.match(duration_str)

    if not match or match.group(0) == '':
        raise ValueError(
            f"Invalid duration format: '{duration_str}'. "
            f"Expected format like '1.5w2d3.5h4m5.2s600ms'. "
            f"Units must be in order (w, d, h, m, s, ms)."
        )

    parts = match.groupdict()

    # Извлекаем значения во float
    weeks        = float(parts['w'])  if parts['w']  else 0.0
    days         = float(parts['d'])  if parts['d']  else 0.0
    hours        = float(parts['h'])  if parts['h']  else 0.0
    minutes      = float(parts['m'])  if parts['m']  else 0.0
    seconds      = float(parts['s'])  if parts['s']  else 0.0
    milliseconds = float(parts['ms']) if parts['ms'] else 0.0

    # Считаем итоговое количество миллисекунд
    total_ms = (
        weeks * 7 * 24 * 60 * 60 * 1000 +
        days * 24 * 60 * 60 * 1000 +
        hours * 60 * 60 * 1000 +
        minutes * 60 * 1000 +
        seconds * 1000 +
        milliseconds
    )

    # Возвращаем int, если дробная часть нулевая, для более чистого вывода
    return int(total_ms) if total_ms.is_integer() else total_ms
