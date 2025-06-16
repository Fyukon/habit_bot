import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(name: str = "bot"):
    logs_dir = Path(__name__)
    logs_dir.mkdir(exist_ok=True)

    log_format = "[%(asctime)s] - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Файловый обработчик (ротация по дням)
    file_handler = logging.FileHandler(
        filename=logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(log_format))

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger
