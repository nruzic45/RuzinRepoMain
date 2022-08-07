import cv2
import mediapipe as mp
import detekcijaRuke

def strim(brojSlika:int, zapis: bool):
    video = cv2.VideoCapture(0)
    count = 0

    mpRuke = mp.solutions.hands
    ruke = mpRuke.Hands()
    tacke = mp.solutions.drawing_utils

    while(True and (count < brojSlika)):

        ret, frame = video.read()
        detektovano = detekcijaRuke.nadjiRuku(frame, ruke)

        if detektovano.multi_hand_landmarks:
            for detektovanaRuka in detektovano.multi_hand_landmarks:
                tacke.draw_landmarks(frame, detektovanaRuka, mpRuke.HAND_CONNECTIONS)

        cv2.imshow('BlockDetect - press q to stop' , frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if zapis:
            cv2.imwrite("frame%d.jpg" % count, frame)
            count = count + 1


    video.release()
    cv2.destroyAllWindows()
