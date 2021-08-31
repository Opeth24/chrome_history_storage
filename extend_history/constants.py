import os

DRIVE_NAME = 'temp_chrome_history_db.csv'
TEMP_NAME = 'temp_db.csv'
PATH_TO_ACTIV = os.path.join(os.path.expanduser("~"), r'AppData\Local\ChromeHistorySaver\last_time_activ.txt')

__all__ = [
    'DRIVE_NAME',
    'TEMP_NAME',
    'PATH_TO_ACTIV'
]
