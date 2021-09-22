import os

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="./", help="path to the folder whose subfolders will be scanned")
    parser.add_argument("-o", "--output", help="if given, the data will be printed", action="store_true")
    return parser.parse_args()
    

def get_sizes(data, current_path):
    if not data.get(current_path):
        return 0
    size = 0
    for folder in data[current_path]["folders"]:
        tmp = get_sizes(data, os.path.join(current_path, folder))
        data[current_path]["folders"][folder] = tmp
        size += tmp
    for file in data[current_path]["files"]:
        try:
            tmp = os.path.getsize(os.path.join(current_path, file))
        except FileNotFoundError:
            tmp = 0
        except OSError:
            tmp = 0
        data[current_path]["files"][file] = tmp
        size += tmp
    return size

def explore(path):
    """
    returns tuple
    index 0 is the total size
    index 1 is a dictionary for every file and folder with size included
    """
    data = {x[0]: {"folders": {y: 0 for y in x[1]}, "files": {z: 0 for z in x[2]}} for x in os.walk(path)}
    total_size = get_sizes(data, path)
    return (total_size, data)

if __name__ == "__main__":
    args = get_args()
    result = explore(args.path)
    if args.output:
        print(result[1])
    print("Total size:", result[0])

