from gpiozero.pins.mock import MockFactory
from gpiozero import Device, LED

import config.ENVIRONMENT as Config
import sqlite3
import sys
from time import sleep

if Config.SHOULD_MOCK_GPIOZERO:
	Device.pin_factory = MockFactory()

GPIO_REGISTRY_LED = dict()
for gpioId in Config.GPIO_REGISTRY:
	GPIO_REGISTRY_LED[gpioId] = LED(gpioId)
	print(f'Observing schedule for {gpioId}')

SQL_GET_GPIO_OPEN_NOW = '''SELECT DISTINCT name FROM schedule_led WHERE DATETIME("now", "localtime") BETWEEN open_at AND close_at;'''

def getOpenGPIOIdNow(db):
	raOpenGPIOId = []
	try:
		cursor = db.cursor()
		cursor.execute(SQL_GET_GPIO_OPEN_NOW)
		records = cursor.fetchall()
		for row in records:
			raOpenGPIOId.append(row[0])
		cursor.close()
	except:
		print("Unexpected error", sys.exc_info()[0])
	finally:
		if cursor:
			cursor.close()
	return raOpenGPIOId

while True:
	try:
		db = sqlite3.connect(Config.DATABASE_FILE)
		raOpenGPIOId = getOpenGPIOIdNow(db)
		for gpioId, led in GPIO_REGISTRY_LED.items():
			shouldBeOpen = gpioId in raOpenGPIOId
			isOn = led.is_lit
			if shouldBeOpen and not isOn:
				led.on()
				print(f'{gpioId} is now OPEN')
			elif shouldBeOpen and isOn:
				print(f'{gpioId} is OPEN')
			else:
				led.off()
				if isOn:
					print(f'{gpioId} is now CLOSED')
				else:
					print(f'{gpioId} is CLOSED')
			
	except sqlite3.Error as error:
		print("sqlite3.Error", error)
	finally:
		if (db):
			db.close()

	sleep(Config.SLEEP_CYCLE_S)
	print("------")