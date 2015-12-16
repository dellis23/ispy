from distutils.core import setup


setup(
    name='ispy',
    packages=['ispy'],
    version='0.1.1',
    license='GPLv2',
    description='A python script for monitoring the output of terminals and processes.',
    author='Daniel Ellis',
    author_email='ellisd23@gmail.com',
    url='https://github.com/dellis23/ispy',
    scripts=[
        'bin/ispy',
    ],
    install_requires=[
        'python-ptrace',
    ],
)
