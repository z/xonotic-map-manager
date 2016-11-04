from setuptools import setup
from setuptools import find_packages
from xmm import __author__, __email__, __url__, __version__


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.in') as f:
    required = f.read().splitlines()

setup(
    name='xmm',
    version=__version__,
    description='Xonotic Map Manager',
    long_description=readme,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE', 'README.md', 'docs/*', 'config/*', 'bin/*']},
    include_package_data=True,
    install_requires=required,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    scripts=['pkg/xmm.bash', 'pkg/xmm.zsh'],
    entry_points={
       'console_scripts': [
          'xmm = xmm.cli:main'
       ]
    },
)
