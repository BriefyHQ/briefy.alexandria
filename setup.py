"""Digital Assets Library: store and search digital assets data and metadata.."""
from setuptools import find_packages
from setuptools import setup

import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'HISTORY.rst')) as f:
    CHANGES = f.read()

requires = [
    'briefy.common',
    'briefy.ws',
    'prettyconf',
    'pyramid==1.9.1',
    'pyramid_tm',
    'pyramid_zcml',
    'setuptools',
]

test_requirements = [
    'flake8',
    'pytest'
]

setup(
    name='briefy.alexandria',
    version='0.1.0',
    description='Digital Assets Library: store and search digital assets data and metadata.',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    author='Briefy Tech Team',
    author_email='developers@briefy.co',
    url='https://github.com/BriefyHQ/briefy.alexandria',
    keywords='briefy,assets,library,api',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['briefy', ],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    tests_require=test_requirements,
    install_requires=requires,
    entry_points="""
    [paste.app_factory]
     main = briefy.alexandria:main
    """,
)
