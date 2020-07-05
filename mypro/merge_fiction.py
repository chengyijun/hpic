import pymongo

from tools import get_config


def merge_chapters():
    config = get_config()
    name = config.get('fiction').get('name')
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["fcitions"]
    mycol = mydb[name]

    for data in mycol.find().sort("index"):
        content = data.get('content')
        content = content.replace('　　', '\n\t')
        with open(f'./{name}.txt', 'a', encoding='utf-8') as f:
            f.write(data.get('title') + '\r\n\r\n' + content + '\r\n\r\n')
    print('合成结束')


def main():
    merge_chapters()


if __name__ == '__main__':
    main()
