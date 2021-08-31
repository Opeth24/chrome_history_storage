import os
import sys


def resource_path(relative_path: str) -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        #  relative_path;client_secrets
        bundle_dir = os.path.join(sys._MEIPASS, 'client_secrets', relative_path)
        print(f'{bundle_dir=}')
    else:
        bundle_dir = os.path.join(os.path.abspath("."), relative_path)
    return bundle_dir
