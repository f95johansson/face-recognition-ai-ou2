from perceptron import Perceptron
from moods import Moods
from random import shuffle

LEARNING_RATE = 0.01

class NeuralNetwork:

    def __init__(self, training_set, facit_set):
        self._training_set = training_set
        self._facit_set = facit_set
        input_size = len(next(iter(training_set.values())))
        self._perceptrons = {
            Moods.happy:       Perceptron(LEARNING_RATE, input_size),
            Moods.sad:         Perceptron(LEARNING_RATE, input_size),
            Moods.mischievous: Perceptron(LEARNING_RATE, input_size),
            Moods.mad:         Perceptron(LEARNING_RATE, input_size),
        }

    def learn(self):
        for i in range(20):
            ids = list(self._training_set.keys())
            shuffle(ids)
            for id in ids:
                image = self._training_set[id]
                for mood, perceptron in self._perceptrons.items():
                    answer = int(mood.value == self._facit_set[id])
                    perceptron.train(image, answer)

    def check(self, test_set):
        with open('result.txt', 'w') as file:
            for id in test_set.keys():
                image = test_set[id]
                answers = {}
                for mood, perceptron in self._perceptrons.items():
                    answers[perceptron.check(image)] = mood
                final_answer = answers[max(answers.keys())]
                #print('Image{} {}'.format(id, final_answer))
                file.write('Image{} {}\n'.format(id, final_answer.value))