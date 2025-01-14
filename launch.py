import sys
from legacy.legacy import *


if __name__ == "__main__":
    # This is how it will select which generator to run
    file = str(sys.argv[1])
    # This will be the seed for the generator
    seed = int(sys.argv[2])