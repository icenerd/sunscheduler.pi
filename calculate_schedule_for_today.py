""" from gpiozero import LED """
from datetime import date
from datetime import timedelta 
from astral import LocationInfo
from astral.sun import sun
import config.ENVIRONMENT as Config
import json
import sqlite3

SQL_CREATE_SCHEDULE_LED = '''CREATE TABLE IF NOT EXISTS schedule_led(name TEXT NOT NULL, open_at DATETIME NOT NULL, close_at DATETIME NOT NULL);'''
SQL_DELETE_ALL_SCHEDULE_LED = '''DELETE FROM schedule_led;'''
SQL_INSERT_SCHEDULE_LED = '''INSERT INTO schedule_led(name, open_at, close_at) VALUES("%s", "%s", "%s");'''

with open(Config.MANIFEST_FILE, 'r') as file:
	jsonConfig = json.load(file)
	locationInfo = LocationInfo()
	locationInfo.name = jsonConfig["name"]
	locationInfo.region = jsonConfig["region"]
	locationInfo.timezone = jsonConfig["timezone"]
	locationInfo.latitude = jsonConfig["latitude"]
	locationInfo.longitude = jsonConfig["longitude"]
	print((f'{jsonConfig["name"]}, {jsonConfig["region"]}, {jsonConfig["timezone"]}, {jsonConfig["latitude"]}, {jsonConfig["longitude"]}'))

	sunCalculations = sun(locationInfo.observer, date=date.today(), tzinfo=locationInfo.timezone)
	print((
		f'dawn: {sunCalculations[Config.DAWN].strftime(Config.FTIME)}\n'
		f'sunrise: {sunCalculations[Config.SUNRISE].strftime(Config.FTIME)}\n'
		f'noon: {sunCalculations[Config.NOON].strftime(Config.FTIME)}\n'
		f'sunset: {sunCalculations[Config.SUNSET].strftime(Config.FTIME)}\n'
		f'dusk: {sunCalculations[Config.DUSK].strftime(Config.FTIME)}'
	))

	try:
		db = sqlite3.connect(Config.DATABASE_FILE)
		db.execute(SQL_CREATE_SCHEDULE_LED)
		db.execute(SQL_DELETE_ALL_SCHEDULE_LED)
		for entry in jsonConfig["schedule_led"]:
			try:
				if entry["gpio_id"] not in Config.GPIO_REGISTRY:
					print((f'Warning: Unknown GPIO({entry["gpio_id"]}), entry ignored.'))
					print((f'{entry["gpio_id"]}: {entry["relative_to"]}, {entry["open_at"]}, {entry["duration"]}'))
				elif entry["duration"] <= 0:
					print((f'Warning: Duration must be positive integer minutes, entry ignored.'))
					print((f'{entry["gpio_id"]}: {entry["relative_to"]}, {entry["open_at"]}, {entry["duration"]}'))
				elif entry["relative_to"] not in Config.ASTRAL:
					print((f'Warning: Unknown relative anchor in time, entry ignored.'))
					print((f'{entry["gpio_id"]}: {entry["relative_to"]}, {entry["open_at"]}, {entry["duration"]}'))
				else:
					open_at = sunCalculations[entry["relative_to"]] + timedelta(minutes=entry["open_at"])
					close_at = sunCalculations[entry["relative_to"]] + timedelta(minutes=entry["open_at"]) + timedelta(minutes=entry["duration"])
					sql = SQL_INSERT_SCHEDULE_LED % (entry["gpio_id"], open_at.strftime(Config.FTIME), close_at.strftime(Config.FTIME))
					db.execute(sql)
					print((f'Executed {sql}'))
			except:
				print("Error with a schedule entry")
		db.commit()
	except sqlite3.Error as error:
		print("sqlite3.Error", error)
	finally:
		if db:
			db.close()