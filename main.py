from search_dir import search
from pdf import set_pdf
from excel import excel
from ocr import ocr
import os, glob
import pathlib


excel_text = excel()
print(excel_text)

for search_words in excel_text:
    dir_names = str(search_words[0]).split(',')
    words = str(search_words[1]).split(',')
    print(dir_names)

    for dir_name in dir_names:
        path_cd = pathlib.Path()
        dir_path = search(dir_name)
        dir_name2 = str(dir_path).split('/')[1]
        print(dir_path)
        for f in glob.glob(f'{dir_path}/*.pdf'):
            pdf_name = str(os.path.split(f)[1]).split('.')[0]
            pdf_path = dir_path + '/' + str(os.path.split(f)[1])
            print(pdf_path)
            pdf_size = set_pdf(pdf_path)
            print(pdf_size)
            img_names = []

            path_cd = pathlib.Path()
            for img in glob.glob('img/*.jpg'):
                print(img)
                img_names.append(str(img).split('/')[-1])
                print(img_names)
            print(words)
            print(pdf_name)
            print(dir_name2)
            ocr(img_names, words, pdf_name, dir_name2)
            dir = './img'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
