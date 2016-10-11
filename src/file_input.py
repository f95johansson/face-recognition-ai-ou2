from collections import OrderedDict
import preprocessing as pre
from preprocessing import IMAGE_SIZE


class InvalidFileError(Exception):pass

def open_images(path):
    training_images = OrderedDict()

    current_image_line = 0
    current_image = []
    current_id = None
    with open(path) as file:
        for line in file:
            if len(line) != 0 and line[0] != '#' and line[0] != '\n':
                if current_image_line > 0:
                    image_row_strings=line.split(' ')
                    for pixel in image_row_strings:
                        try:
                            current_image.append(int(pixel))
                        except ValueError:
                            raise InvalidFileError()

                    current_image_line -= 1
                    if current_image_line == 0:
                        current_image = pre.rotate(current_image)
                        current_image = pre.normalize(current_image)
                        current_image.append(1) # bias
                        training_images[current_id] = current_image
                        current_image = []
                        current_id = None

                elif line.startswith('Image'):
                    header, current_id = _get_header(line)
                    if len(header) == 1:
                        current_image_line = IMAGE_SIZE
                    else:
                        raise InvalidFileError()
    return training_images


def open_answers(path):
    facit_values = {}

    with open(path) as file:
        for line in file:
            if len(line) != 0 and line[0] != '#' and line[0]!='\n':
                if line.startswith('Image'):
                    header, current_id = _get_header(line)
                    if len(header) == 2: # form: "Imaged1 1" = facit
                        facit = _get_facit(header)
                        facit_values[current_id] = facit
                    else:
                        raise InvalidFileError()
                else:
                    raise InvalidFileError()
    return facit_values

def _get_header(line):
    header = line.split(' ')
    try:
        header.remove('')
    except ValueError:
        pass
    id = header[0].replace('Image', '')
    try:
        return header, int(id)
    except ValueError:
        raise InvalidFileError()

def _get_facit(header):
    facit = header[1]
    try:
        return int(facit)
    except ValueError:
        raise InvalidFileError()
