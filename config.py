"""Configuration settings for the parking zones application."""
from typing import Dict, List, Tuple

# Map center point (latitude, longitude)
TARGET_POINT: Tuple[float, float] = (45.38096, 20.39373)

# Map settings
MAP_RADIUS_METERS: int = 5000
MAP_FILENAME: str = "parking_map.html"

# Parking zone definitions
PARKING_ZONES: Dict[str, List[str]] = {
    "red": [
        "Пупинова", "Светосавска", "Јеврејска", "Гимназијска",
        "Краља Александра Првог Карађорђевића", "Краља Петра Првог",
        "Сарајлијина", "Немањина", "Др Славка Жупанског"
    ],
    "yellow": [
        "Слободана Бурсаћа", "Савезничка", "Цара Душана", "Мирослава Тирша"
    ],
    "green": [
        "Кеј другог октобра", "Обала Соње Маринковић", "Обилићева",
        "Петефијева", "Даничићева", "Марка Орешковића", "Иве Лоле Рибара",
        "Косте Абрашевића", "20. октобра", "Југ Богдана", "Саве Текелије"
    ]
}

# Map visualization settings
ZONE_COLORS = {
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "green": "#00FF00"
}

# Map marker settings
MARKER_SETTINGS = {
    "location": TARGET_POINT,
    "popup": "Центар",
    "color": "blue",
    "icon": "info-sign"
}
