from turtle import window_width
from image import Image
import cv2


def main():
    image = Image(0)
    window_name = 'Frame'
    image.set_window(window_name)
    video_capture, w, h = image.video_capure()
    w, h = image.factor((w, h))

    q_key = False
    while not q_key:
        q_key = image.check_key('q')
        ret, frame = video_capture.read()
        frame = image.resize(frame, (w, h))

        cv2.imshow(window_name, frame)

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
