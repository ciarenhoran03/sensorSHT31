Sistem Pemantauan Suhu dan Kelembapan Berbasis MQTT dengan Kontrol LED
Proyek ini menggunakan Raspberry Pi untuk membaca data dari sensor SHT31 dan mengontrol kecerahan LED melalui MQTT. Data suhu dan kelembapan dikirim ke broker MQTT, dan LED dikendalikan melalui perintah MQTT.

Komponen
Raspberry Pi
Sensor SHT31 (I2C)
LED (GPIO 18)
Broker MQTT (misalnya Mosquitto)
Instalasi
Install dependensi:

Copy code
sudo apt-get install python3-smbus python3-rpi.gpio
pip install paho-mqtt
Atur Broker MQTT: Jika belum, pasang dan jalankan broker MQTT (misalnya Mosquitto):

Copy code
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
Koneksi Hardware:

Hubungkan Sensor SHT31 ke pin I2C.
Hubungkan LED ke GPIO 18 dengan resistor.
Cara Menggunakan
Jalankan program:

Copy code
python3 mqtt_suhu_led.py
Kontrol LED: Kirim perintah ke topik control/led:

ON1, ON2, ON3 untuk mengatur kecerahan LED.
OFF untuk mematikan LED.
Pemantauan Suhu dan Kelembapan: Data diterbitkan setiap 2 detik ke topik:

sensors/sht31/suhu
sensors/sht31/kelembapan
Contoh Penggunaan
Mengontrol LED:

Copy code
mosquitto_pub -h localhost -t control/led -m "ON1"
Menerima data suhu:

Copy code
mosquitto_sub -h localhost -t sensors/sht31/suhu
