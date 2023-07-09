
from logging import Formatter, getLogger, INFO, Logger, StreamHandler

# Initialize the logger
LOGGER_NAME: str = "spaceinvaders"
logger: Logger = getLogger(LOGGER_NAME)
logger.setLevel(INFO)
console_handler: StreamHandler = StreamHandler()
formatter: Formatter = Formatter("%(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
