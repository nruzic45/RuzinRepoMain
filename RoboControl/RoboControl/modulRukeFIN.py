import cv2
import mediapipe as mp
import detekcijaRuke


class detektorRuke():
    def __init__(self, mod=False, brRuku=2):
        self.mode = False
        self.brRuku = brRuku
        # self.verovatDetekcije = verovatDetekcije #zajebava?? treba pogledati api funkcije
        # self.verovatPracenja = verovatPracenja

        self.mpRuke = mp.solutions.hands
        self.ruke = self.mpRuke.Hands(self.mode, self.brRuku)
        self.crtajTacke = mp.solutions.drawing_utils

    def detektuj(self, frame):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.detektovano = self.ruke.process(frameRGB)

    def crtaj(self, frame):
        if self.detektovano.multi_hand_landmarks:
            for detektovaneTacke in self.detektovano.multi_hand_landmarks:
                self.crtajTacke.draw_landmarks(frame, detektovaneTacke, self.mpRuke.HAND_CONNECTIONS)
        return frame

    def getPoz(self, frame, redBrRuke, zapis=False):

        pozicije = []
        if self.detektovano.multi_hand_landmarks:
            detektovaneTacke = self.detektovano.multi_hand_landmarks[redBrRuke]
            for id, tacka in enumerate(detektovaneTacke.landmark):
                visinaSlike, sirinaSlike, f = frame.shape
                fx = int(tacka.x * sirinaSlike)
                fy = int(tacka.y * visinaSlike)
                pozicije.append([id, fx, fy])

        if zapis:
            pozicijeSTR = ' '
            for pozicija in pozicije:
                pozicijeSTR += "|"
                for i in pozicija:
                    pozicijeSTR += (str(i) + 'g')
            pozicijeSTR += '\n'

            with open('readme.txt', 'a') as f:
                f.write(pozicijeSTR)

        return pozicije


# Bojlerplate code
def main():
    video = cv2.VideoCapture(0)

    dr = detektorRuke()
    while True:
        ret, frame = video.read()

        frame = dr.detekcijaRuke(frame)

        cv2.imshow('BlockDetect - press q to stop', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
