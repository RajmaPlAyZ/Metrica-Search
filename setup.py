from setuptools import setup, find_packages

setup(
    name='metrica',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'csv',
        'trie',
    ],  # Add any dependencies here
    entry_points={
        'console_scripts': [
            'metrica-cli = metrica.cli:main',  # Adjust as needed for your CLI entry point
        ],
    },
    author='Aryan Kaul',
    author_email='aryankaul178@gmail.com',
    description='A Trie-based Extended search algorithm library',
    license='MIT',
    keywords='search data structure',
    url='https://github.com/RajmaPlAyZ',
)
