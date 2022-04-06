import cv2
import numpy as np
import glob
import sys


class Image:
    def __init__(self, file_path: None) -> None:
        # check available files in path
        if isinstance(file_path, str):
            # full_path = glob.glob(file_path, recursive=True)
            # if full_path:
            self.__path = file_path
            # else:
                # print('No file with that path')
                # sys.exit(1)
        elif isinstance(file_path, int):
            self.__path = file_path
        else:
            print('No file with that path')
            sys.exit(1)

    def set_window(self, name: str = 'Frame', x_pos: int = 20, y_pos: int = 20):
        cv2.namedWindow(name)
        cv2.moveWindow(name, x_pos, y_pos)

    def gray(self, img: np.ndarray):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def gaussian_blur(self, img, kernel: tuple = (7, 7), skip: int = 0):
        return cv2.GaussianBlur(img, kernel, skip)

    def canny_edge_detector(self, img, threshold_1: int = 100, threshold_2: int = 200):
        return cv2.Canny(img, threshold_1, threshold_2)

    def hsv_to_cv_hsv(self, hsv: np.ndarray) -> np.ndarray:
        '''
        Color normalization of HSV to OpenCV HSV
        For HSV, Hue range is [0,179], Saturation range is [0,255]
        and Value range is [0,255]. Different software use different scales.
        So if you are comparing in OpenCV values with them, you need to normalize these ranges.
        '''
        hsv_cv = np.array([179, 255, 255])
        hsv_orig = np.array([360, 100, 100])
        cv_hsv = np.divide((hsv * hsv_cv), hsv_orig)
        return cv_hsv

    def video_capure(self):
        video_capture = cv2.VideoCapture(self.__path)
        if video_capture.isOpened():
            # width
            width = video_capture.get(3)
            # height
            height = video_capture.get(4)
            return (video_capture, width, height)
        print('Video Capture not opened')
        sys.exit(1)

    def check_key(self, c: str = 'q') -> bool:
        '''check if key q was pressed'''
        if cv2.waitKey(1) & 0xFF == ord(c):
            return True
        return False

    def factor(self, dim: tuple, factor: float = 1.0):
        if factor == 1.0:
            factor = 300 / dim[1]
        return (int(factor * dim[0]), int(factor * dim[1]))

    def resize(self, img: np.ndarray, dim: tuple) -> np.array:
        return cv2.resize(img, (dim[0], dim[1]))

    def prespective_transform(self, source_pts, destination_pts):
        return cv2.getPerspectiveTransform(source_pts, destination_pts)

    def wrap_prespective(self, img, transform_matrix, dim):
        return cv2.warpPerspective(img, transform_matrix, dim)

    def mask_region_of_interest(self, dim, vertices):
        mask = np.zeros((dim[1], dim[0], 1), dtype=np.uint8)
        cv2.fillPoly(mask, vertices, (255))
        return mask

    def bitwise_and(self, img_1, img_2):
        return cv2.bitwise_and(img_1, img_2)

    def hough_lines(self, img: np.ndarray, rho: float, theta: float, threshold: int, min_length: int, max_gap: int):
        lines = cv2.HoughLinesP(img, rho=rho, theta=theta, threshold=threshold,
                                minLineLength=min_length, maxLineGap=max_gap)
        return np.squeeze(lines)

    def get_slope(self, lines: np.ndarray):
        denominator = lines[:, 2] - lines[:, 0]
        denominator = np.where(denominator == 0, .1, denominator)
        numerator = lines[:, 3] - lines[:, 1]
        return numerator / denominator

    def filter_slope(self, lines: np.array, max_slope: float = 0.5):
        slope = self.get_slope(lines)
        return lines[np.abs(slope) > max_slope]

    def left_right_lanes(self, lines: np.ndarray):
        slope = self.get_slope(lines)
        left_lane = lines[slope <= 0]
        right_lane = lines[slope > 0]
        return left_lane, right_lane

    def draw_lines(self, img: np.ndarray, lines: np.ndarray):
        line_thickness = 2
        for x1, y1, x2, y2 in lines:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0),
                     thickness=line_thickness)

    def draw_rect(self, img, coor, color=(255, 0, 0), thicknes=2):
        x, y, w, h = coor
        return cv2.rectangle(img, (x, y), (x + w, y + h), color, thicknes)

    def draw_circle(self, img, coor, rad, color=(0, 255, 0), thicknes=2):
        x, y = coor
        return cv2.circle(img, (x, y), rad, color, thicknes)

    def cascade_clasifier(self, path):
        return cv2.CascadeClassifier(path)

    def detect_cascade(self, img, cascade):
        return cascade.detectMultiScale(img)

    def show_img(self, win_name, img):
        cv2.imshow(win_name, img)

    def destroy_windows(self):
        cv2.destroyAllWindows()

    def release_feed(self, feed):
        feed.release()
