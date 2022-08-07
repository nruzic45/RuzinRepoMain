"""
Created on Sat Sep  4 08:35:44 2021

@author: Nikola
"""

import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from threading import Thread
import time
import serial
import math

global nx, kx, ny, ky, nz, kz, kraj #globalne promenljive za opis iymerenog ubrzanja
kx = 2
nx = 2
ky = 2
ny = 2
kz = 2
nz = 2
krajL = 0

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Proba'
        self.left = 200
        self.top = 200
        self.width = 730
        self.height = 520
        self.initUI()
    
    def initUI(self):
        
        global data, nx, kx, ny, ky, nz, kz
        global ax
        global ay 
        global az
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Taster za Kalibraciju
        self.dugmeKal = QPushButton('Kalibracija', self)
        self.dugmeKal.resize(100, 50)
        self.dugmeKal.move(10, 10)
        self.dugmeKal.clicked.connect(self.kal)
        
         # Taster za Letenje
        self.dugmeLet = QPushButton('Letenje', self)
        self.dugmeLet.resize(100, 50)
        self.dugmeLet.move(10, 60)
        self.dugmeLet.clicked.connect(self.let)
        
         # Taster za Izlaz
        self.dugmeIzl = QPushButton('Izlaz', self)
        self.dugmeIzl.resize(100, 50)
        self.dugmeIzl.move(10, 400)
        self.dugmeIzl.clicked.connect(self.izlaz)
        
        
        # Dodavanje polja za unos teksta
        self.text_input = QLineEdit('2', self)
        self.text_input.resize(100, 50)
        self.text_input.move(10,450)
        
        
        #Grafik
        self.grafik = PlotCanvas(self, width = 6, height = 5)
        self.grafik.move(120, 10)
        
        self.niz = []
        self.t = np.arange(0, 10, 0.1)
        
        t1.start()
    
        self.show()
       
    @pyqtSlot()
    
    def kal(self):
        
               #funkcija za pocetak kalibracije, stvara cetiri dugmica 
               #za kalibraciju tri razlicitih osa u prekid kalibracije
       
        self.dugmeKx = QPushButton('KalibracijaX', self)
        self.dugmeKx.resize(100, 50)
        self.dugmeKx.move(10, 200)
        self.dugmeKx.clicked.connect(self.kalx)
        self.dugmeKx.show()
        
        self.dugmeKy = QPushButton('KalibracijaY', self)
        self.dugmeKy.resize(100, 50)
        self.dugmeKy.move(10, 250)
        self.dugmeKy.clicked.connect(self.kaly)
        self.dugmeKy.show()
        
        self.dugmeKz = QPushButton('KalibracijaZ', self)
        self.dugmeKz.resize(100, 50)
        self.dugmeKz.move(10, 300)
        self.dugmeKz.clicked.connect(self.kalz)
        self.dugmeKz.show()
        
        self.dugmeKalEnd = QPushButton('Kraj Kalibracije', self)
        self.dugmeKalEnd.resize(100, 50)
        self.dugmeKalEnd.move(10, 350)
        self.dugmeKalEnd.clicked.connect(self.kraj)
        self.dugmeKalEnd.show()
        
      
    def izlaz(self):
        #metoda koja implementira zatvaranje aplikacije
        ser.close()
        ex.close()
        sys.exit()
        
        
        
    def kraj(self):
        self.dugmeKx.hide()
        self.dugmeKy.hide()
        self.dugmeKz.hide()
        self.dugmeKalEnd.hide()
        #funkcija koja upisuje izmerene parametre kalibracije i
        #sakriva dugmice 
        
        d = open('Parametri letelice', 'w')
        pom = self.text_input.text() + '\n' + 'kx = ' + str(kx) + ' nx = ' + str(nx) + '\n' + 'ky = ' + str(ky) + ' ny = ' + str(ny) + '\n' + 'kz = ' + str(kz) + ' nz = ' + str(nz) + '\n'
        d.write(pom)
        d.close()
        
    def krajLeta(self):
        
        #Funkcija koja oznacava kraj leta 
        global krajL
        krajL = 0
        poruka = 'a' + '\n' #a oznacava wait stanje
        ser.write(poruka.encode())
        
        self.dugmeKL.hide()
        self.dugmeKal.show()
        self.dugmeLet.show()
        
        
        
        
    def let(self):
        
        
        global krajL
        global ax
        global ay 
        global az
        krajL = 1
        poruka = 'k' + '\n' #Kraj kalibracije, pocetak leta, javljamo to Arduinu
        ser.write(poruka.encode())
        time.sleep(0.1)
        
        self.dugmeLet.hide()
        self.dugmeKal.hide()
        
        #stvaramo novo dugme za kraj leta
        
        self.dugmeKL = QPushButton('Kraj leta', self)
        self.dugmeKL.resize(100, 50)
        self.dugmeKL.move(10, 110)
        self.dugmeKL.clicked.connect(self.krajLeta)
        self.dugmeKL.show()
        
        
        
        i = 0
        
        #A = 2
        #self.grafik.plot(x = self.t, y = A*np.sin(self.t), naslov = 'sin(x)')
        while (krajL):#pokusaj prikazivanja rezultata grafikom
            i = i + 1
            print(ax)
            self.niz = np.arange(1, i, 1)
            self.grafik.clear()
            self.grafik.plot(x = niz, y = niz, naslov = 'Ubrzanje')
            
        ######
        
        
        #kalibracije su identicne za sve tri ose. Saljemo odgovarajuc karakter
        #serijskom komunikacijom Arduinu. Globalna promenljiva data
        #u sebi sadrzi informaciju o ubrzanju. 
        
        
    def kalx(self):
        
        global data, kx, nx
        poruka = 'x' + '\n'
        ser.write(poruka.encode())
        time.sleep(0.1)
        
        u1 = 0
        u2 = 0
        
        while(True):

            if data > 1000: #Kada god je pritisnut kapacitivni senzor dodaje
                            #se 1000 na izmereni napon.
                if u1 == 0:
                    u1 = data - 1000 
                    print(data)
                    data = 0
                else:
                    u2 = data - 1000
                    break
            else:
                print(data)
                time.sleep(0.1)

        
        
        kx = 2*9.81/(u1-u2)
        nx = 9.81 - u1*kx
        kx = round(kx, 2) #racunanje parametara kalibracije
        nx = round(nx, 2)
        print(kx)
        print(nx)
        
        
    def kaly(self):
        
        global data, ky, ny
        poruka = 'y' + '\n'
        ser.write(poruka.encode())
        time.sleep(0.1)
        
        u1 = 0
        u2 = 0
        
        while(True):

            if data > 1000:
                if u1 == 0:
                    u1 = data - 1000
                    print(data)
                    data = 0
                else:
                    u2 = data - 1000
                    break
            else:
                print(data)
                time.sleep(0.1)

        
        
        ky = 2*9.81/(u1-u2)
        ny = 9.81 - u1*ky
        ky = round(ky, 2)
        ny = round(ny, 2)
        print(ky)
        print(ny)
        
    
    def kalz(self):
        
        global data, kz, nz
        poruka = 'z' + '\n'
        ser.write(poruka.encode())
        time.sleep(0.1)
        
        u1 = 0
        u2 = 0
        
        while(True):

            if data > 1000:
                if u1 == 0:
                    u1 = data - 1000
                    print(data)
                    data = 0
                else:
                    u2 = data - 1000
                    break
            else:
                print(data)
                time.sleep(0.1)

        
        
        kz = 2*9.81/(u1-u2)
        nz = 9.81 - u1*kz
        kz = round(kz, 2)
        nz = round(nz, 2)
        print(kz)
        print(nz)
        
   
class PlotCanvas(FigureCanvas): #Klasa koja implementira figuru u gui.

    def __init__(self, parent = None, width = 2, height = 2, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
#        self.plot()


    def plot(self, x, y, naslov = ' ', tip = 'k-'):
        self.axes.cla()
        self.axes.grid()
        self.axes.plot(x, y, tip)
        self.axes.set_title(naslov)
        self.draw()
    
com_port = 'COM7'
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate) #deklaracija serijske komunikacije



def fun1(): #funkcija koju izvrsavamo u niti pored niti koja se izvrsava za GUI
    
    global data
    print('Pocetak fun1')
    global ax
    global ay 
    global az
    az = []
    ax = []
    ay = []
    while(True):
        data = ser.readline()
        data = float(data.decode())
        time.sleep(0.1)
        #citamo podatke iz serijske komunikacije sa Arduinom
        if krajL == 1:

            #racunamo date napone, s obzirom da su formatirani kao devetocifreni broj
            pom = str(data)
            ux = int(pom[0])*100+int(pom[1])*10+int(pom[2])
            uy = int(pom[3])*100+int(pom[4])*10+int(pom[5])
            uz = int(pom[6])*100+int(pom[7])*10+int(pom[8])
            
            #koriscenjem kalibracionig parametara racunamo ubrzanja
            axp = kx*ux + nx
            ayp = ky*uy + ny
            azp = kz*uz + nz
            
            
            ax.append(axp)
            ay.append(ayp)
            az.append(azp)
            

            #Racunanje uglova propinjanja i skretanja
            psi = round(math.atan(axp/math.sqrt(ayp*ayp+azp*azp)), 2)
            teta = round(-1 * math.atan(ayp/math.sqrt(axp*axp+azp*azp)), 2)
            
            #plt.figure()
            #t1 = np.linspace(0, 11, 2000)
            #plt.plot(t1, np.sin(t1))

            s = str(teta) #slanje podataka o uglu propinjanja Arduinu.
            ser.write(s.encode())
        else:
            ax = []
            ay = []
            az = []
            
        
    
def fun2():#Funkcija niti za GUI
        
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
    

t1 = Thread(target=fun1)
t2 = Thread(target=fun2)


t2.start()