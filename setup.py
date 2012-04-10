from setuptools import setup

version = '0.11dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-extensions',
    'django-treebeard',
    'django-nose',
    'djangorestframework',
    'lizard-area',
    'lizard-fewsnorm',
    'lizard-ui >= 3.0',
    'lizard-security',
    'lizard-portal',
    'lizard-task',
    'pkginfo',
    'celery',
    'dbfpy',
    ],

tests_require = [
    ]

setup(name='lizard-esf',
      version=version,
      description="TODO",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='TODO',
      author_email='TODO@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_esf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
