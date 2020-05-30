import random
from tqdm import trange

with open('file_to_sort.txt', 'a', encoding='utf-8') as f:
    for _ in trange(1_000_000):
        f.write(str(random.randint(-10000, 10000)) + '\n')
