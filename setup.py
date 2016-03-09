from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

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
    scripts=['bin/xmm']
)