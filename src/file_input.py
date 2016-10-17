from collections import OrderedDict
import preprocessing as pre
from preprocessing import IMAGE_SIZE


class InvalidFileError(Exception):pass

def open_file(path, ordered=False):
    """
    Open a text file and evaluates the data according to the syntax specified in
    https://www8.cs.umu.se/kurser/5DV121/HT15/assignment2/faces.html
    :param path: String path to file
    :return: dict with key: <id> and value: <image>
    """

    data = {} if not ordered else OrderedDict()
    with open(path) as file:
        try:
            iterator = iter(file)

            while True:
                line = next(iterator).rstrip()
                if line.startswith('#'): pass
                elif line == '': pass
                elif line.startswith('Image'):
                    if ' ' in line:
                        id, answer = _read_answer(line)
                        data[id] = answer
                    else:
                        id = _read_id(line)
                        image = _read_image(iterator)
                        image = pre.rotate(image)
                        image = pre.normalize(image)
                        image.append(1) # bias
                        data[id] = image
                else:
                    raise InvalidFileError("With line: "+line)

        except StopIteration:
            pass
        except ValueError:
            raise InvalidFileError()
    return data

def _read_answer(line):
    """
    Ger id and answer from a line with format "Image<ID> <Answer>"
    :param line: line, string with assumed answer and id
    :return: id, answer
    """
    id_string, answer_string = line.split(' ')
    id = int(id_string[len('Image'):])
    answer = int(answer_string)
    return id, answer

def _read_id(line):
    """
    Get id from a line with format "Image<ID>"
    :param line: line, string with assumed id
    :return: id
    """
    return int(line[len('Image'):])

def _read_image(iterator):
    """
    Get the image from the next IMAGE_SIZE lines
    Returns a list of the pixel values
    :param iterator: iterator for file
    :return: image in form of lists of ints
    """
    image = []
    for i in range(IMAGE_SIZE):
        image.extend(list(map(int, next(iterator).split(' '))))
    return image
