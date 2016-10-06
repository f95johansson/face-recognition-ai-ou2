import sys
import fileIO
from neural_network import NeuralNetwork

def main():
    try:
        training_path = sys.argv[1]
        facit_path = sys.argv[2]
        test_path = sys.argv[3]


        training_set = fileIO.open_images(training_path)
        facit_set = fileIO.open_answers(facit_path)
        test_set = fileIO.open_images(test_path)

        network = NeuralNetwork(training_set, facit_set)
        network.learn()
        network.check(test_set)

    except ValueError:
        print('Invalid arguments')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
