import sys
import file_input
from neural_network import NeuralNetwork

def main():
    """
    Takes 3 arguments from command line in forms of paths to text files.
    Path to: trainging images, training answers and test images
    """
    try:
        training_path = sys.argv[1]
        answers_path = sys.argv[2]
        test_path = sys.argv[3]

    except IndexError:
        print('Invalid arguments')

    else:
        training_set = file_input.open_file(training_path)
        answer_set = file_input.open_file(answers_path)
        test_set = file_input.open_file(test_path, ordered=True)

        network = NeuralNetwork(training_set, answer_set)
        network.learn()
        network.check(test_set)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
