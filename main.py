from image import Image
from pwm_control import PWM
from i2c import I2C


def main():
    flip = 0
    dispW = 640
    dispH = 480
    face_file = 'haarcascade/frontalface_default.xml'
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    image = Image(camSet)
    window_name = 'Frame'
    image.set_window(window_name)
    video_capture, w, h = image.video_capure()
    W, H = image.factor((w, h))
    face_cascade = image.cascade_clasifier(face_file)
    img_center = (W // 2, H // 2)
    pca = I2C()
    pca.set_pca9685()
    #1000 10000
    for c in range(0, 8):
        for i in range(100, 5000, 1):
            print(i)
            pca.set_pca_channel(c,i)


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
            # duty_cycle_x = servo.pixelsToDutyCycle(offset[0], img_center[0])
            # duty_cycle_y = servo.pixelsToDutyCycle(offset[1], img_center[1])


        image.show_img(window_name, frame)

    image.release_feed(video_capture)
    image.destroy_windows()


if __name__ == '__main__':
    main()
