from perceptron import Perceptron
from moods import Moods
from random import shuffle

LEARNING_RATE = 0.01

class NeuralNetwork:

    def __init__(self, training_set, facit_set):
        self._training_set = training_set
        self._facit_set = facit_set
        self._input_size = len(next(iter(training_set.values())))
        self._perceptrons = {
            Moods.happy:       Perceptron(LEARNING_RATE, self._input_size),
            Moods.sad:         Perceptron(LEARNING_RATE, self._input_size),
            Moods.mischievous: Perceptron(LEARNING_RATE, self._input_size),
            Moods.mad:         Perceptron(LEARNING_RATE, self._input_size),
        }

    def learn(self):
        total_error =0
        counter = self._input_size*len(self._training_set)*len(self._perceptrons)
        total_error+=self.learning_step()
        n = 0

        threshold = 20

        """
        19 -> 71%
        """

        while total_error/counter > threshold:
            n += 1
            counter+=self._input_size*len(self._training_set)*len(self._perceptrons)
            total_error+=self.learning_step()
            #print(n, total_error/counter)

    def check(self, test_set):
        #with open('result.txt', 'w') as file:
        for id in test_set.keys():
            image = test_set[id]
            answers = {}
            for mood, perceptron in self._perceptrons.items():
                answers[perceptron.check(image)] = mood
            final_answer = answers[max(answers.keys())]
            print('Image{} {}'.format(id, final_answer.value))
            #file.write('Image{} {}\n'.format(id, final_answer.value))

    def learning_step(self):
         ids = list(self._training_set.keys())
         shuffle(ids)
         total_error=0
         for id in ids:
             image = self._training_set[id]
             for mood, perceptron in self._perceptrons.items():
                 answer = int(mood.value == self._facit_set[id])
                 total_error += perceptron.train(image, answer)**2
         return total_error
