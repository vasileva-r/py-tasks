from setuptools import setup, find_packages

setup(
    name='movie_dataset',
    version='1.0.0',
    author='Roza',
    author_email='vuchevar@yahoo.com',
    description='Movie dataset task',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'logging'
    ],
)