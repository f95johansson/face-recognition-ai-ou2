import sys
import file_input
from neural_network import NeuralNetwork

def main():
    try:
        training_path = sys.argv[1]
        facit_path = sys.argv[2]
        test_path = sys.argv[3]

    except ValueError:
        print('Invalid arguments')

    else:
        training_set = file_input.open_file(training_path)
        facit_set = file_input.open_file(facit_path)
        test_set = file_input.open_file(test_path, ordered=True)

        network = NeuralNetwork(training_set, facit_set)
        network.learn()
        network.check(test_set)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
