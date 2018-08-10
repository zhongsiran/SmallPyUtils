import os
import sys
from itertools import zip_longest
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas

# jpg_files = ['1.jpg', '2.jpg', '3.jpg']


def conpdf(photos_files, pdf_name):
    (w, h) = portrait(A4)
    c = canvas.Canvas(pdf_name, pagesize=portrait(A4))
    for i in range(0, len(photos_files)):
        c.drawImage(os.getcwd() + '/jpgs/' + photos_files[i], 0, 0, w, h)
        c.showPage()
    c.save()

def is_jpg(file_name):
    if 'jpg' in file_name.lower():
        if file_name != '0.jpg':
            return file_name

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

all_files = os.listdir(os.getcwd() + '/jpgs/')
all_files.sort(key=lambda x:int(x[:-4]))
jpg_files = list(filter(is_jpg, all_files))
# for jpg in jpg_files:
#     print(jpg)
# conpdf(files)

print(list(grouper(jpg_files, 3, '0.jpg')))
corp_list = ['dokn', 'okno', 'ooddkn']
i = 0
for photo_pack in list(grouper(jpg_files, 3, '0.jpg')):
    pdf_name =  corp_list[i] + '.pdf'
    conpdf(photo_pack, pdf_name)
    i += 1