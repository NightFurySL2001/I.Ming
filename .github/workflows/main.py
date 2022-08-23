import os
import sys

RENAME_LIST_EN = {
    "I.MingCP": ["PMing.I", "I.MingU"],
    "I.MingVarCP": ["PMingVar.I", "I.MingVarU"],
}


def main():
    file_list = []
    # walk through all directory of current repo
    for root, dirs, files in os.walk("."):
        # list all files in current walking dir
        for name in files:
            # if name
            if "I.MingCP" in name or "I.MingVarCP" in name:
                # loop through changing name
                for orig, new in RENAME_LIST_EN:
                    # if file does not exist
                    if not os.path.exists(os.path.join(root, name.replace(orig, new[0]))):
                        # add file into list of files to be convert
                        file_list.append(os.path.join(root, name))
               
    print(file_list)
    sys.exit(0)


if __name__ == "__main__":
    main()
