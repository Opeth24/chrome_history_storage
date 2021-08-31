import csv
import os
import sys
import sqlite3

from constants import TEMP_NAME, PATH_TO_ACTIV


class FileProcessor:
    def __init__(self):
        self.path = self.get_path_to_history()
        self.history = self.get_history()

    @staticmethod
    def get_path_to_history() -> str:
        root = f'{os.path.expanduser("~")}'
        chrome_path = r'AppData\Local\Google\Chrome\User Data\Default\History'
        path_to_db = os.path.join(root, chrome_path)

        if not os.path.exists(path_to_db):
            attempts = 3
            while not os.path.exists(path_to_db):
                attempts -= 1

                if attempts == 0:
                    sys.exit('Incorrect path. The program is shutting down')

                print(f'Incorrect path! Yoy have {attempts} attempt.')
                path_to_db = input("Input directory to your Google history file: ")

        return path_to_db

    def get_history(self):
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        # _SQL = 'SELECT name FROM sqlite_master WHERE type = "table"'  # Все таблицы в БД
        # _SQL = 'PRAGMA table_info(urls);'  # Все названия столбцов
        _SQL = """SELECT url, title, visit_count,
               datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') AS time, last_visit_time FROM urls
               ORDER BY time """

        try:
            cursor.execute(_SQL)
        except sqlite3.OperationalError:
            input('Please, close Google Chrome browser and press Enter...')
            cursor.execute(_SQL)

        result = cursor.fetchall()
        cursor.close()
        db.close()

        return result

    def to_csv(self):
        with open(TEMP_NAME, 'w', encoding='utf-8', newline='') as csv_f:
            writer = csv.writer(csv_f, dialect='excel')
            writer.writerow(['URL', 'Description', 'Visit Count', 'Time', 'Google Format Time'])
            for data in self.history:
                writer.writerow(data)

    @staticmethod
    def add_today_history(new_history):
        with open(TEMP_NAME, 'a', encoding='utf-8', newline='') as csv_f:
            writer = csv.writer(csv_f, dialect='excel')
            for data in new_history:
                writer.writerow(data)

    @staticmethod
    def get_last_data_from_csv():
        """Return last data in csv"""
        with open(TEMP_NAME, 'r', encoding='utf-8', newline='') as csv_f:
            reader = csv.reader(csv_f, dialect='excel')
            for row in reader:
                last = row
            return int(last[-1])  # return row[-1] test test test

    def get_last_time_activ_from_history(self):
        return str(self.history[-1][-1])

    @staticmethod
    def is_activ_exist() -> bool:
        return os.path.exists(PATH_TO_ACTIV)

    @staticmethod
    def write_activity(activ_time: str):
        os.makedirs(os.path.dirname(PATH_TO_ACTIV), exist_ok=True)
        with open(PATH_TO_ACTIV, 'w') as f:
            f.write(activ_time)

    @staticmethod
    def read_activity():
        with open(PATH_TO_ACTIV, 'r') as f:
            return int(f.read())

    def get_new_history_from_db(self, csv_last_data: int):
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        # _SQL = 'SELECT name FROM sqlite_master WHERE type = "table"'  # Все таблицы в БД
        # _SQL = 'PRAGMA table_info(urls);'  # Все названия столбцов
        _SQL = """SELECT url, title, visit_count,
               datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') AS time, last_visit_time FROM urls
               WHERE last_visit_time > ?
               ORDER BY time """

        cursor.execute(_SQL, (csv_last_data,))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
