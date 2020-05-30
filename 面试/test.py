class RPointer:
    def __init__(self, f_r):
        self.f_r = f_r
        self.current_value = self.f_r.__next__().strip()

    def get_next_value(self):
        try:
            self.current_value = self.f_r.__next__().strip()
        except StopIteration:
            self.current_value = None


file_list = ['block_data_0.txt', 'block_data_1.txt', 'block_data_3.txt']

pointer_list = [open(i, 'r', encoding='utf-8') for i in file_list]

rpointer_list = [RPointer(i) for i in pointer_list]


result_list = []
while rpointer_list:
    rpointer_list = [i for i in rpointer_list if i.current_value is not None]
    if len(rpointer_list) == 0:
        break
    rpointer_list = sorted(rpointer_list, key=lambda x: x.current_value, reverse=True)
    result_list.append(rpointer_list[0].current_value)
    print(
        [i.current_value for i in rpointer_list], '\n', result_list
    )
    rpointer_list[0].get_next_value()
