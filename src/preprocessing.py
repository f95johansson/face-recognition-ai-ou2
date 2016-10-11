from PIL import Image
from PIL import ImageEnhance
from math import atan2
from math import degrees

IMAGE_SIZE = 20
HIGHEST_PIXEL_VALUE = 31

def highpass_filter(image):
    for i,value in enumerate(image):
        if value <= 5/31:
            image[i] = 0

def normalize(image):
    return [x / HIGHEST_PIXEL_VALUE for x in image]

def contrast(image_list):
    image = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE)) # L = 8bit grayscale
    image_list = [x * 255 / HIGHEST_PIXEL_VALUE for x in image_list]
    image.putdata(image_list)
    image = ImageEnhance.Contrast(image)
    image_list = list(image.enhance(.25).getdata())
    image_list = [x * HIGHEST_PIXEL_VALUE / 255 for x in image_list]
    return image_list

def rotate(image_list):
    darkest_pixels = _get_darkest_pixels(image_list)
    x, y = _calculate_mean_position(darkest_pixels)
    # move origin point to middle of image
    x -= IMAGE_SIZE // 2 
    y -= IMAGE_SIZE // 2

    rotation = degrees(atan2(y, x))

    image = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE)) # L = 8bit grayscale
    image.putdata(image_list)

    return list(image.rotate(rotation).getdata())

def _get_darkest_pixels(image_list, dark_count=30):
    darkest_pixels = [] # pixel -> position
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
    # pixels: (pixel, position)
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
