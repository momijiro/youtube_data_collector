from setuptools import find_packages, setup
# google-api-python-client
# pandas
# python-dateutil
# tqdm


setup(
    name='youtube-data-collector',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'pandas',
        'python-dateutil',
        'tqdm',
    ],
    author='momijiro',
    description='A simple library to collect data using YouTube API',
    url='https://github.com/momijiro/youtube-data-collector',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
