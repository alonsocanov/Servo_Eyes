from image import Image
from i2c import I2C
from utils import regression
import cv2

servos = {'neck': 0, 'r_cheak': 1, 'l_cheak': 2, 'r_eye': 3, 'r_eyelid': 4, 'l_eyelid': 5, 'l_eye': 6}

servos_limits = {'neck': [1000, 10000], 'r_cheak': [2500, 8500], 'l_cheak': [3500, 9500], 'r_eye': [4500, 6500], 'r_eyelid': [1500, 4500], 'l_eyelid': [4500, 7500], 'l_eye': [5500, 7500]}

def main():
    flip = 4
    dispW = 640
    dispH = 480
    face_file = 'haarcascade/frontalface_default.xml'
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'



    image = Image(camSet)
    window_name = 'Frame'
    image.set_window(window_name)
    video_capture, w, h = image.video_capure()
    W, H = image.factor((w, h))
    output = cv2.VideoWriter('Video.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 20, (W, H))
    face_cascade = image.cascade_clasifier(face_file)
    img_center = (W // 2, H // 2)
    pca = I2C()
    pca.set_pca9685()
    #1000 10000

    # pca.set_pca_channel(servos['l_cheak'], 6500)

    # dif =



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
            duty_cycle_neck = regression(face_center[0], 1500, 9500, W)
            duty_cycle_rcheak = regression(face_center[1], 2500, 8500, H)
            duty_cycle_lcheak = regression(face_center[1], 9500, 3500, H)
            duty_cycle_reye = regression(face_center[0], 6500, 4500, W)
            duty_cycle_leye = regression(face_center[0], 7500, 5500, W)
            pca.set_pca_channel(servos['neck'], duty_cycle_neck)
            pca.set_pca_channel(servos['r_cheak'], duty_cycle_rcheak)
            pca.set_pca_channel(servos['l_cheak'], duty_cycle_lcheak)
            pca.set_pca_channel(servos['r_eye'], duty_cycle_reye)
            pca.set_pca_channel(servos['l_eye'], duty_cycle_leye)




        output.write(frame)
        image.show_img(window_name, frame)

    image.release_feed(output)
    image.release_feed(video_capture)
    image.destroy_windows()


if __name__ == '__main__':
    main()
