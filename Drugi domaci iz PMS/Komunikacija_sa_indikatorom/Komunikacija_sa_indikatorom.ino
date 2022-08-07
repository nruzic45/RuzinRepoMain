#include <TM1637Display.h>
#include <TimerOne.h>

const int CLK = 9;
const int DIO = 8;

// Naponi izmereni za 3 ose u akcelerometru:
volatile int x = 0;
volatile int y = 0;
volatile int z = 0;

// Stanja:
// 0 - ceka se komanda; 11 - 1. korak kalibracije x ose; 12 - 2. korak kalibracije x ose;
// 21 - 1. korak kalibracije y ose; 22 - 2. korak kalibracije y ose;
// 31 - 1. korak kalibracije z ose; 31 - 2. korak kalibracije z ose; 4 - glavni deo
volatile byte stanje = 0;
const int VCCPin = A0;
const int xPin = A1;
const int yPin = A2;
const int zPin = A3;
const int GNDPin = A4;

int touchPin = 2;
// a je pomocna promenljiva za slanje podataka na serijski port
int a = 0;
volatile byte state = LOW;
String inputString = "";
// ledValue je broj koji oznacava osvetljenost diode (izmedju 0 i 255)
float ledValue = 0;
// decimal je pomocna promenljiva za skladistanje dela ledValue koji se nalazi iza decimalne tacke
float decimal = 0;

int ledPin = 11;
// pointIndicator oznacava da li smo dosli do decimalne tacke prilikom citanja podataka sa serijskog porta
int pointIndicator = 0;
int i = 1;

int NumStep = 0;

TM1637Display display(CLK, DIO);

void setup() {
  Serial.begin(9600);
  Timer1.initialize(100000);
  Timer1.attachInterrupt(timerIsr);

  pinMode(VCCPin, OUTPUT);
  pinMode(GNDPin, OUTPUT);
  digitalWrite(VCCPin, HIGH);
  digitalWrite(GNDPin, LOW);
  
  display.setBrightness(7);
  
  pinMode(touchPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(touchPin), kalibracija, RISING);
}

// U loop delu koda salju se podaci na serijski port. U zavisnosti od stanja, zavisi koji napon ce se slati
void loop() {
    String a;
    if (stanje == 1) {
      stanje = 0;
      a = String(x)+String(y)+String(z);
      Serial.println(a);
    }
    
    delay(100);
}

// Kada se nesto pojavi na serijskom portu, Arduino to cita znak po znak. To moze da bude pozitivan ili negativan broj ili slovo koje oznacava
// u koje stanje ce Arduino da predje
void serialEvent() {
  ledValue = 0;
  decimal = 0;
  i = 1;
  pointIndicator = 0;
  analogWrite(3, 0); // Iskljucujemo diode dok se citaju podaci sa Serial porta
  analogWrite(11, 0);
  while (Serial.available()) {

    
    int digit = Serial.read();
    if (digit == 'x') {
      stanje = 1;
      break;
    }
    
    else {
      if (digit == '-') {
        ledPin = 3;
      }
      else if (digit != '\n') {
        if(digit == '.') {
          pointIndicator = 1;
        }
        else {
          digit = digit - 48;
          if (pointIndicator == 0) {
            ledValue = ledValue*10 + digit;
          }
          else {
            decimal = decimal + digit/(pow(10,i));
            i++;
          }
        }
      }
      // Kada dodjemo do kraja broja poslatog sa na serijski port, tu vrednost koristimo
      // da ukljucimo jednu od dve diode sa odredjenim intenzitetom
      else {
        ledValue = (ledValue + decimal)*255/3.14;
        analogWrite(ledPin, ledValue);
        ledPin = 11;
      }
    }
    
  }
}


// Kalibracija je zapravo prekid povezan sa kapacitivnim senzorom. U trenutku kada
// je pritisnut, ako je Arudino u odgovarajucem stanju, na serijski port bice poslat
// odgovarajuci napon sa pratecom jedinicom, koja ce u Python-u oznacavati da je dati
// broj jedna od vrednosti potrebnih za kalibraciju
void kalibracija() {
  String a;
  a = String(x)+String(y)+String(z)+'1';
  Serial.println(a);
}

// Vrednosti sa akcelerometra se ocitavaju na svaki otkucaj tajmera
void timerIsr() {
  x = analogRead(xPin);
  y = analogRead(yPin);
  z = analogRead(zPin);
}
