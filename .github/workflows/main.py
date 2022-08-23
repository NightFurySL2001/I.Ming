import os
import sys

def main():
    file_list = []
    for root, dirs, files in os.walk("."):
       for name in files:
            if "I.MingCP-" in name or "I.MingVarCP-" in name:
                file_list.append(os.path.join(root, name))
       #   print(os.path.join(root, name))
       #for name in dirs:
           
               
    print(file_list)
    sys.exit(0)


if __name__ == "__main__":
    main()
