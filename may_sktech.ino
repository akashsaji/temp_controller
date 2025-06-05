#include <Wire.h> // For I2C communication
#include <Adafruit_ADS1X15.h> // For ADS1115 ADC
#include <U8glib.h> // For OLED display (keep if using U8glib)

U8GLIB_SH1106_128X64 oled(U8G_I2C_OPT_NONE); // OLED using SH1106 controller

#define out_pin 6 // Pin to drive MOSFET gate
#define rst_pin 7 // Pin to reset the circuit

const float V_th = 115.0; // Threshold voltage in mV (115 mV = 115 mA)
const float FSR = 6.144 / 32768.0; // Voltage per bit for ADS1115 at ±6.144V gain
int16_t adc0 = 0; // Holds raw ADC reading
float voltage = 0.0; // Holds converted voltage value

Adafruit_ADS1115 ads; // Create ADS1115 object

void setup() {
  Serial.begin(115200);
  pinMode(out_pin, OUTPUT);
  pinMode(rst_pin, INPUT_PULLUP);

  Serial.println("Initializing ADS1115...");
  ads.begin();
  ads.setGain(GAIN_TWOTHIRDS); // ±6.144V (default), use GAIN_ONE for ±4.096V if needed
}

void loop() {
  read_analog_value();

  if (voltage >= V_th) {
    // Stay in loop while overcurrent and reset not pressed
    while (digitalRead(rst_pin) != LOW) {
      digitalWrite(out_pin, LOW); // Turn off MOSFET
      read_analog_value();
      serial_display();
      delay(1000);
    }
  } else {
    digitalWrite(out_pin, HIGH); // Keep MOSFET ON
  }

  serial_display();
  delay(1000);
}

// Read analog value from ADS1115
void read_analog_value() {
  adc0 = ads.readADC_SingleEnded(0); // Read A0 pin
  voltage = adc0 * FSR * 1000.0; // Convert to millivolts (mV)
  oled_display(voltage);
}

// Print data to Serial Monitor
void serial_display() {
  Serial.print("ADC0: ");
  Serial.print(adc0);
  Serial.print("\tVoltage (mV): ");
  Serial.println(voltage, 4);
}

// Display data on OLED
void oled_display(float voltage) {
  oled.firstPage();
  do {
    oled.setFont(u8g_font_profont12);
    oled.setPrintPos(0, 15);
    oled.print("Voltage (mV):");
    oled.setPrintPos(0, 25);
    oled.print(voltage, 4);

    oled.setPrintPos(0, 45);
    oled.print("Current (mA):");
    oled.setPrintPos(0, 55);
    oled.print(voltage, 4); // Same as voltage in mV → Current in mA via 1 Ohm sense resistor
  } while (oled.nextPage());
}
