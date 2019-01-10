from distutils.core import setup

setup(
    name='pyimago',
    version='1.0',
    packages=['pyimago'],
    url='https://github.com/Pandaaaa906/pyimago',
    license='',
    author='Andrew Yip',
    author_email='ye.pandaaaa906@gmail.com',
    description='A python binding of Imago',
    package_dir={'pyimago': 'pyimago'},
    package_data={'pyimago': ['imago_x64/*', ]},
)
