from pdf2image import convert_from_path
import os
from PIL import Image
from tqdm import tqdm


def pdf_extract(pdf_path, output_folder=None):
    print(f"extracting: {pdf_path}")
    pdf_path = os.path.abspath(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    if not output_folder:
        output_folder = os.path.join(os.path.dirname(pdf_path), f"{pdf_name}_image")
    temp_folder = os.path.join(os.path.dirname(pdf_path), "temp")
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

    pdf_pages = convert_from_path(
        pdf_path=pdf_path,
        dpi=200,
        output_folder=temp_folder,
        poppler_path="poppler-20.12.1/bin",
        paths_only=True,
    )

    for i, page in enumerate(tqdm(pdf_pages)):
        page = Image.open(page)  # type: ignore
        page.save(os.path.join(output_folder, f"{pdf_name}_{i}.png"), "png")

    for temp_file in os.listdir(temp_folder):
        try:
            os.remove(os.path.join(temp_folder, temp_file))
        except Exception as e:
            print("删除pdf抽取临时文件错误:", e)
    os.rmdir(temp_folder)
    return output_folder


def extract_folder(pdf_folder, output_folder=None):
    for dir_, folders, files in os.walk(os.path.abspath(pdf_folder)):
        for file_ in files:
            if os.path.splitext(file_)[-1].lower() == ".pdf":
                pdf_extract(os.path.join(dir_, file_), output_folder)


if __name__ == "__main__":
    pdf_extract(r"C:\Users\pro3\Downloads\新建文件夹\科幻世界.1992.06.pdf")
