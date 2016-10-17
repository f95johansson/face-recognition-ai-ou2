from perceptron import Perceptron
from moods import Moods
from random import shuffle

LEARNING_RATE = 0.01

class NeuralNetwork:
    """
        Keeps track of the perceptron. Controls when the perceptron are
        training and when to test.
        :param training_set: the set of images to train on
        :param facit_set: the set of facit to the training_set
    """
    def __init__(self, training_set, facit_set):
        self._training_set = training_set
        self._facit_set = facit_set
        self._input_size = len(next(iter(training_set.values()))) # first value
        self._perceptrons = {
            Moods.happy:       Perceptron(LEARNING_RATE, self._input_size),
            Moods.sad:         Perceptron(LEARNING_RATE, self._input_size),
            Moods.mischievous: Perceptron(LEARNING_RATE, self._input_size),
            Moods.mad:         Perceptron(LEARNING_RATE, self._input_size),
        }

    def learn(self):
        """
            This method is the part where the program learns the perceptron to
            recognize moods in pictures. It keeps track of the total error in
            order to quit the learningface when the error is small enough.
        """
        total_error = 0
        threshold = 0.05

        counter = len(self._training_set)*len(self._perceptrons)
        total_error+=self.learning_step()

        while total_error/counter > threshold:
            counter += len(self._training_set)*len(self._perceptrons)
            total_error +=self.learning_step()

    def check(self, test_set):
        """
            This is the method used when the image answer is not available for
            the program to read.
            :param test_set: Set of data to test the NeuralNetwork with  
        """
        for id in test_set.keys():
            image = test_set[id]
            answers = {}
            for mood, perceptron in self._perceptrons.items():
                answers[perceptron.check(image)] = mood
            final_answer = answers[max(answers.keys())]
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
         total_error=0
         for id in ids:
             image = self._training_set[id]
             for mood, perceptron in self._perceptrons.items():
                 answer = int(mood.value == self._facit_set[id])
                 total_error += perceptron.train(image, answer)**2
         return total_error
