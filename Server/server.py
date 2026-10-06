import socket
import random
import time
import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))
clients = set()

print("Waiting for clients")

while True:
	sock.settimeout(0.03)
	try:
		data, addr = sock.recvfrom(1024)
		if addr not in clients:
			print(f"New client: {addr}")
			clients.add(addr)
	except socket.timeout:
		pass

	time.sleep(0.005)
	euler = sensor.euler
	accel=sensor.acceleration
	sensorData = f"h:{euler[0]}\nr:{euler[1]}\np:{euler[2]}\nax:{accel[0]}\nay:{accel[1]}\naz:{accel[2]}"
	for client in clients:
		try:
			sock.sendto(sensorData.encode(), client)
		except TimeoutError:
			print("Error: client timed out")
			clients.remove(client)
