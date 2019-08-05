import cv2
import numpy as np
import wave
import struct
import os


def __main__(picfile, outfilename):
    picfile = os.path.join('Inputphotos', picfile)
    img = open_image(picfile)
    img = threshold_image(img)
    img = find_contours(img)
    img = cv2.bitwise_not(img)
    wav = make_wave(img)
    create_wav_file(outfilename, wav)


def open_image(filename):  # Opens file, converts it to grayscale, and inverts it, then outputs it as an array
    img_ = cv2.imread(filename)
    img_ = format_image(img_)
    img_ = cv2.medianBlur(img_, 7)
    ret, img_ = cv2.threshold(img_, 180, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(os.path.join('DebugCheckImages', 'ThresholdTest.png'), img_)
    arrayimg = np.asarray(img_)
    return arrayimg


def format_image(image):
    img_ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    img_ = cv2.bitwise_not(img_)  # inverts image
    return img_


def threshold_image(image):  # First blurs the image, then thresholds it
    blur = cv2.GaussianBlur(image, (5, 5), 1)  # blurs image for better thresholding
    ret, img_ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Makes image binary B&W
    return img_


def find_contours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print(len(contours), ' contours found')
    if len(contours) > 100:
        print('Contour count is high, a cleaner picture might be needed.')
    bestcurveindex = find_longest_contour(contours)
    blank = create_blank(image)
    cv2.drawContours(blank, contours, bestcurveindex, (255, 255, 255), 2)
    slope = get_avg_slope(blank, contours, bestcurveindex, drawline=False)
    if len(contours) > 100:
        while abs(slope) > 2:
            contours.pop(bestcurveindex)
            bestcurveindex = find_longest_contour(contours)
            blank = create_blank(image)
            cv2.drawContours(blank, contours, bestcurveindex, (255, 255, 255), 2)
            slope = get_avg_slope(blank, contours, bestcurveindex, drawline=False)
    cimg = blank
    cv2.imwrite(os.path.join('DebugCheckImages', 'ContourCheck.png'), cimg)
    cimg = format_image(cimg)
    return cimg


def find_longest_contour(cont):
    perimeterlist = [cv2.arcLength(i, False) for i in cont]
    bestindex = perimeterlist.index(max(perimeterlist))
    return bestindex


def create_blank(image):
    shape = image.shape
    w = shape[1]
    h = shape[0]
    blank_image = np.zeros(shape=[h, w, 3], dtype=np.uint8)
    return blank_image


def get_avg_slope(img_, cont, index, drawline=False):
    rows, cols = img_.shape[:2]
    [vx, vy, x, y] = cv2.fitLine(cont[index], cv2.DIST_L2, 0, 0.01, 0.01)
    lefty = int((-x * vy / vx) + y)
    righty = int(((cols - x) * vy / vx) + y)
    slope = (lefty - righty) / (cols - 1)
    if drawline:
        cv2.line(img_, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
    return slope


def make_wave(image):
    print('Creating Wave')
    wav_ = []
    height = image.shape[0]
    width = image.shape[1]
    prevprog = None
    for i in range(width):
        prog = progress(i, width)
        if prog != prevprog and prog % 5 == 0:
            print(str(prog) + '%')
        col = image[:, i]
        for j in range(height):
            if col[j] == 255:
                wav_.append(height - j)
                break
        prevprog = prog
    wav_ = center(wav_)
    wav_ = centerwave(wav_)
    wav_ = rescalewave(wav_)
    return wav_


def center(vals):
    range_ = max(vals) - min(vals)
    sub = range_ / 2
    newvals = [v - sub for v in vals]
    return newvals


def centerwave(vals):
    start, end = vals[0], vals[-1]
    avg = round((start + end) / 2, 3)
    newvals = [round(n - avg, 3) for n in vals]
    return newvals


def rescalewave(vals):
    premax = max(max(vals), abs(min(vals)))
    outmax = 32700
    diff = outmax / premax
    outvals = [round(i * diff, 3) for i in vals]
    return outvals


def progress(cur, tot):
    percent = round((cur * 100) / tot)
    return percent


def create_wav_file(fname, vals):
    outfilename = os.path.join('OutputWavs', (fname + '.wav'))
    out = wave.open(outfilename, 'w')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(44100)

    for value in vals:
        data = struct.pack('<h', int(value))
        out.writeframesraw(data)


__main__('PhonePhoto17.jpg', 'OutputWav17')
