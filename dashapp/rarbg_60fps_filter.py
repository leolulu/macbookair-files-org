import os
import re
import json


def package_json_data(dir_path):
    result = []
    for json_file_name in os.listdir(dir_path):
        json_file_path = os.path.join(dir_path, json_file_name)
        if os.path.splitext(json_file_path)[-1] == '.json':
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = f.read()
                data = json.loads(data)
                result.extend(data)
    return result


def parse_json(json_data):
    temp_fps_result = []
    for row in json_data:
        desc = row['desc']
        desc = desc.split('\n')
        desc = map(lambda x: x.lower().strip(), desc)
        desc = [i for i in desc if i != '']
        name = row['name']
        page_url = row['page_url']
        magnet = row['magnet']
        for desc_row in desc:
            fps_re_find_result = re.findall(r"frame.*?(\d+\.?\d*)", desc_row)
            if fps_re_find_result:
                fps = float(fps_re_find_result[0])
                if fps >= 50:
                    temp_fps_result.append((fps, name))
                    print(magnet)
            elif desc_row.find('frame') != -1:
                print("有frame，但是没有取到fps：", name, desc_row)

    print("================================" * 5)
    for i in sorted(temp_fps_result, key=lambda x: x[1]):
        print('\t'.join(map(lambda x: str(x), i)))
    print("")


# for i in img_url_page_url_list[::-1]:
#     with open('rarbg.history', 'r', encoding='utf-8') as f:
#         his = f.read().split('\n')
#     if str(i) not in his:
#         print(i)
#         with open('rarbg.history', 'a', encoding='utf-8') as f:
#             f.write('\n'+str(i))
#     else:
#         img_url_page_url_list.remove(i)

# print(img_url_page_url_list)

if __name__ == '__main__':
    json_data = package_json_data(r"C:\Users\sisplayer\Downloads")
    parse_json(json_data)
