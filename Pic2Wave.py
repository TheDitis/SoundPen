import cv2
import numpy as np
import wave
import struct
import os


def main(picfile, outfilename):
    picfile = os.path.join('Inputphotos', picfile)
    img = open_image(picfile)
    img = threshold_image(img)
    img = find_contours(img)
    img = cv2.bitwise_not(img)
    wav = make_wave(img)
    create_wav_file(outfilename, wav)


def batch_process(piclst, outnamelist):
    if isinstance(outnamelist, str) or len(outnamelist) == 1:
        if isinstance(outnamelist, list):
            outname = outnamelist[0]
        else:
            outname = outnamelist
        namelen = len(outname)
        for i in range(len(piclst)):
            if i == 0:
                outname = outname + str(i + 1)
            else:
                outname = outname[:namelen] + str(i + 1)
            main(piclst[i], outname)
    if isinstance(outnamelist, list) and len(outnamelist) > 1:
        if len(piclst) != len(outnamelist):
            print("lists must be equal length")
            raise ValueError
        for i in range(len(piclst)):
            main(piclst[i], outnamelist[i])


def open_image(filename):  # Opens file, converts it to grayscale, and inverts it, then outputs it as an array
    img_ = cv2.imread(filename)
    img_ = format_image(img_)
    img_ = cv2.medianBlur(img_, 7)
    ret, img_ = cv2.threshold(img_, 180, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(os.path.join('DebugImages', 'ThresholdTest.png'), img_)
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
    print('\n', len(contours), ' contours found')
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
    cv2.imwrite(os.path.join('DebugImages', 'ContourCheck.png'), cimg)
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
    while (44100 / len(vals)) < 32:
        vals = doublefreq(vals)
    # vals = tune_to_c(vals)
    for value in vals:
        data = struct.pack('<h', int(value))
        out.writeframesraw(data)


def doublefreq(wav):
    outwav = [wav[i] for i in range(len(wav)) if i % 2 == 0]
    return outwav


def halffreq(wav):
    outwav = []
    for i in wav:
        outwav.append(i)
        outwav.append(i)
    return outwav


def find_nearest_c(wav):
    samples = len(wav)
    freq = 44100 / samples
    lowc = 16.35
    cfreqs = [round(lowc * (2 ** i), 2) for i in range(9)]
    nearc = min(cfreqs, key=lambda x: abs(x - freq))
    newlen = round(44100 / nearc)
    print('start freq: ', freq)
    print('c freq list: ', cfreqs)
    print('nearest c freq: ', nearc)
    print('input samples: ', len(wav))
    print('desired samples: ', newlen)
    diff = newlen - samples
    print('difference: ', diff)
    return diff


def tune_to_c(wav):
    samples = len(wav)
    n = find_nearest_c(wav)
    interval = round(abs(samples / n))
    print('interval: ', interval)
    if n == 0:
        print('No tuning needed.')
        newwav = wav
    elif n < 0:
        print('Tuning up')
        newwav = [wav[i] for i in range(samples) if i % interval == 0]
    elif n > 0:
        print('Tuning down')
        newwav = [wav[i] for i in range(samples) if i % interval != 0]
    print('out samples: ', len(newwav))
    return newwav


if __name__ == "__main__":
    input_filename = 'LoopyLine.jpg'  # input file must be placed into Inputphotos folder! Don't use relative path
    output_filename = 'output'  # don't include file extension. It will always be .wav. It will land in the OutputWavs folder

    main(input_filename, output_filename)
