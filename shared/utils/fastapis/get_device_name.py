from user_agents import parse


def get_device_name(device_str: str | None):
    if device_str == 'Telegram Bot': return 'Telegram Bot'

    # Парсим в красивое название устройства
    ua = parse(device_str)
    # Собираем строку вида: 'Chrome 120 (MacOS)'
    device_str = f'{ua.browser.family} {ua.browser.version_string} ({ua.os.family})'
    return device_str
