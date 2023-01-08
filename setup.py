#!/bin/env python3
'''Setup script.'''
from pathlib import Path
from setuptools import setup, find_packages

THIS_DIRECTORY = Path(__file__).parent

REQUIREMENTS = (THIS_DIRECTORY / "requirements.txt").read_text().split('\n')[:-1]
LONG_DESCRIPTION = (THIS_DIRECTORY / "README.md").read_text()

CONTENT = {
    "name": "sulphurvision",
    "version": "2.0.0",
    "author": "Willow Ciesialka",
    "author_email": "wciesialka@gmail.com",
    "url": "https://github.com/wciesialka/sulfurvision",
    "description": "Create an image of Barnacle Boy holding an object.",
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/markdown",
    "license": "GPL-3.0",
    "packages": find_packages(where="src"),
    "entry_points": {
        'console_scripts': [
            'sulfurvision = sulfurvision.__main__:main'
        ]
    },
    "classifiers": [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Operating System :: OS Independent"
    ],
    "keywords": "python image",
    "package_dir": {"": "src"},
    "include_package_data": True,
    "package_data": {'': ['data/base.jpg', 'data/impact.ttf']},
    "install_requires": REQUIREMENTS,
    "zip_safe": False,
    "python_requires": ">=3.11.1"
}

setup(**CONTENT)
