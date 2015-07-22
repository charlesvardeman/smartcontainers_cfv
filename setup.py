try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Docker Smart Containers',
    'author': 'Charles F Vardeman II',
    'url': 'https://github.com/charlesvardeman/smartcontainers',
    'download_url': 'https://github.com/charlesvardeman/smartcontainers',
    'author_email': 'My email.',
    'version': '0.02',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'smartcontainers'
}

setup(**config)
