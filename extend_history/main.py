import os

from file_processor import FileProcessor
from google_drive_connect import DriveManagment
from constants import TEMP_NAME

if __name__ == '__main__':
    file_process = FileProcessor()

    today_activ = file_process.get_last_time_activ_from_history()

    drive_control = DriveManagment()

    if drive_control.read_from_google_drive():

        if file_process.is_activ_exist():
            print('activ_exist')
            prev_activity = file_process.read_activity()
        else:
            print("Can't find local file with time activity. Try to read data from Google Drive.")
            print("Synchronization...")
            prev_activity = file_process.get_last_data_from_csv()

        new_history = file_process.get_new_history_from_db(prev_activity)
        print(f'You have {len(new_history)} new activity!')

        if new_history:
            file_process.add_today_history(new_history)
            drive_control.delete_from_drive()
            drive_control.send_to_drive()
    else:
        file_process.to_csv()
        drive_control.send_to_drive()

    file_process.write_activity(today_activ)

    if os.path.exists(TEMP_NAME):
        os.remove(TEMP_NAME)
