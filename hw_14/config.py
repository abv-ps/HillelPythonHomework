# config.py
# This file contains configuration settings for the application.

import os
from pathlib import Path
from typing import Tuple


class Config:
    """
    Клас Config зберігає конфігураційні параметри для програми.

    Атрибути:
        BASE_URL (str): Шаблон URL для сторінок новин.

        PAGE_RANGE (Tuple[int, int]): Діапазон сторінок для обробки.
    """
    BASE_URL: str = "https://www.rbc.ua/rus/news/{page}"
    PAGE_RANGE: Tuple[int, int] = (1, 24)
    PLOT_DIR: str = os.path.join(os.getcwd(), 'plots')
