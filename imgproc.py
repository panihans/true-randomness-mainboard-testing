import configparser
from pathlib import Path

import cv2 as cv
import numpy as np

config = configparser.ConfigParser()
config['DEFAULT'] = {
    'lH': '89',
    'lS': '128',
    'lV': '128',
    'hH': '179',
    'hS': '255',
    'hV': '255',
    'img': '1'
}
config['VALUES'] = {}

defaults_uri = './trackbar_defaults.txt'
defaults = Path(defaults_uri)


def write_config():
    with open(defaults_uri, 'w') as configfile:
        config.write(configfile)


def read_config():
    config.read(defaults_uri)


trackbar_window = 'trackbars'

lower_b = np.array([0, 0, 0])
upper_b = np.array([179, 255, 255])


def update_cv2_inrange_bounds():
    global lower_b, upper_b
    lower_b = np.array([cv.getTrackbarPos('lH', trackbar_window),
                        cv.getTrackbarPos('lS', trackbar_window),
                        cv.getTrackbarPos('lV', trackbar_window)])
    upper_b = np.array([cv.getTrackbarPos('hH', trackbar_window),
                        cv.getTrackbarPos('hS', trackbar_window),
                        cv.getTrackbarPos('hV', trackbar_window)])


def trackbar_updated(value=None):
    config['VALUES'] = {
        'lH': cv.getTrackbarPos('lH', trackbar_window),
        'lS': cv.getTrackbarPos('lS', trackbar_window),
        'lV': cv.getTrackbarPos('lV', trackbar_window),
        'hH': cv.getTrackbarPos('hH', trackbar_window),
        'hS': cv.getTrackbarPos('hS', trackbar_window),
        'hV': cv.getTrackbarPos('hV', trackbar_window),
        'img': cv.getTrackbarPos('img', trackbar_window)
    }
    update_cv2_inrange_bounds()
    write_config()


def load_trackbars(config_name):
    cv.setTrackbarPos('lH', trackbar_window, config.getint(config_name, "lH"))
    cv.setTrackbarPos('lS', trackbar_window, config.getint(config_name, "lS"))
    cv.setTrackbarPos('lV', trackbar_window, config.getint(config_name, "lV"))
    cv.setTrackbarPos('hH', trackbar_window, config.getint(config_name, "hH"))
    cv.setTrackbarPos('hS', trackbar_window, config.getint(config_name, "hS"))
    cv.setTrackbarPos('hV', trackbar_window, config.getint(config_name, "hV"))


def save_trackbars(config_name):
    config[config_name] = {
        'lH': cv.getTrackbarPos('lH', trackbar_window),
        'lS': cv.getTrackbarPos('lS', trackbar_window),
        'lV': cv.getTrackbarPos('lV', trackbar_window),
        'hH': cv.getTrackbarPos('hH', trackbar_window),
        'hS': cv.getTrackbarPos('hS', trackbar_window),
        'hV': cv.getTrackbarPos('hV', trackbar_window),
        'img': cv.getTrackbarPos('img', trackbar_window)
    }
    write_config()


def main():
    read_config()
    cv.namedWindow(trackbar_window)
    cv.resizeWindow(trackbar_window, 300, 600)

    cv.createTrackbar('lH', trackbar_window, config.getint("VALUES", "lH"), 179, trackbar_updated)
    cv.createTrackbar('lS', trackbar_window, config.getint("VALUES", "lS"), 255, trackbar_updated)
    cv.createTrackbar('lV', trackbar_window, config.getint("VALUES", "lV"), 255, trackbar_updated)
    cv.createTrackbar('hH', trackbar_window, config.getint("VALUES", "hH"), 179, trackbar_updated)
    cv.createTrackbar('hS', trackbar_window, config.getint("VALUES", "hS"), 255, trackbar_updated)
    cv.createTrackbar('hV', trackbar_window, config.getint("VALUES", "hV"), 255, trackbar_updated)
    cv.createTrackbar('img', trackbar_window, config.getint("VALUES", "img"), 8, trackbar_updated)
    trackbar_updated()

    se1 = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
    while True:
        frame = cv.imread(f'imgs/Capture{config.getint("VALUES", "img") + 1}.PNG')
        frame_2 = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        h, w, c = frame.shape
        blank = (np.zeros((h, w, 3), np.uint8))
        blank[:] = (255, 255, 255)
        blank = cv.rectangle(blank, (0, h-75), (w, h), (0, 0, 0),cv.FILLED)

        frame_2 = cv.bitwise_and(frame_2, blank)


        # frame_2 = cv.GaussianBlur(frame_2, (15, 15), 15)
        # frame_2 = cv.medianBlur(frame_2, 11)
        frame_2 = cv.erode(frame_2, se1)
        frame_2 = cv.dilate(frame_2, se1)

        cv.imshow('og', frame)
        cv.imshow('hsv', frame_2)
        thresh_img = cv.inRange(frame_2, lower_b, upper_b)
        cv.imshow('thresh', thresh_img)

        key = cv.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('w'):
            config_name = input('write trackbars to: ')
            if len(config_name) > 1:
                save_trackbars(config_name)
        if key & 0xFF == ord('r'):
            config_name = input('read trackbars from: ')
            if len(config_name) > 1:
                load_trackbars(config_name)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
