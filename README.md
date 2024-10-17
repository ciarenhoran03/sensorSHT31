Sistem Pemantauan Suhu dan Kelembapan Berbasis MQTT dengan Kontrol LED.

Proyek ini menggunakan Raspberry Pi untuk membaca data dari sensor SHT31 dan mengontrol kecerahan LED melalui MQTT. 
` mermaid
sequenceDiagram
    participant Client as MQTT Client
    participant Broker as MQTT Broker (Raspberry Pi)
    participant Sensor as SHT31 Sensor
    participant LED as LED (GPIO 18)
    
    Client->>Broker: Subscribe to control/led
    Sensor->>Broker: Publish suhu to sensors/sht31/suhu
    Sensor->>Broker: Publish kelembapan to sensors/sht31/kelembapan
    Broker->>Client: Data suhu dan kelembapan
    Client->>Broker: Publish ON1/ON2/ON3/OFF to control/led
    Broker->>LED: Control brightness based on message
    LED->>Client: Feedback (optional)
    Sensor->>Broker: Publish updated data every 2 seconds

 `
