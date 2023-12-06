from pdf2image import convert_from_path
import fitz

def set_pdf(pdf_path):
    target_path = pdf_path
    # pathlibを用いたパスでも良い

    doc = fitz.open(target_path)

    page_num = 0
    page = doc.load_page(page_num)

    pdf_width = int(page.rect.width)
    pdf_height = int(page.rect.height)

    print(pdf_width)
    print(pdf_height)
    size = str(pdf_width) + 'x' + str(pdf_height)
    pdf_size = None
    if size == '595x842':
        pdf_size = 'A4'
    elif size == '842×1191':
        pdf_size = 'A3'

    images = convert_from_path(target_path)
    for i, image in enumerate(images):
        image.save('img/img'+str(i)+'.jpg', 'JPEG')
    return pdf_size
