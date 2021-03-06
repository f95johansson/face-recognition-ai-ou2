from PIL import Image
from PIL import ImageEnhance
from math import atan2
from math import degrees

IMAGE_SIZE = 20
HIGHEST_PIXEL_VALUE = 31

def normalize(image):
    """
    Returns image with pixel values between 0-1
    :param image: in form of a list with values from 0 to 31
    :return: list with values form 0 to 1
    """
    return [x / HIGHEST_PIXEL_VALUE for x in image]

def highpass_filter(image):
    """
    Perform highpass filter on a non-normalized image
    :param image: in form of a list with values from 0 to 31
    :return: list with values with lower values under 8 set to 0
    """
    for i,value in enumerate(image):
        if value <= 8:
            image[i] = 0
    return image

def contrast(image_list):
    """
    Increases the image contrast on a non-normalized image
    :param image_list: in form of a list with values from 0 to 31
    :return: image with a higher contrast
    """
    image = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE)) # L = 8bit grayscale
    image_list = [x * 255 / HIGHEST_PIXEL_VALUE for x in image_list]
    image.putdata(image_list)
    image = ImageEnhance.Contrast(image)
    image_list = list(image.enhance(4).getdata())
    image_list = [x * HIGHEST_PIXEL_VALUE / 255 for x in image_list]
    return image_list

def rotate(image_list):
    """
    Rotates the image with the eyes always pointing upwards
    :param image_list: in form of a list with values from 0 to 31
    :return: rotated image with eyes pointing upwards
    """
    darkest_pixels = _get_darkest_pixels(image_list)
    x, y = _calculate_mean_position(darkest_pixels)
    # move origin point to middle of image
    x -= IMAGE_SIZE // 2
    y -= IMAGE_SIZE // 2

    rotation = degrees(atan2(y, x)) + 90

    image = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE)) # L = 8bit grayscale
    image.putdata(image_list)

    return list(image.rotate(rotation).getdata())

def _get_darkest_pixels(image_list, dark_count=30):
    """
    Returns a list of the darkest pixel values in image
    List consits of tuples with a tuple of (pixel, position)
    :param image_list: in form of a list with values from 0 to 31
    :return: list of the <dark_count> darkest pixels
    """

    darkest_pixels = [] # consits of tutple of (pixel, position)
    lightest_dark_pixel = None
    for position, pixel in enumerate(image_list):
        if len(darkest_pixels) < dark_count:
            darkest_pixels.append((pixel, position))
            if lightest_dark_pixel == None:
                lightest_dark_pixel = pixel
            elif pixel < lightest_dark_pixel: # brighter
                lightest_dark_pixel = pixel

        elif pixel > lightest_dark_pixel: # darker
            for i, value in enumerate(darkest_pixels):
                if value[0] == lightest_dark_pixel:
                    darkest_pixels.pop(i)

            darkest_pixels.append((pixel, position))
            lightest_dark_pixel = HIGHEST_PIXEL_VALUE + 1 # max dark
            for dark_pixel, _ in darkest_pixels:
                if dark_pixel < lightest_dark_pixel: # brighter
                    lightest_dark_pixel = dark_pixel            

    return darkest_pixels

def _calculate_mean_position(pixels):
    """
    Calculates the mean position of all values in pixels
    :param pixels: list of pixels if form of tuples (pixel, position)
    """
    mean_y = 0
    mean_x = 0
    for _, position in pixels:
        y = position // IMAGE_SIZE
        x = position % IMAGE_SIZE
        mean_y += y
        mean_x += x
    mean_y /= len(pixels)
    mean_x /= len(pixels)
    return mean_x, mean_y
