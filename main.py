from image import Image
from pwm_control import PWM


def main():
    face_file = 'haarcascade/frontalface_default.xml'
    image = Image(0)
    window_name = 'Frame'
    image.set_window(window_name)
    video_capture, w, h = image.video_capure()
    W, H = image.factor((w, h))
    face_cascade = image.cascade_clasifier(face_file)
    img_center = (W // 2, H // 2)
    servo = PWM()
    servo.start()

    q_key = False
    while not q_key:
        q_key = image.check_key('q')
        ret, frame = video_capture.read()
        frame = image.resize(frame, (W, H))
        faces = image.detect_cascade(frame, face_cascade)
        if len(faces) == 1:
            x, y, w, h = faces[0]
            frame = image.draw_rect(frame, faces[0])
            face_center = (x + w // 2, y + h // 2)
            frame = image.draw_circle(frame, face_center, 1)
            offset = (face_center[0] - img_center[0],
                      face_center[1] - img_center[1])
            duty_cycle = servo.pixelsToDutyCycle(offset[0], img_center[0])
            print(duty_cycle)

        image.show_img(window_name, frame)

    image.release_feed(video_capture)
    image.destroy_windows()


if __name__ == '__main__':
    main()
