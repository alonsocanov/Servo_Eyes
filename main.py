from image import Image
from i2c import I2C
from utils import regression

def main():
    flip = 0
    dispW = 640
    dispH = 480
    face_file = 'haarcascade/frontalface_default.xml'
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

    servos = {'neck': [0, 4500], 'r_cheak': [1, 5500], 'l_cheak': [2, 6500], 'r_eye': [3, 5500], 'r_eyelid': [4, 8000], 'l_eyelid': [5, 4500], 'l_eye': [6, 4500]}

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



    q_key = False
    while not q_key:
        q_key = image.check_key('q')
        ret, frame = video_capture.read()
        frame = image.resize(frame, (W, H))
        faces = image.detect_cascade(frame, face_cascade)
        pca.set_pca_channel(servos['r_eyelid'][0], 6000)

        if len(faces) == 1:
            x, y, w, h = faces[0]
            frame = image.draw_rect(frame, faces[0])
            face_center = (x + w // 2, y + h // 2)
            frame = image.draw_circle(frame, face_center, 1)
            offset = (face_center[0] - img_center[0],
                      face_center[1] - img_center[1])
            duty_cycle_w = regression(face_center[0], 10000, 1000, W)
            duty_cycle_h = regression(face_center[1], 10000, 1000, h)
            # print(duty_cycle)
            # pca.set_pca_channel(servos['r_eye'][0], 4500)





        # image.show_img(window_name, frame)

    image.release_feed(video_capture)
    image.destroy_windows()


if __name__ == '__main__':
    main()
