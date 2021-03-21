from core import Bumblebee
import features
import sys

if __name__ == "__main__":
    print(features.__all__)

    bumblebee = Bumblebee(features.__all__)
    bumblebee.run()
