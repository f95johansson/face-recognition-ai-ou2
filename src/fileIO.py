

class InvalidFileError(Exception):pass


class FileIO:
    def __init__(self, training_path, facit_path):
        self.training_path=training_path
        self.facit_path = facit_path
        self.training_images = {}
        self.facit_values = {}
        self.open_training(self.training_path)
        self.open_facit(self.facit_path)


    def open_training(self, path):
        current_image_line = 0
        current_image = []
        current_id = None
        with open(path) as file:
            for line in file:
                if len(line) != 0 and line[0] != '#' and line[0] != '\n':
                    if current_image_line > 0:
                        image_row_strings=line.split(' ')
                        try:
                            image_row = [int(x) for x in image_row_strings]
                        except ValueError:
                            raise InvalidFileError()
                        current_image.append(image_row)
                        current_image_line -= 1
                        if current_image_line == 0:
                            self.training_images[current_id] = current_image
                            current_image = []
                            current_id = None

                    elif line.startswith('Image'):
                        header, current_id = self.get_header(line)
                        if len(header) == 1:
                            current_image_line = 20
                        else:
                            raise InvalidFileError()


    def open_facit(self, path):
        with open(path) as file:
            for line in file:
                if len(line) != 0 and line[0] != '#' and line[0]!='\n':
                    if line.startswith('Image'):
                        header, current_id = self.get_header(line)
                        if len(header) == 2:
                            facit = self.get_facit(header)
                            self.facit_values[current_id] = facit
                        else:
                            raise InvalidFileError()
                    else:
                        raise InvalidFileError()

    def get_header(self, line):
        header=line.split(' ')
        try:
            header.remove('')
        except ValueError:
            pass
        id = header[0].replace('Image', '')
        try:
            return header, int(id)
        except ValueError:
            raise InvalidFileError()

    def get_facit(self, header):
        facit = header[1]
        try:
            return int(facit)
        except ValueError:
            raise InvalidFileError()
