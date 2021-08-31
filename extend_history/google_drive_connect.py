from dataclasses import dataclass
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from constants import DRIVE_NAME, TEMP_NAME
from helpers.exe_path import resource_path


@dataclass()
class DriveManagment:
    auth = GoogleAuth()

    def __post_init__(self):
        self.auth.DEFAULT_SETTINGS['client_config_file'] = resource_path('client_secrets.json')
        self.auth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.auth)
        self.id = self.get_id()

    def get_id(self) -> str:
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        file_id = None

        for f in file_list:
            if f['title'] == DRIVE_NAME:
                file_id = f['id']
                break

        return file_id

    def read_from_google_drive(self) -> bool:
        if not self.id:
            return False

        file2 = self.drive.CreateFile({'id': self.id})
        file2.GetContentFile(TEMP_NAME)

        return True

    def send_to_drive(self):
        file1 = self.drive.CreateFile({'title': DRIVE_NAME})

        file1.SetContentFile(TEMP_NAME)
        file1.Upload()

    def delete_from_drive(self):
        file = self.drive.CreateFile({'id': self.id})
        file.Delete()
