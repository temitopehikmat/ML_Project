import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs", LOG_FILE)# cwd indicates current working directory
os.makedirs(logs_path, exist_ok=True) # this state that even thouh there is file or folder keep on appending the files inside that whenever we want to create a file

LOG_FILE_PATH=os.path.join(logs_path, LOG_FILE)

# when creating the log, and want to overwrite the functionality of the logging, there is need to set it up in basicConfig
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", # %(asctime)s-timestamp, (lineno)d-line number
    level=logging.INFO,
   
)
