import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"


def setup_logger(level: int = logging.INFO) -> None:
	"""Configura logs em arquivo (logs/app.log) e no console."""
	LOG_DIR.mkdir(parents=True, exist_ok=True)

	formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

	file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
	file_handler.setFormatter(formatter)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(formatter)

	root = logging.getLogger()
	root.setLevel(level)
	root.addHandler(file_handler)
	root.addHandler(console_handler)

	logging.getLogger(__name__).info("Logger inicializado — arquivo: %s", LOG_FILE.resolve())


logger = logging.getLogger(__name__)
