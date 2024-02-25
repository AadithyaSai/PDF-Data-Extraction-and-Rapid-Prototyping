# Contains functions for OCR Preprocessing
import functools
import cv2

# import pandas
import pytesseract
from PIL import Image
import pypdfium2 as pdfium


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def process_file(file_path, table_data):
    if file_path.lower().endswith(".pdf"):
        pdf = pdfium.PdfDocument(file_path)
        page = pdf[
            0
        ]  # TODO: make script handle multipage pdfs. As of now the webapp cannot handle such files
        image = page.render(scale=4).to_numpy()
    else:  # assuming all non-pdfs are images
        image = cv2.imread(file_path)

    return process_pic(image, table_data)


def process_pic(image, table_data):
    def greater(a, b):  # for contour sorting L-R
        momA = cv2.moments(a)
        (xa, ya) = int(momA["m10"] / momA["m00"]), int(momA["m01"] / momA["m00"])

        momB = cv2.moments(b)
        (xb, yb) = int(momB["m10"] / momB["m00"]), int(momB["m01"] / momB["m00"])
        if xa > xb:
            return 1

        if xa == xb:
            return 0
        else:
            return -1

    # img = cv2.imread(pic_name, cv2.IMREAD_GRAYSCALE)

    # img_bin = 255-img
    # thresh,img_bin = cv2.threshold(img_bin,128,255,cv2.THRESH_OTSU)

    # image = image_resize(cv2.imread(pic_name), 2000, 2000)

    table_roi = image[
        table_data["y"] : table_data["y"] + table_data["h"],
        table_data["x"] : table_data["x"] + table_data["w"],
    ]
    gray = cv2.cvtColor(table_roi, cv2.COLOR_BGR2GRAY)  # grayscale
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 60
    )
    og_thresh = thresh.copy()

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
    )
    cnts = cv2.findContours(
        remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (0, 0, 0), 5)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 11))
    remove_vertical = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2
    )
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (0, 0, 0), 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, table_data["h"]))
    dilated = cv2.dilate(thresh, kernel, iterations=1)  # dilate

    ocr_data = []
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )  # get contours
    contours = sorted(list(contours), key=functools.cmp_to_key(greater))
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w < 10:
            continue
        cv2.rectangle(table_roi, (x, y), (x + w, y + h), (0, 255, 0))
        text = get_OCR(og_thresh[y : y + h, x : x + w])
        text_lines = [line for line in text.splitlines() if line]
        ocr_data.append(text_lines)

    # remainging image
    image_top = image[: table_data["y"], :]
    gray_top = cv2.cvtColor(image_top, cv2.COLOR_BGR2GRAY)  # grayscale
    thresh_top = cv2.adaptiveThreshold(
        gray_top, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 60
    )
    ocr_top = get_OCR(thresh_top)

    image_bot = image[table_data["y"] + table_data["h"] :, :]
    gray_bot = cv2.cvtColor(image_bot, cv2.COLOR_BGR2GRAY)  # grayscale
    thresh_bot = cv2.adaptiveThreshold(
        gray_bot, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 60
    )
    ocr_bot = get_OCR(thresh_bot)

    return {"top": ocr_top, "bottom": ocr_bot, "table": ocr_data}


def pdf2img(pdf):
    print(pdf)
    pdf = pdfium.PdfDocument(pdf)
    page = pdf[
        0
    ]  # TODO: make script handle multipage pdfs. As of now the webapp cannot handle such files
    image = page.render(scale=4).to_numpy
    cv2.imwrite("/media/pages/img.jpg", image)


def get_OCR(roi, is_table=True):
    if is_table:
        config = "--psm 6 --oem 1"
    else:
        config = "--psm 4 --oem 1"
    return pytesseract.image_to_string(Image.fromarray(roi), config=config)


if __name__ == "__main__":
    td = {"x": 95, "y": 554, "w": 1158, "h": 490}
    process_pic("input/sample1.png", td)
