
import os
def extract_number(item):
    return int(item.split()[0][:-1])

def get_directories_dict(root_dir):
    directories_dict = {}
    for root, dirs, _ in os.walk(root_dir):
        if os.path.basename(root).startswith('class_'):
            directories_dict[os.path.basename(root)] = sorted(dirs, key=extract_number)
    return directories_dict

print(get_directories_dict('data/class'))