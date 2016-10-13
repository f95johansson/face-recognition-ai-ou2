from perceptron import Perceptron
from moods import Moods
from random import shuffle

LEARNING_RATE = 0.01

class NeuralNetwork:
    """
        Keeps track of the perceptron. Controls when the perceptron are
        training and when to test.

        This NeuralNetwork is a modified version which splits each image
        into two, with the eyes in one half and mouth in the other. 
        Two perceptrons is assigned to each half of the images,
        i.e two eys perceptrons and two mouth perceptrons. 
        When checking against test set, answer is given by combining
        answers from the two sets of perceptrons
    """

    def __init__(self, training_set, facit_set):
        self._training_set = training_set
        self._facit_set = facit_set
        self._input_size = len(next(iter(training_set.values()))) // 2 # len(first value) / 2
        self._perceptrons_mouth = {
            Moods.happy:       Perceptron(LEARNING_RATE, self._input_size),
            Moods.sad:         Perceptron(LEARNING_RATE, self._input_size)
        }
        self._perceptrons_eyes = {
            Moods.sad:       Perceptron(LEARNING_RATE, self._input_size),
            Moods.mad:         Perceptron(LEARNING_RATE, self._input_size)
        }

    def learn(self):
        """
            This method is the part where the program learns the perceptron to
            recognize moods in pictures. It keeps track of the total error in
            order to quit the learningface when the error is small enough.
        """
        total_error = 0
        threshold = 0.07

        counter = len(self._training_set)*len(self._perceptrons_mouth)
        total_error+=self.learning_step()

        while total_error/counter > threshold:
            counter += len(self._training_set)*len(self._perceptrons_mouth)
            total_error +=self.learning_step()

    def check(self, test_set):
        """
            This is the method used when the image answer is not available for
            the program to read.  
        """
        for id in test_set.keys():
            image_eyes, image_mouth = _split_image(test_set[id])

            answers_eyes = {}
            answers_mouth = {}
            for mood, perceptron in self._perceptrons_mouth.items():
                answers_mouth[perceptron.check(image_mouth)] = mood

            for mood, perceptron in self._perceptrons_eyes.items():
                answers_eyes[perceptron.check(image_eyes)] = mood
            
            final_answer_mouth = answers_mouth[max(answers_mouth.keys())]
            final_answer_eyes = answers_eyes[max(answers_eyes.keys())]

            if final_answer_mouth == Moods.happy and final_answer_eyes == Moods.sad:
                final_answer = Moods.happy
            elif final_answer_mouth == Moods.happy and final_answer_eyes == Moods.mad:
                final_answer = Moods.mischievous
            elif final_answer_mouth == Moods.sad and final_answer_eyes == Moods.sad:
                final_answer = Moods.sad
            else:
                final_answer = Moods.mad

            print('Image{} {}'.format(id, final_answer.value))

    def learning_step(self):
        """
            This is where the actual trining is happening. The method sends an
            image with it's answer to the perceptron. One training session is
            one lap with a specific set of picture. It also returns the total
            error of that session.
        """
        ids = list(self._training_set.keys())
        shuffle(ids)
        total_error = 0
        for id in ids:
            image_eyes, image_mouth = _split_image(self._training_set[id])

            for mood, perceptron in self._perceptrons_mouth.items():
                answer = int(mood.value % 2 == self._facit_set[id] % 2) # if both even
                total_error += perceptron.train(image_mouth, answer)**2

            for mood, perceptron in self._perceptrons_eyes.items():
                # if 1 or 2; 3 or 4
                answer = int(mood.value + (mood.value % 2) == 
                    self._facit_set[id] + (self._facit_set[id] % 2))
                total_error += perceptron.train(image_eyes, answer)**2

        return total_error


def _split_image(image):
    return image[:len(image)//2], image[len(image)//2:]
