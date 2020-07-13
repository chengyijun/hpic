import os

import yaml


def get_config():
    yaml_file = os.path.join(os.getcwd(), "config.yml")
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


def main():
    print(get_config())


if __name__ == '__main__':
    main()
