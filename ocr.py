import os
import sys
from PIL import Image
import pyocr
import cv2
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as pagesizes
import reportlab.lib.units as unit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdf
from pypdf import PdfReader, PdfWriter, PdfMerger

def ocr(image_names, words, pdf_name, dir_name):
    GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Bold.ttf"
    num_kakeru = 0.127
    for i, image_name in enumerate(image_names):
        file_path = f'img/{image_name}'
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("OCRエンジンが指定されていません")
            sys.exit(1)
        else:
            tool = tools[0]

        img = Image.open(file_path)
        img.show()

        box_builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
        text_contents = tool.image_to_string(img,lang="jpn",builder=box_builder)

        image = Image.open(file_path)
        img2 = cv2.imread(file_path)
        height, width, _ = img2.shape
        pagesize = str(height) + 'x' + str(width)
        print(pagesize)
        # for res in text_position:
        #     print(res.content)

        for l, word in enumerate(words):
            word_len = len(words)
            layer_num = 0
            for j, res in enumerate(text_contents):
                content = res.content
                plus_one = 1
                while word.startswith(content):
                    print(content)
                    minus_one = 1
                    if content == word:
                        print(content, 'マッチしました')
                        # cv2.rectangle(img2, res.position[0], res.position[1], (0, 0, 255), 2)
                        res_start_pos, res_end_pos = res.position
                        print(res_start_pos, res_end_pos)
                        res_start_x_pos = res_start_pos[0] * num_kakeru
                        res_start_y_pos = res_start_pos[1] * num_kakeru
                        res_end_y_pos = res_end_pos[1] * num_kakeru
                        last_start_pos, last_end_pos = text_contents[j + plus_one - 1].position
                        print(last_start_pos, last_end_pos)
                        last_end_x_pos = last_end_pos[0] * num_kakeru
                        last_end_y_pos = last_end_pos[1] * num_kakeru
                        # last_end_x_pos1 = 0
                        # last_end_y_pos1 = 0
                        step_start_x_pos = 0
                        step_start_y_pos = 0
                        # keyword_width = 0
                        # keyword_height = 0
                        keyword_width2 = 0
                        keyword_height2 = 0
                        print(res_start_x_pos, res_start_y_pos, res_end_y_pos, last_end_x_pos, last_end_y_pos)
                        if last_end_y_pos - res_end_y_pos <= 5:
                            print(last_end_y_pos - res_end_y_pos)
                            keyword_width = last_end_x_pos - res_start_x_pos
                            keyword_height = last_end_y_pos - res_start_y_pos
                            print(keyword_width)
                            print(keyword_height)
                        else:
                            while True:
                                print(text_contents[j + plus_one - minus_one - 1].content)
                                last_start_pos, last_end_pos = text_contents[j + plus_one - minus_one - 1].position
                                print(last_start_pos, last_end_pos)
                                last_end_x_pos1 = last_end_pos[0] * num_kakeru
                                last_end_y_pos1 = last_end_pos[1] * num_kakeru

                                if last_end_y_pos1 - res_end_y_pos <= 5:
                                    keyword_width = last_end_x_pos1 - res_start_x_pos
                                    keyword_height = last_end_y_pos1 - res_start_y_pos
                                    last_start_pos, last_end_pos = text_contents[j + plus_one - minus_one + 1].position
                                    print(last_start_pos, last_end_pos)
                                    step_start_x_pos = last_start_pos[0] * num_kakeru
                                    step_start_y_pos = last_start_pos[1] * num_kakeru
                                    keyword_width2 = last_end_x_pos - step_start_x_pos
                                    keyword_height2 = last_end_y_pos - step_start_y_pos
                                    break
                                minus_one += 1
                                print(last_end_y_pos1)
                                print(minus_one)




                        can = canvas.Canvas(f"./layer/layer{layer_num}.pdf", pagesize=pagesizes.A4, bottomup=False)
                        layer_num += 1
                        # can.setFillColorRGB(255, 0, 0, 0)
                        pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
                        font_size = 10
                        can.setFont('GenShinGothic', font_size)
                        can.setStrokeColorRGB(0,0,0,0)
                        can.setFillColorRGB(255, 241, 0, 0.5)
                        # can.drawString(res_start_x_pos * unit.mm, res_start_y_pos * unit.mm , word)

                        can.rect((res_start_x_pos) * unit.mm, res_start_y_pos * unit.mm, (keyword_width) * unit.mm, keyword_height * unit.mm, fill=True)
                        can.rect(step_start_x_pos * unit.mm, step_start_y_pos * unit.mm, (keyword_width2) * unit.mm, keyword_height2 * unit.mm, fill=True)
                        can.showPage()
                        can.save()
                    content += text_contents[j + plus_one].content
                    print(content)

                    plus_one += 1
            if l == 0:
                reader = PdfReader(f'./テストコピー/{dir_name}/{pdf_name}.pdf')
            else:
                reader = PdfReader(f'./created_pdf/{pdf_name} {i}-{l - 1}.pdf')
            pdf = PdfWriter()
            for k in range(layer_num):
                new_pdf = PdfReader(f'./layer/layer{k}.pdf')
                if i == 0 or l == 0:
                    reader.pages[i].merge_page(new_pdf.pages[0])
                else:
                    reader.pages[0].merge_page(new_pdf.pages[0])
            if i == 0 or l == 0:
                pdf.add_page(reader.pages[i])
            else:
                pdf.add_page((reader.pages[0]))
            new_file_name = f'./created_pdf/{pdf_name} {i}-{l}.pdf'
            with open(new_file_name, 'wb') as f:
                pdf.write(f)
            dir = './layer'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
    merger = PdfMerger()
    word_len2 = len(words) - 1
    for m in range(len(image_names)):
        merger.append(f'./created_pdf/{pdf_name} {m}-{word_len2}.pdf')
    merger.write(f'./テストコピー/{dir_name}/{pdf_name} new.pdf')
    merger.close()
    dir = f'./created_pdf'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
