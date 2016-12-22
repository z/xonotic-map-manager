from setuptools import setup
from setuptools import find_packages
from xmm import __author__, __email__, __url__, __license__, __version__, __summary__, __keywords__


with open('requirements.in') as f:
    install_requires = f.read().splitlines()

try:
    import pypandoc
    readme_contents = pypandoc.convert('README.md', 'rst')
    changelog_contents = pypandoc.convert('CHANGELOG.md', 'rst')
except(IOError, ImportError):
    with open('README.md') as f:
        readme_contents = f.read()
    with open('CHANGELOG.md') as f:
        changelog_contents = f.read()

long_description = '{}\n{}'.format(readme_contents, changelog_contents)

setup(
    name='xmm',
    version=__version__,
    description=__summary__,
    long_description=long_description,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE', 'README.md', 'CHANGELOG.md', 'docs/*', 'config/*', 'bin/*', 'pkg/*', 'resources/*']},
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
    keywords=__keywords__,
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: MIT License',

        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Topic :: Games/Entertainment',
        'Topic :: System :: Archiving :: Packaging',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
