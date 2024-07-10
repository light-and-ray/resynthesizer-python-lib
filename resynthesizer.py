import ctypes, os
from ctypes import Structure, POINTER, CFUNCTYPE
from ctypes import c_void_p, c_int, c_double, c_char_p, c_uint, c_size_t, c_ubyte

from PIL import Image

# Define the structs corresponding to the C headers
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

# Load the shared library
if os.name == 'nt':
    resynthesizer_lib = ctypes.CDLL("./bin/resynthesizer.dll")
else:
    resynthesizer_lib = ctypes.CDLL("./bin/resynthesizer.so")

# Define the function prototype
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
    # Get the raw byte array of the image
    img_bytes = image.tobytes()

    # Create a ctypes array from the raw byte data
    img_data = (c_ubyte * len(img_bytes)).from_buffer_copy(img_bytes)

    # Create an instance of ImageBuffer
    input_buffer = ImageBuffer()
    input_buffer.data = ctypes.cast(img_data, POINTER(c_ubyte))
    input_buffer.width = image.width
    input_buffer.height = image.height
    input_buffer.rowBytes = image.width * len(image.mode)

    return input_buffer





def image_buffer_to_pil_image(image_buffer, mode):
    # Calculate the size of the buffer
    buffer_size = image_buffer.rowBytes * image_buffer.height

    # Create a bytes object from the buffer data
    buffer_data = ctypes.cast(image_buffer.data, POINTER(ctypes.c_ubyte * buffer_size))

    # Convert buffer_data to bytes object
    buffer_bytes = bytes(buffer_data.contents)

    # Create PIL Image from bytes data
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




# Python function to wrap imageSynth
def resynthesize(input_image, mask_image, parameters=None):
    if parameters is None:
        parameters = getDefaultParams()
    # Convert PIL images to ImageBuffer
    input_buffer = pil_image_to_image_buffer(input_image.convert('RGB'))
    mask_buffer = pil_image_to_image_buffer(mask_image.convert('L'))

    image_format = T_RGB

    # Set up progress callback (not implemented here)
    def progress_callback(percent_done, context_info):
        pass

    # Set up cancel flag
    cancel_flag = ctypes.c_int(0)

    # Call the imageSynth function
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

    # Convert the output buffer to PIL Image
    output_image = image_buffer_to_pil_image(input_buffer, "RGB")

    return output_image



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('mask')
    parser.add_argument('output', default="out.png")
    args = parser.parse_args()
    image = Image.open(args.image)
    mask = Image.open(args.mask).resize(image.size)
    output = resynthesize(image, mask)
    output.save(args.output)
