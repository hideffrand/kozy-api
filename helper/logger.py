import os
from datetime import datetime
LOG_FOLDER = 'tmp/log'


def log(origin, msg):
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    log_message = f'[{current_time}] {origin} | {msg}\n'

    if os.getenv('DEBUG') == 'True':
        os.makedirs(LOG_FOLDER, exist_ok=True)
        log_filename = os.path.join(LOG_FOLDER, f'log_{current_date}.txt')
        with open(log_filename, 'a') as log_file:
            log_file.write(log_message)

    print(log_message)
