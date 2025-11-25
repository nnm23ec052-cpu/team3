import network
import urequests
from machine import Pin, ADC, I2C
import time
import dht
from ch1116 import CH1116_I2C

# --------------------------
# CONFIG
# --------------------------
WIFI_SSID = "WIFI_Id"
WIFI_PASS = "WIFI_Password"

THINGSPEAK_KEY = "Thingspeak_API_key"

TELEGRAM_TOKEN = "Telegram_Token"
CHAT_ID = "Telegram_Chat_Id"

TEMP_LIMIT = 30
SOIL_LIMIT = 64500

# --------------------------
# PINS
# --------------------------
DHT_PIN = 15
SOIL_PIN = 26
PUMP_PIN = 13
FAN_PIN  = 14

# --------------------------
# SENSOR SETUP
# --------------------------
sensor = dht.DHT22(Pin(DHT_PIN))
soil = ADC(Pin(SOIL_PIN))

pump = Pin(PUMP_PIN, Pin.OUT)
fan  = Pin(FAN_PIN, Pin.OUT)

pump.value(0)
fan.value(0)

# --------------------------
# OLED SETUP
# --------------------------
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = CH1116_I2C(128, 32, i2c, addr=0x3C)

oled.fill(0)
oled.text("Smart Farm IoT", 0, 0)
oled.text("Connecting WiFi...", 0, 12)
oled.show()

# --------------------------
# WIFI CONNECT
# --------------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print("Connecting...")
        time.sleep(0.5)
    print("WiFi Connected")

connect_wifi()

# --------------------------
# SIMPLE TELEGRAM SEND
# --------------------------
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        urequests.post(url, json={"chat_id": CHAT_ID, "text": msg}).close()
    except:
        print("Telegram error")


# --------------------------
# THINGSPEAK
# --------------------------
def send_ts(temp, hum, soil_val, pump_on, fan_on):
    try:
        url = (f"http://api.thingspeak.com/update?api_key={THINGSPEAK_KEY}"
               f"&field1={temp}&field2={hum}&field3={soil_val}"
               f"&field4={pump_on}&field5={fan_on}")
        urequests.get(url).close()
    except:
        print("TS error")


# --------------------------
# MAIN LOOP
# --------------------------
print("System Started")

while True:
    try:
        # Read sensors
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        soil_val = soil.read_u16()

        # Auto control logic
        pump_on = soil_val < SOIL_LIMIT
        fan_on = temp > TEMP_LIMIT

        pump.value(1 if pump_on else 0)
        fan.value(1 if fan_on else 0)

        # OLED update
        oled.fill(0)
        oled.text(f"T:{temp}C H:{int(hum)}%", 0, 0)
        oled.text(f"Soil:{soil_val}", 0, 10)
        oled.text(f"Pump:{'ON' if pump_on else 'OFF'}", 0, 20)
        oled.text(f"Fan:{'ON' if fan_on else 'OFF'}", 70, 20)
        oled.show()

        # Thingspeak upload
        send_ts(temp, hum, soil_val, int(pump_on), int(fan_on))

        # Print on shell
        print(f"Temp={temp}C Hum={hum}% Soil={soil_val} Pump={pump_on} Fan={fan_on}")

        # --------------------------
        #  TELEGRAM UPDATE
        # --------------------------
        message = (
            f"Smart Farm Update\n"
            f"Temp: {temp}°C\n"
            f"Hum: {hum}%\n"
            f"Soil: {soil_val}\n"
            f"Pump: {'ON' if pump_on else 'OFF'}\n"
            f"Fan: {'ON' if fan_on else 'OFF'}"
        )
        send_telegram(message)

    except Exception as e:
        print("ERR:", e)

    time.sleep(20)   # send every 20 sec, change if needed
