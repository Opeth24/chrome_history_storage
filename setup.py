from setuptools import find_packages
from setuptools import setup


setup(
    name="extend_chrome_history",
    version='1.0.0',
    packages=find_packages(exclude=['*_notebooks', '*playground*']),
    author="Veselov Anton",  # repository maintainer
    author_email="veselov95.anton@gmail.com",  # repository maintainer
    install_requires=[
        'PyDrive==1.3.1',
        'google-api-python-client==1.8.0'
    ],
)
