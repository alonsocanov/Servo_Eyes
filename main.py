from turtle import window_width
from image import Image
import cv2


def main():
    face_file = 'haarcascade/frontalface_default.xml'
    image = Image(0)
    window_name = 'Frame'
    image.set_window(window_name)
    video_capture, w, h = image.video_capure()
    W, H = image.factor((w, h))
    face_cascade = image.cascade_clasifier(face_file)

    q_key = False
    while not q_key:
        q_key = image.check_key('q')
        ret, frame = video_capture.read()
        frame = image.resize(frame, (W, H))
        faces = image.detect_cascade(frame, face_cascade)
        for x, y, w, h in faces:
            frame = image.draw_rect(frame, (x, y, w, h))
        cv2.imshow(window_name, frame)

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
