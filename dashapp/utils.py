import os
import shutil
from IPython.core.interactiveshell import ExecutionInfo
from tqdm import tqdm


def image_picker_quantitative(img_base_path, quantity: int, move: bool):
    execution_mode = shutil.move if move else shutil.copy
    img_base_path = os.path.abspath(img_base_path)
    img_list = []
    for root_, dirs_, files_ in os.walk(img_base_path):
        for file_ in files_:
            img_list.append(os.path.join(img_base_path, root_, file_))
    img_list.sort()
    n = 0
    for img in tqdm(img_list):
        n += 1
        target_folder_path = os.path.join(img_base_path, f'{quantity}_{n//quantity+1}')
        if not os.path.exists(target_folder_path):
            os.mkdir(target_folder_path)
        execution_mode(img, target_folder_path)


if __name__ == "__main__":
    image_picker_quantitative(
        r"C:\Dpan\python-script\macbookair-files\dashapp\static\img",
        200,
        True
    )
