import os
import sys

import pytesseract
from PIL import Image
from tqdm import tqdm


dir_path = sys.argv[1]

for file in tqdm(os.listdir(dir_path)):
    file_path= os.path.join(dir_path, file)
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    result = f"<comic-text file-name='{file}'>\n{text.strip()}\n</comic-text>\n\n"
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write(result)
