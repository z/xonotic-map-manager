from setuptools import setup
from setuptools import find_packages
from xmm import __author__, __email__, __url__, __version__


with open('README.md') as f:
    readme_contents = f.read()

with open('LICENSE') as f:
    license_contents = f.read()

with open('requirements.in') as f:
    install_requires = f.read().splitlines()

setup(
    name='xmm',
    version=__version__,
    description='Xonotic Map Manager',
    long_description=readme_contents,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=license_contents,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE', 'README.md', 'docs/*', 'config/*', 'bin/*', 'pkg/*', 'resources/*']},
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    scripts=['pkg/xmm.bash', 'pkg/xmm.zsh'],
    entry_points={
       'console_scripts': [
          'xmm = xmm.cli:main'
       ]
    },
)
