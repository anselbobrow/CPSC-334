int r1 = 12;
int r2 = 14;
int r3 = 27;
int r4 = 26;

void setup() {
  analogReadResolution(12);
  Serial.begin(115200);
}

void loop() {
  int r1val = analogRead(r1);
  int r2val = analogRead(r2);
  int r3val = analogRead(r3);
  int r4val = analogRead(r4);
  Serial.printf("[%d,%d,%d,%d]\n", r1val, r2val, r3val, r4val);
  delay(200);
}
