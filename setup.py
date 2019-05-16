from setuptools import setup

setup(
    name='unitpy',
    version='0.0.1',
    packages=['unitpy', 'unitpy.units', 'unitpy.units.combined_units'],
    url='',
    license='MIT',
    author='Joseph Enders',
    author_email='',
    description='Allows for calculation for values containing units.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['six'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
