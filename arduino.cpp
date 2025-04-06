#define Led1 12
#define Led2 11
#define Led3 10
#define Led4 6
#define Led5 7
#define playsound 3

void setup() {
  pinMode(Led1, OUTPUT);
  pinMode(Led2, OUTPUT);
  pinMode(Led3, OUTPUT);
  pinMode(Led4, OUTPUT);
  pinMode(Led5, OUTPUT);
}

void loop() {
  // adjust on and off delay time acc to use case
  digitalWrite(Led1, HIGH);
  digitalWrite(Led2, HIGH);
  digitalWrite(Led3, HIGH);
  digitalWrite(Led4, HIGH);
  digitalWrite(Led5, HIGH);
  delay(5000); 
  
  digitalWrite(Led1, LOW);
  digitalWrite(Led2, LOW);
  digitalWrite(Led3, LOW);
  digitalWrite(Led4, LOW);
  digitalWrite(Led5, LOW);
  delay(100); 

  digitalWrite(playsound, HIGH);
  delay(100);
  digitalWrite(playsound, LOW);
  delay(3000);
}
