import logging
import os 
from datetime import datetime


LOG_File = f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log"
log_path = os.path.join(os.getcwd(), "logs")

os.makedirs(log_path, exist_ok=True)

Log_File_PATH = os.path.join(log_path, LOG_File)

logging.basicConfig(level=logging.INFO,
        filename=Log_File_PATH,
        format='[%(asctime)s] %(levelname)s - %(message)s')