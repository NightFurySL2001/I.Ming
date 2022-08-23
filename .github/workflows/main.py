import os
import sys

def main():
    path = os.environ["GITHUB_ENV"]
    print(path)
    
    for root, dirs, files in os.walk(path):
       for name in files:
          print(os.path.join(root, name))
       for name in dirs:
          print(os.path.join(root, name))
    sys.exit(0)


if __name__ == "__main__":
    main()
