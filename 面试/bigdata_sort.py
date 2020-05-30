import math
import os


class ReadDataPointer:
    '''
    指针对象
    使用文件句柄，遍历外部文件
    '''

    def __init__(self, f_r):
        self.f_r = f_r
        self.current_value = self.f_r.__next__().strip()

    def get_next_value(self):
        try:
            self.current_value = self.f_r.__next__().strip()
        except StopIteration:
            self.current_value = None


class BigDataSort:
    def __init__(self, file_path, split_num):
        self.file_path = file_path
        self.split_num = split_num

    def get_total_count(self):
        f = open(self.file_path, 'r', encoding='utf-8')
        self.row_num = 0
        for _ in f:
            self.row_num += 1
        self.batch_num = math.ceil(self.row_num / self.split_num)
        print('row_num:', self.row_num)
        print('batch_num:', self.batch_num)
        f.close()

    def data_split(self):
        self.store_file_list = ['block_data_{}.txt'.format(i) for i in range(self.split_num)]
        counter = 0
        i = 0
        with open('file_to_sort.txt', 'r', encoding='utf-8') as f_r:
            for row in f_r:
                counter += 1
                if counter > self.batch_num:
                    i += 1
                    counter = 0
                with open(self.store_file_list[i], 'a', encoding='utf-8') as f_w:
                    f_w.write(row.strip() + '\n')

    def sort_within_file(self):
        for file_path in self.store_file_list:
            with open(file_path, 'r', encoding='utf-8') as f_r:
                data = [int(i) for i in f_r.read().split('\n') if i != '']
            os.remove(file_path)
            for i in sorted(data, reverse=True):
                with open(file_path, 'a', encoding='utf-8') as f_w:
                    f_w.write(str(i) + '\n')

    def concat_sort_result(self):
        pointer_list = [open(i, 'r', encoding='utf-8') for i in self.store_file_list]
        rdpointer_list = [ReadDataPointer(i) for i in pointer_list]

        while True:
            rdpointer_list = [i for i in rdpointer_list if i.current_value is not None]
            if len(rdpointer_list) == 0:
                break
            rdpointer_list = sorted(rdpointer_list, key=lambda x: int(x.current_value), reverse=True)
            with open('sorted_result.txt', 'a', encoding='utf-8') as f:
                f.write(rdpointer_list[0].current_value + '\n')
            rdpointer_list[0].get_next_value()

    def run(self):
        # 1. 获取待排序数据总数，根据split_num，计算出每个分隔文件的行数
        self.get_total_count()
        # 2. 将待排序数据存储为split_num个不同的本地txt文件，每个数字一行
        self.data_split()
        # 3. 使用python内置的sort功能，读取对每个块，进行内存中的排序，然后写回本地文件
        self.sort_within_file()
        # 使用多指针，将排序好的所有block组合在一起，按行写入结果文件（降序）
        self.concat_sort_result()


if __name__ == "__main__":
    bds = BigDataSort('file_to_sort.txt', 10)   # 输入文件路径，分块数
    bds.run()
