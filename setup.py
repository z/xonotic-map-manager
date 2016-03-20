from setuptools import setup
from setuptools import find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='xmm',
    version='0.3.0',
    description='Xonotic Map Manager',
    long_description=readme,
    author='Tyler Mulligan',
    author_email='z@xnz.me',
    url='https://github.com/z/xonotic-map-manager',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['pkg/xmm.bash', 'pkg/xmm.zsh'],
    entry_points={
       'console_scripts': [
          'xmm = xmmc.xmm:main'
       ]
    },
    install_requires=required
)
