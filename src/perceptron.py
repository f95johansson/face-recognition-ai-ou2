from random import random
from math import exp

class Perceptron:
    def __init__(self, learning_rate, number_of_input):
        self._learning_rate = learning_rate
        self.weights = [(random()-.5)/100 for i in range(number_of_input)]

    def train(self, inputs, answer):
        """
        Adjust the weights based on the inputs and the corresponding answers.
        Returns error
        """
        a = self.check(inputs)
        error = answer - a

        for i in range(len(inputs)):    
            delta_weight = self._learning_rate * error * inputs[i]
            self.weights[i] += delta_weight
        return error


    def check(self, inputs):
        """
        Returns activation value given from the summation of inputs and weights
        """
        if len(inputs) != len(self.weights):
            raise ValueError('Wrong number of inputs')

        summation = 0
        for i in range(len(self.weights)):
            summation += self.weights[i]*inputs[i]
        return activation_function(summation)



def activation_function(x):
    """Sigmoid logistic activation function"""
    return 1/(1+exp(-x))
