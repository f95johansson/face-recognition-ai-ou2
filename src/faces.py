
import sys

def main():
    try:
        training_path = sys.argv[1]
        training_facit = sys.argv[2]
        test_path = sys.argv[3]
    except ValueError:
        print('Invalid arguments')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')