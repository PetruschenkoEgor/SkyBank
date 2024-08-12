import datetime
import requests
import logging
import os
from src.utils import get_data_from_excel, PATH_TO_FILE_EXCEL


# Файл, в который сохраняются логи
PATH_TO_FILE_FILE_HANDLER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "views.log")

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_FILE_HANDLER, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


