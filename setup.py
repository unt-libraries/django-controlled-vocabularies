from setuptools import setup, find_packages

setup(
    name='django-controlled-vocabularies',
    version='3.0.0',
    packages=find_packages(exclude=['tests*']),
    description='',
    long_description='See the home page for more information.',
    include_package_data=True,
    install_requires=[
        'lxml==4.9.1',
    ],
    url='https://github.com/unt-libraries/django-controlled-vocabularies',
    author='University of North Texas Libraries',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    keywords=['django', 'controlled', 'vocabularies', 'vocabulary'],
    classifiers=[
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
