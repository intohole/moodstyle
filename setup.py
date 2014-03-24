from setuptools import setup, find_packages



kw = dict(
    name='moodstyle',
    version='0.0.1',
    description='data mining python code',
    author='intoblack',
    author_email='intoblack86@gmail.com',
    url='https://github.com/intoblack/moodstyle',
    download_url='https://github.com/intoblack/moodstyle',
    platforms='all platform',
    packages=find_packages(),
    include_package_data=True
)

setup(**kw)

