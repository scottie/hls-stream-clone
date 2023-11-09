# setup.py
from setuptools import setup

setup(
    name='hls_downloader',
    version='0.1',
    py_modules=['hls_downloader'],
    install_requires=[
        'm3u8',
        # add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'hls-downloader=hls_downloader:main',
        ],
    },
)
