from random import random
from math import exp

class Perceptron:
    def __init__(self, learning_rate, number_of_input):
        self._learning_rate = learning_rate
        self.weights = [random() for i in range(number_of_input)]

    def train(self, inputs, answer):
        if len(inputs) != len(self.weights):
            raise ValueError('Wrong number of inputs')

        a = self.check(inputs)
        total_error =0

        for i in range(len(inputs)):
            error = answer - a
            total_error+=error
            delta_weight = self._learning_rate * error * inputs[i]
            self.weights[i] = self.weights[i] + delta_weight
        return total_error



    def check(self, inputs):
        summation = 0
        for i in range(len(inputs)):
            summation += self.weights[i]*inputs[i]
        return activation_function(summation)



def activation_function(x):
    return 1/(1+exp(-x))
