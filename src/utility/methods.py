import os


def read_text_file(file):
    with open(file, "r") as f:
        return f.read()


def create_folder(name):
    if os.path.isdir(name):
        print(f"folder {name} already exists")
    else:
        path = "./" + name
        os.mkdir(path)


def get_folder_size(dir_name):
    return len(
        [
            name
            for name in os.listdir(dir_name)
            if os.path.isfile(os.path.join(dir_name, name))
        ]
    )
