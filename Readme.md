# Resynthesizer python lib

https://github.com/61315/resynthesizer wrapped into python library

Resynthesizer is a very old (2000 year) open-source equivalent to Adobe Photoshop's "Content-Aware Fill" feature

Requirements:

```bash
pip install pillow
```

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

## try

Install Gradio 3 demo requirements and run:
```bash
python -m venv venv
. venv/bin/activate
pip install gradio==3.41.2 pillow
python ./demo.py

```

Windows:
```cmd
python -m venv venv
venv\Script\activate
pip install gradio==3.41.2 pillow
pip install msvc-runtime setuptools
# you also need to have installed https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version
python ./demo.py
```


![](/demo.jpg)

## resynthesizer.so build

1. `git clone https://github.com/61315/resynthesizer`

2. install `gcc`, `make`

3. Modify `Makefile` (added `-fPIC`, use `gcc` instead of `clag`, remove all examples):
<details>

<summary>Makefile</summary>

```Makefile
.POSIX:
CC        = gcc -std=c99
CPPFLAGS  = -MMD -MP -DSYNTH_LIB_ALONE -fPIC
CFLAGS    = -Wall -Wextra -pedantic -O3
LDFLAGS   = -lm
LDLIBS    =
# PREFIX = /usr/local

LIB_DIR := lib
BUILD_DIR := build
SRC_DIR := resynthesizer

# Collect resynthesizer sources and headers, then create object files out of the sources.
SRCS := $(shell find $(SRC_DIR) -name '*.c')
OBJS := $(SRCS:%.c=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRC_DIR) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

STATIC_LIB := $(LIB_DIR)/libresynthesizer.a

ASSET_DIR := assets
EXAMPLE_DIR := examples
EXAMPLES := $(EXAMPLE_DIR)/hello $(EXAMPLE_DIR)/ppm $(EXAMPLE_DIR)/painter

# -g -Wall -Wextra -Werror -std=c99 -pedantic-errors
# TODO: Try both -Werror and -pedantic-errors after all the chores are done.

all: $(STATIC_LIB) test
	@echo "\033[1;92mDone!\033[0m"

# Build resynthesizer as static library.
$(STATIC_LIB): $(OBJS)
	@echo "\033[1;92mBuilding $@\033[0m"
	mkdir -p $(dir $@)
	ar rvs $@ $^

$(BUILD_DIR)/%.o: %.c
	@echo "\033[1;92mBuilding $@\033[0m"
	mkdir -p $(dir $@)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

.PHONY: clean test all

clean:
	$(RM) -r $(BUILD_DIR) $(LIB_DIR) $(EXAMPLES)


-include $(DEPS)

```
</details>

4. Link:
```bash
gcc -shared -o lib.so build/resynthesizer/*.o
```

5. For .dll I've used `x86_64-w64-mingw32-gcc` from `sudo apt-get install gcc-mingw-w64` instead of `gcc`. It shows strange worse result on my virtual machine, I don't know why. They are the same if I build in VM using clang, or if I build it on Linux

6. For Max OS .dylib was built by the author: https://github.com/61315/resynthesizer/issues/6#issuecomment-2221651270
