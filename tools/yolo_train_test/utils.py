import yaml


def genJson(path,class_name,filename):
    # 创建要写入 YAML 文件的数据结构，使用 OrderedDict
    # 创建要写入 YAML 文件的数据结构，使用列表保持顺序
    data = {
        "path": path,
        "train": "images/train",  # 示例数据
        "val": "images/val",  # 示例数据
        "test": "images/test",  # 示例数据
        "names": {i: name for i, name in enumerate(class_name)}  # 转换为所需格式
    }

    # 使用一个顺序列表来确保输出顺序
    ordered_data = {
        'path': data['path'],
        'train': data['train'],
        'val': data['val'],
        'test': data['test'],
        'names': data['names']
    }

    # 将数据写入 YAML 文件
    with open(filename, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(ordered_data, yaml_file, allow_unicode=True, sort_keys=False)

    print("YAML 文件已成功创建。")

    return True

