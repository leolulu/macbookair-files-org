import pypdf
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import utils
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as rlImage, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册微软雅黑字体
font_path = 'C:/Windows/Fonts/msyh.ttc'  # 字体文件路径
font_name = 'Microsoft YaHei'  # 自定义字体名称
pdfmetrics.registerFont(TTFont(font_name, font_path))

# 读取PDF文件
input_pdf = 'input.pdf'
output_pdf = 'output.pdf'

with open(input_pdf, 'rb') as file:
    reader = pypdf.PdfReader(file)
    num_pages = len(reader.pages)

    # 创建一个新的PDF文件
    doc = SimpleDocTemplate(output_pdf, pagesize=A4, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)

    # 设置新的字体大小、行距和字体
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontSize = 8
    normal_style.leading = 10
    normal_style.fontName = font_name

    story = []

    # 循环处理每个原始页面
    for i in range(num_pages):
        # 读取原始页面并将其转换为图像
        page = reader.pages[i]
        if page.extract_text().strip() != "":  # 跳过空白页（方案2）
            print(page.extract_text().strip())
            # 添加原始页面的文本内容到输出PDF（方案1、3）
            text_content = page.extract_text()
            if text_content.strip():
                text_paragraph = Paragraph(text_content, normal_style)
                story.append(text_paragraph)

            # 添加一个分隔符
            story.append(Spacer(0, 0.25 * inch))

    # 保存输出PDF文件
    doc.build(story)
