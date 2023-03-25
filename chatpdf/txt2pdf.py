from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册微软雅黑字体
font_path = 'C:/Windows/Fonts/msyh.ttc'  # 字体文件路径
font_name = 'Microsoft YaHei'  # 自定义字体名称
pdfmetrics.registerFont(TTFont(font_name, font_path))

# 设置输入TXT文件和输出PDF文件的名称
input_txt = 'input.txt'
output_pdf = 'output.pdf'

# 读取TXT文件
with open(input_txt, 'r', encoding='utf-8') as file:
    text_content = file.read()

# 创建一个新的PDF文件
doc = SimpleDocTemplate(output_pdf, pagesize=A4, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)

# 设置新的字体大小、行距和字体
styles = getSampleStyleSheet()
normal_style = styles['Normal']
normal_style.fontSize = 12
normal_style.leading = 14
normal_style.fontName = font_name

# 将TXT文件的文本内容添加到输出PDF
text_paragraph = Paragraph(text_content, normal_style)
story = [text_paragraph]

# 保存输出PDF文件
doc.build(story)
