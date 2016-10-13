from collections import OrderedDict
import preprocessing as pre
from preprocessing import IMAGE_SIZE


class InvalidFileError(Exception):pass

def open_file(path, ordered=False):
    data = {} if not ordered else OrderedDict()
    with open(path) as file:
        try:
            iterator = iter(file)

            while True:
                line = iterator.__next__().rstrip()
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
                        data[id] = image
                else:
                    raise InvalidFileError("With line: "+line)

        except StopIteration:
            pass
        except ValueError:
            raise InvalidFileError()
    return data

def _read_answer(line):
    id_string, answer_string = line.split(' ')
    id = int(id_string[len('Image'):])
    answer = int(answer_string)
    return id, answer

def _read_id(line):
    return int(line[len('Image'):])

def _read_image(iterator):
    image = []
    for i in range(IMAGE_SIZE):
        image.extend(list(map(int, iterator.__next__().split(' '))))
    return image
