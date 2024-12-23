import os
from datetime import datetime

LOG_FOLDER = 'log'


def log(origin, msg):
    current_date = datetime.now().strftime('%d-%m-%Y')

    os.makedirs(LOG_FOLDER, exist_ok=True)
    log_filename = os.path.join(LOG_FOLDER, f'log_{current_date}.txt')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    log_message = f'[{current_time}] {origin} | {msg}\n'

    with open(log_filename, 'a') as log_file:
        log_file.write(log_message)

    print(log_message)
