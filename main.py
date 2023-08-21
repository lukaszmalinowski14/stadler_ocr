from pytesseract import *
import argparse
import cv2
from pathlib import Path


def czytanie_wartosci_komorki(x, y, w, h, kolumna):
    conf1 = "--psm 7 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    conf2 = '--psm 7 --oem 1 -c tessedit_char_whitelist=X0123456789,.'

    if kolumna in (0, 1, 2, 6, 7):
        conf = conf2
    else:
        conf = conf1
    finalimg = rgb[y:y+h, x:x+w]
    # finalimg.show()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    # border = cv2.copyMakeBorder(
    #     finalimg, 2, 2, 2, 2,   cv2.BORDER_CONSTANT, value=[255, 255])
    resizing = cv2.resize(finalimg, None, fx=2,
                          fy=2, interpolation=cv2.INTER_CUBIC)
    # dilation = cv2.dilate(resizing, kernel, iterations=1)
    # erosion = cv2.erode(dilation, kernel, iterations=1)
    cv2.imwrite(str(Path.cwd())+"/resize.png", resizing)
    out = pytesseract.image_to_string(resizing)
    if (len(out) == 0):
        # PSM 3 dla złozonych i poj wyrazów
        ##
        out = pytesseract.image_to_string(
            resizing, config=conf)
    print(f"odczytany teskt to {out}")


def korekta(x, y, w, h, kolumna):
    if kolumna in (0, 1, 2, 3, 6, 7):
        x += 5
        y += 5
        w -= 10
        h -= 10
    elif kolumna in (4, 5):
        x = x
        y = y
        w = w
        h = h

    return x, y, w, h

# We construct the argument parser
# and parse the arguments
# ap = argparse.ArgumentParser()

# ap.add_argument("-i", "--image",
#                 required=True,
#                 help="d.jpg")
# ap.add_argument("-c", "--min-conf",
#                 type=int, default=0,
#                 help="5")
# args = vars(ap.parse_args())


# We load the input image and then convert
# it to RGB from BGR. We then use Tesseract
# to localize each area of text in the input
# image
images = cv2.imread("table.png")
rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

# Then loop over each of the individual text
# localizations
# for i in range(0, len(results["text"])):

#     # We can then extract the bounding box coordinates
#     # of the text region from the current result

#     x = results["left"][i]
#     y = results["top"][i]
#     w = results["width"][i]
#     h = results["height"][i]


#     # We will also extract the OCR text itself along
#     # with the confidence of the text localization
#     text = results["text"][i]
#     conf = int(results["conf"][i])

#     # filter out weak confidence text localizations
#     if conf > 0:

#         # We will display the confidence and text to
#         # our terminal
#         print("Confidence: {}".format(conf))
#         print("Text: {}".format(text))
#         print("")

#         # We then strip out non-ASCII text so we can
#         # draw the text on the image We will be using
#         # OpenCV, then draw a bounding box around the
#         # text along with the text itself
#         text = "".join(text).strip()
#         cv2.rectangle(images,
#                       (x, y),
#                       (x + w, y + h),
#                       (0, 0, 255), 2)
#         cv2.putText(images,
#                     text,
#                     (x, y - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1.2, (0, 255, 255), 3)

# XXXXXXXXXXXXXXXXXXXXXXXXXX
lines_y = [10, 80, 140, 210, 280, 355, 420, 492, 560,
           630, 690, 768, 830, 905, 960, 1040, 1100]

lines_x = [30, 120, 220, 510, 580, 950, 1500, 1820, 1960]

# wyznaczenie punktów przeciecia linni
count_x = 0
count_y = 0

for x_line in lines_x:
    for y_line in lines_y:
        x, y = (x_line, y_line)
        if count_x < 8:
            w = lines_x[count_x+1]-x_line
        else:
            continue
        if count_y < 16:
            h = lines_y[count_y+1]-y_line
        else:
            continue

        (x, y, w, h) = korekta(x, y, w, h, count_x)
        czytanie_wartosci_komorki(x, y, w, h, count_x)
        cv2.rectangle(images,
                      (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)

        cv2.imshow("Image", images)
        cv2.waitKey(0)
        count_y += 1
    count_x += 1
    count_y = 0
# y = 290
# x = 40
# w = 70
# h = 60
# y = 280
# x = 950
# w = 500
# h = 75
# y = 280
# x = 580
# w = 370
# h = 75
text = "test"
cv2.rectangle(images,
              (x, y),
              (x + w, y + h),
              (0, 0, 255), 2)
# cv2.putText(images,
#             text,
#             (x, y - 10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             1.2, (0, 255, 255), 3)


# przesłanie fragmentu obrazu do OCR
# bitxor = cv2.bitwise_xor(img, img_vh)
# bitnot = cv2.bitwise_not(bitxor)
finalimg = rgb[y:y+h, x:x+w]
# finalimg.show()
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
# border = cv2.copyMakeBorder(
#     finalimg, 2, 2, 2, 2,   cv2.BORDER_CONSTANT, value=[255, 255])
resizing = cv2.resize(finalimg, None, fx=2,
                      fy=2, interpolation=cv2.INTER_CUBIC)
# dilation = cv2.dilate(resizing, kernel, iterations=1)
# erosion = cv2.erode(dilation, kernel, iterations=1)
cv2.imwrite(str(Path.cwd())+"/resize.png", resizing)
out = pytesseract.image_to_string(resizing)
if (len(out) == 0):
    # PSM 3 dla złozonych i poj wyrazów
    ##
    out = pytesseract.image_to_string(
        resizing, config='--psm 7 --oem 1 -c tessedit_char_whitelist=ABCDEFGHOJKLMNOPRSTUVWXZYQ0123456789')
print(f"odczytany teskt to {out}")


###############################################################

# After all, we will show the output image
cv2.imshow("Image", images)
cv2.waitKey(0)
