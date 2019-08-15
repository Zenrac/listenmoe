from setuptools import setup

setup(
    name='listenmoe',
    packages=['listenmoe'],
    version='v1.0.1',
    description='Unofficial python3 API wrapper to get information about'
    'the listen.moe live stream using aiohttp',
    author='Zenrac',
    author_email='zenrac@outlook.fr',
    url='https://github.com/Zenrac/listenmoe',
    download_url='https://github.com/Zenrac/listenmoe/archive/v1.0.1.tar.gz',
    keywords=['listenmoe'],
    include_package_data=True,
    install_requires=['aiohttp', 'asyncio']
)
