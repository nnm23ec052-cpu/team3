# 🌱 IoT Smart Farm Greenhouse System with Raspberry Pi Pico

This project implements an **IoT Smart Farm Greenhouse System** using Raspberry Pi Pico.  
It monitors **temperature, humidity, and soil moisture** in real time, and automatically controls a **pump** and **fan** for optimal plant growth.  
Data is uploaded to **ThingSpeak** for analytics, and notifications are sent via **Telegram Bot**. An **OLED display** shows live sensor readings and actuator states.

---

## 📌 Problem Statement
Develop an IoT Smart Greenhouse System with Raspberry Pi Pico to monitor and control temperature, humidity, and soil moisture in real time.  
Focus on **optimal plant growth**, **minimal human intervention**, and **resource efficiency**.

---

## 🎯 Scope of the Solution
- Real-time monitoring of temperature, humidity, and soil moisture.
- Automatic control of **water pump** and **fan** based on threshold values.
- Data logging to **ThingSpeak IoT dashboard**.
- Instant alerts via **Telegram Bot**.
- Local OLED display for quick visualization.
- Minimal human intervention with efficient resource usage.

---

## 🛠️ Required Components

### Hardware
- Raspberry Pi Pico W (Wi-Fi enabled)
- DHT22 sensor (temperature & humidity)
- Capacitive soil moisture sensor
- Relay module (to control pump & fan)
- DC water pump
- DC fan
- OLED Display (CH1116, I2C, 128x32)
- Breadboard, jumper wires, resistors

### Software
- **IDE:** Thonny (MicroPython)
- **Firmware:** MicroPython UF2 for Raspberry Pi Pico W
- **Libraries:**  
  - `network` (Wi-Fi)  
  - `urequests` (HTTP requests)  
  - `dht` (DHT22 sensor)  
  - `machine` (GPIO, ADC, I2C)  
  - `ch1116` (OLED driver)

 ## Project Video

![Video Thumbnail](video-thumbnail.png)

[Click here to view/download the full video](video.mp4)


---


