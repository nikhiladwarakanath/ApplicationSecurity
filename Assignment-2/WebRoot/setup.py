from setuptools import find_packages, setup
setup(
    name='temp',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),  # Include all the python modules except `tests`.
    description='My custom package tested with tox',
    long_description='A long description of my custom package tested with tox',
    classifiers=[
        'Programming Language :: Python',
    ],
    
    extras_require={':python_version<"3.7"': ['importlib-resources']}, 

)
