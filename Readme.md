# Resynthesizer python lib

https://github.com/61315/resynthesizer wrapped into python library

Resynthesizer is a very old (2000 year) open-source equivalent to Adobe Photoshop's "Content-Aware Fill" feature

Requirements:

```bash
pip install pillow
```

Usage:
```python
from resynthesizer import resynthesize
from PIL import Image

source = Image.open('source.jpg')
# mask must have black background, white foreground
mask = Image.open('mask.png')
result = resynthesize(source, mask)
result.save('result.jpg')

```

## try

Install and run Gradio 3 demo requirements:
```bash
python -m venv venv
. venv/bin/activate
pip install gradio==3.41.2 pillow
python ./demo.py

```

![](/demo.jpg)

Todo:
- build for Windows
- pack into wheel and add into pip repository
