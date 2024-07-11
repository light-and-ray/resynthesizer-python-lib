from setuptools import setup, find_packages

# python setup.py sdist bdist_wheel

setup(
    name='resynthesizer',
    version='1.0',
    packages=find_packages(),  # Automatically find packages under the current directory

    # Package metadata
    description='A very old open-source "Content-Aware Fill" method',
    long_description="Python library which wraps 61315's pure C implementation of resynthesizer (open-source Content-Aware Fill equivalent)",
    long_description_content_type='text/markdown',
    url='https://github.com/light-and-ray/resynthesizer-python-lib',

    # Dependencies
    install_requires=[
        'pillow',
    ],

    # # Entry points
    # entry_points={
    #     'console_scripts': [
    #         'your_command=your_package_name.module_name:main_function',
    #     ],
    # },


    package_data={
        '': ['bin/*'],  # Include binary files under bin directory
    },

    # Include non-Python files
    include_package_data=True,

    # License
    license='GPL-3.0',  # Specify your license

    # # Classifiers for PyPI
    # classifiers=[
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.9',
    #     # Add more classifiers as appropriate
    # ],
)