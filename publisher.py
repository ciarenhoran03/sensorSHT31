import time
import smbus
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

LED_PIN = 18  
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Inisialisasi PWM pada LED_PIN dengan frekuensi 1000 Hz
pwm_led = GPIO.PWM(LED_PIN, 1000)
pwm_led.start(0)  # Mulai dengan PWM di 0 (LED mati)

MQTT_BROKER = "localhost"
MQTT_PORT = 1884
MQTT_TOPIC_SUHU = "sensors/sht31/suhu"
MQTT_TOPIC_KELEMBAPAN = "sensors/sht31/kelembapan"
MQTT_TOPIC_LED = "control/led"

SHT31_ADDRESS = 0x44
MEASURE_COMMAND = [0x24, 0x00]

def read_sht31():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(SHT31_ADDRESS, MEASURE_COMMAND[0], [MEASURE_COMMAND[1]])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(SHT31_ADDRESS, 0x00, 6)
    temperature = ((data[0] * 256) + data[1]) * 175.0 / 65535.0 - 45.0
    humidity = ((data[3] * 256) + data[4]) * 100.0 / 65535.0
    return temperature, humidity

def on_connect(client, userdata, flags, rc):
    print("Terhubung ke broker MQTT dengan hasil kode: " + str(rc))
    client.subscribe(MQTT_TOPIC_LED)  # Langganan ke topik LED

def on_message(client, userdata, msg):
    led_command = msg.payload.decode()
    print(f"Perintah LED diterima: {led_command}")
    
    if led_command == "ON1":
        pwm_led.ChangeDutyCycle(85)  
        print("LED dinyalakan ke tingkat kecerahan 1 (ON1)")
    elif led_command == "ON2":
        pwm_led.ChangeDutyCycle(170)  
        print("LED dinyalakan ke tingkat kecerahan 2 (ON2)")
    elif led_command == "ON3":
        pwm_led.ChangeDutyCycle(225)  
        print("LED dinyalakan ke tingkat kecerahan 3 (ON3)")
    elif led_command == "OFF":
        pwm_led.ChangeDutyCycle(0)
        print("LED dimatikan (OFF)")
    else:
        print("Perintah tidak dikenali.")

if __name__ == "__main__":
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()  # Mulai loop MQTT

        while True:
            temp, hum = read_sht31()
            
            # Output sesuai yang diinginkan
            print(f"Suhu {temp:.2f} C Kelembapan {hum:.2f} %")

            # Payload tetap untuk pengiriman via MQTT
            payload_suhu = f"Suhu {temp:.2f} C"
            mqtt_client.publish(MQTT_TOPIC_SUHU, payload_suhu)

            payload_kelembapan = f"Kelembapan {hum:.2f} %"
            mqtt_client.publish(MQTT_TOPIC_KELEMBAPAN, payload_kelembapan)

            time.sleep(2)  # Tunggu 2 detik sebelum membaca ulang

    except KeyboardInterrupt:
        print("Program dihentikan.")
    finally:
        pwm_led.stop()  # Hentikan PWM
        GPIO.cleanup()  # Bersihkan GPIO
        mqtt_client.loop_stop()  # Hentikan loop MQTT
        mqtt_client.disconnect()  # Putuskan koneksi dari broker
