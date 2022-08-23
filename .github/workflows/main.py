import os
import sys

def main():
    for root, dirs, files in os.walk("../.."):
       for name in files:
          print(os.path.join(root, name))
       for name in dirs:
          print(os.path.join(root, name))
    sys.exit(0)


if __name__ == "__main__":
    main()
