from setuptools import setup, find_packages

# python setup.py sdist bdist_wheel
# twine upload resynthesizer-1.X-py3-none-any.whl resynthesizer-1.X.tar.gz

setup(
    name='resynthesizer',
    version='1.2',
    packages=find_packages(),  # Automatically find packages under the current directory

    # Package metadata
    description='A very old open-source "Content-Aware Fill" method',
    long_description="""
Python library which wraps 61315's pure C implementation of resynthesizer (open-source Content-Aware Fill equivalent)

## Usage:
```python
from resynthesizer import resynthesize
from PIL import Image

source = Image.open('source.jpg')
# mask must have black background, white foreground
mask = Image.open('mask.png')
result = resynthesize(source, mask)
result.save('result.jpg')

```


You can adjust resynthesizer's params if you want:
```python
from resynthesizer import TImageSynthParameters

# defaults
params = TImageSynthParameters()
params.isMakeSeamlesslyTileableHorizontally = 1
params.isMakeSeamlesslyTileableVertically = 1
params.matchContextType = 1
params.mapWeight = 0.5
params.sensitivityToOutliers = 0.117
params.patchSize = 30
params.maxProbeCount = 200

...

result = resynthesize(source, mask, parameters=params)

```

Package repo: https://github.com/light-and-ray/resynthesizer-python-lib
Pure C Implementation repo: https://github.com/61315/resynthesizer
Original repo: https://github.com/bootchk/resynthesizer

    """,
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
        '': ['resynthesizer/bin/*'],
    },

    # Include non-Python files
    include_package_data=True,

    license='GPL-3.0',


    # # Classifiers for PyPI
    # classifiers=[
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.9',
    #     # Add more classifiers as appropriate
    # ],
)
