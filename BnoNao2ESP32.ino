#include <Wire.h>
#include <Adafruit_BNO08x.h>
#include <Adafruit_NAU7802.h> 

// Create the BNO08x instance
Adafruit_BNO08x bno;
sh2_SensorValue_t sensorValue;

// Create the NAU7802 instance
Adafruit_NAU7802 nau; 

// Global variables for NAU7802 readings and timing
unsigned long nau_last_read_time = 0; // Timer for NAU7802
// Read NAU7802 every 20ms (50Hz)
unsigned long nau_read_interval = 20; 
long current_load = 0; // The raw digital reading from the NAU7802
float current_load_grams = 0.0; // The calculated load value (e.g., in grams or normalized)


// Function to convert quaternion to Euler angles
void quaternionToEuler(sh2_SensorValue_t* sensorValue, float* yaw, float* pitch, float* roll) {
  float q_x = sensorValue->un.arvrStabilizedRV.i;
  float q_y = sensorValue->un.arvrStabilizedRV.j;
  float q_z = sensorValue->un.arvrStabilizedRV.k;
  float q_w = sensorValue->un.arvrStabilizedRV.real;

  // Roll (Rotation around X-axis)
  float sinr_cosp = 2.0 * (q_w * q_x + q_y * q_z);
  float cosr_cosp = 1.0 - 2.0 * (q_x * q_x + q_y * q_y);
  *roll = atan2(sinr_cosp, cosr_cosp);

  // Pitch (Rotation around Y-axis)
  float sinp = 2.0 * (q_w * q_y - q_z * q_x);
  if (abs(sinp) >= 1)
    *pitch = copysign(M_PI / 2, sinp);
  else
    *pitch = asin(sinp);

  // Yaw (Rotation around Z-axis)
  float siny_cosp = 2.0 * (q_w * q_z + q_x * q_y);
  float cosy_cosp = 1.0 - 2.0 * (q_y * q_y + q_z * q_z);
  *yaw = atan2(siny_cosp, cosy_cosp);
}

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);
  Serial.println("BNO08x & NAU7802 High Rate Data Stream");

  // Initialize Wire1 on GPIO 41 and 40
  Wire1.begin(41, 40);
  // Increase the I2C clock speed to 400kHz
  Wire1.setClock(400000); 

  // --- BNO08x Initialization ---
  if (!bno.begin_I2C(0x4A, &Wire1)) { 
    Serial.println("Failed to find BNO08x chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("BNO08x Found!");

  // Enable the report at a higher frequency (10ms interval for 100Hz)
  bno.enableReport(SH2_ARVR_STABILIZED_RV, 10000); 

  // --- NAU7802 Initialization ---
  Serial.println("NAU7802 Initialization...");
  // Pass the pointer to the Wire1 object (&Wire1) to explicitly use the secondary I2C bus
  if (! nau.begin(&Wire1)) { 
    Serial.println("Failed to find NAU7802");
    while (1) delay(10); 
  }
  Serial.println("Found NAU7802");

  // Configure NAU7802 settings (LDO, Gain, Rate) 
  nau.setLDO(NAU7802_3V0);
  nau.setGain(NAU7802_GAIN_128);
  nau.setRate(NAU7802_RATE_80SPS);
  Serial.print("LDO, Gain, Rate set: 3.0V, 128x, 80SPS"); Serial.println();


  // Take 10 readings to flush out readings
  Serial.println("Flushing NAU7802 readings...");
  for (uint8_t i=0; i<10; i++) {
    while (! nau.available()) delay(1); // Wait for data 
    nau.read();
  }

  // Calibrate NAU7802
  Serial.println("Calibrating NAU7802...");
  while (! nau.calibrate(NAU7802_CALMOD_INTERNAL)) {
    Serial.println("Failed to calibrate internal offset, retrying!");
    delay(1000); 
  }
  Serial.println("Calibrated internal offset");
  while (! nau.calibrate(NAU7802_CALMOD_OFFSET)) {
    Serial.println("Failed to calibrate system offset, retrying!");
    delay(1000); 
  }
  Serial.println("Calibrated system offset. System Ready.");
}

void loop() {
  unsigned long current_time = millis(); 
  static unsigned long bno_lastEventMicros = 0;
  unsigned long currentMicros = micros();

  // ===================================
  // Task 2: Read NAU7802 Load Cell Data (Non-blocking timing)
  // Updates the global variable 'current_load_grams' periodically.
  // ===================================
  
  if (current_time - nau_last_read_time >= nau_read_interval) {
      nau_last_read_time = current_time; 
      
      if (nau.available()) {
          current_load = nau.read(); 
          // Conversion using your formula (800-current_load) / 27500.0
          current_load_grams = (float)(800-current_load) / 27500.0; 
      }
  }
  
  // ===================================
  // Task 1: Read BNO08x Roll Angle and Print Output
  // This triggers only when a new BNO event is available (approx. 100Hz).
  // ===================================
  if (bno.getSensorEvent(&sensorValue)) {
    if (sensorValue.sensorId == SH2_ARVR_STABILIZED_RV) {
      float yaw_angle, pitch_angle, roll_angle;
      
      quaternionToEuler(&sensorValue, &yaw_angle, &pitch_angle, &roll_angle);

      unsigned long timeSinceLastEvent = currentMicros - bno_lastEventMicros;
      bno_lastEventMicros = currentMicros;

      // Print only Roll and the last known Load value on a single line
      //Serial.print("X: ");
      // Roll in degrees (X-axis)
      
      //Serial.print(roll_angle * 180.0 / M_PI); 
      //Serial.print(" deg | Load: ");
      
      //Serial.print(",");
      // Print the Load value with 3 decimal places

      Serial.print(roll_angle * 180.0 / M_PI); 
      Serial.print(",");
      Serial.print(-current_load_grams, 3); 
      Serial.println(""); // Use println to ensure a new line
    }
  }
}