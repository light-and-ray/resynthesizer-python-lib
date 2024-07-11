import ctypes, platform, os
from ctypes import Structure, POINTER, CFUNCTYPE
from ctypes import c_void_p, c_int, c_double, c_char_p, c_uint, c_size_t, c_ubyte

from PIL import Image


class ImageBuffer(Structure):
    _fields_ = [
        ("data", POINTER(c_ubyte)),
        ("width", c_uint),
        ("height", c_uint),
        ("rowBytes", c_size_t)
    ]

class TImageSynthParameters(Structure):
    _fields_ = [
        ("isMakeSeamlesslyTileableHorizontally", c_int),
        ("isMakeSeamlesslyTileableVertically", c_int),
        ("matchContextType", c_int),
        ("mapWeight", c_double),
        ("sensitivityToOutliers", c_double),
        ("patchSize", c_uint),
        ("maxProbeCount", c_uint)
    ]

# Define enum equivalent for TImageFormat
T_RGB = 0
T_RGBA = 1
T_Gray = 2
T_GrayA = 3


script_dir = os.path.dirname(os.path.abspath(__file__))

if platform.system() == 'Windows':
    resynthesizer_lib = ctypes.CDLL(os.path.join(script_dir, "bin", "libresynthesizer.dll"))
elif platform.system() == 'Darwin':
    resynthesizer_lib = ctypes.CDLL(os.path.join(script_dir, "bin", "libresynthesizer_universal.dylib"))
else:
    resynthesizer_lib = ctypes.CDLL(os.path.join(script_dir, "bin", "libresynthesizer.so"))


imageSynth = resynthesizer_lib.imageSynth
imageSynth.argtypes = [
    POINTER(ImageBuffer),
    POINTER(ImageBuffer),
    c_int,
    POINTER(TImageSynthParameters),
    CFUNCTYPE(None, c_int, c_void_p),
    c_void_p,
    POINTER(c_int)
]
imageSynth.restype = c_int


def pil_image_to_image_buffer(image: Image.Image):
    img_bytes = image.tobytes()

    img_data = (c_ubyte * len(img_bytes)).from_buffer_copy(img_bytes)

    input_buffer = ImageBuffer()
    input_buffer.data = ctypes.cast(img_data, POINTER(c_ubyte))
    input_buffer.width = image.width
    input_buffer.height = image.height
    input_buffer.rowBytes = image.width * len(image.mode)

    return input_buffer




def image_buffer_to_pil_image(image_buffer, mode):
    buffer_size = image_buffer.rowBytes * image_buffer.height
    buffer_data = ctypes.cast(image_buffer.data, POINTER(ctypes.c_ubyte * buffer_size))
    buffer_bytes = bytes(buffer_data.contents)
    pil_image = Image.frombytes(mode, (image_buffer.width, image_buffer.height), buffer_bytes)

    return pil_image




def getDefaultParams():
    params = TImageSynthParameters()
    params.isMakeSeamlesslyTileableHorizontally = 1
    params.isMakeSeamlesslyTileableVertically = 1
    params.matchContextType = 1
    params.mapWeight = 0.5
    params.sensitivityToOutliers = 0.117
    params.patchSize = 30
    params.maxProbeCount = 200
    return params




def resynthesize(input_image, mask_image, parameters=None):
    if parameters is None:
        parameters = getDefaultParams()

    input_buffer = pil_image_to_image_buffer(input_image.convert('RGB'))
    mask_buffer = pil_image_to_image_buffer(mask_image.convert('L').resize(input_image.size))

    image_format = T_RGB

    def progress_callback(percent_done, context_info):
        # doesn't work because wasn't compiled with #define DEEP_PROGRESS
        pass

    cancel_flag = ctypes.c_int(0)

    result = imageSynth(
        ctypes.byref(input_buffer),
        ctypes.byref(mask_buffer),
        image_format,
        ctypes.byref(parameters),
        CFUNCTYPE(None, c_int, c_void_p)(progress_callback),
        None,  # contextInfo, opaque to the engine
        ctypes.byref(cancel_flag)
    )

    if result != 0:
        raise RuntimeError(f"imageSynth failed with error code {result}")

    output_image = image_buffer_to_pil_image(input_buffer, "RGB")

    return output_image



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('mask')
    parser.add_argument('output', default="out.png", nargs='?')
    args = parser.parse_args()
    image = Image.open(args.image)
    mask = Image.open(args.mask)
    output = resynthesize(image, mask)
    output.save(args.output)

