import os
import re
import sys
from collections import Counter

txt_content_for_save = []


def index_word(word):
    with open("coca20000.txt", "r", encoding="utf-8") as f:
        coca_data = f.read().strip().split("\n")
    word = word[0]
    try:
        rank = coca_data.index(word)
        rank += 1
    except ValueError:
        rank = 99999
    return rank


def print_with_save(content):
    print(content)
    txt_content_for_save.append(content)


def filter_difficult_word(txt_file_path):
    with open(txt_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    sentences = content.split("\n")
    sentences = [i.strip() for i in sentences]

    words = re.findall(r"\w+", content)
    count = [[i[0], i[1]] for i in Counter(words).items()]
    result = [[w, index_word(w)] for w in count]
    result.sort(key=lambda x: x[1])
    # result格式
    # ['fitness', 8]  3386
    # [单词  出现次数] 词频

    # 剔除没有词频的词
    result = [i for i in result if i[-1] != 99999]
    # 剔除词频小于1000的词
    result = [i for i in result if i[-1] > 8000]
    # 筛选出现次数大于1的词
    # result = [i for i in result if i[0][1] >= 1]

    print_with_save("".join(["出现次数".ljust(8), "词频".ljust(12), "单词"]))
    for i in [i for i in result if i[0][1] >= 2]:
        print_with_save("".join([str(i[0][1]).ljust(8), str(i[1]).ljust(12), f"【【【{i[0][0]}】】】".ljust(20)]))
        for s in sentences:
            # if s.find(i[0][0]) != -1:
            if i[0][0] in re.findall(r"\w+", s):
                s = s.replace(i[0][0], f"【{i[0][0]}】")
                print_with_save(f">>> {s}")
        print_with_save("")

    print_with_save("\n\n                    字母顺序排序:")
    for i in sorted(result, key=lambda x: x[0][0]):
        print_with_save("".join([str(i[0][1]).ljust(8), str(i[1]).ljust(12), i[0][0].ljust(20)]))

    print_with_save("\n\n")
    print_with_save("".join(["出现次数".ljust(8), "词频".ljust(12), "单词"]))
    for i in [i for i in result if i[0][1] >= 2]:
        print_with_save("".join([str(i[0][1]).ljust(8), str(i[1]).ljust(12), i[0][0].ljust(20)]))

    print_with_save("\n\n用来复制高亮的:")
    for i in [i for i in result if i[0][1] >= 1]:
        print_with_save(i[0][0])

    with open("_coca".join(os.path.splitext(txt_file_path)), "w", encoding="utf-8") as f:
        f.write("\n".join(txt_content_for_save))


if __name__ == "__main__":
    filter_difficult_word(sys.argv[1])
