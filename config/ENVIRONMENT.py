DATABASE_FILE = "bin/xōchipilli.sqlite.db"
MANIFEST_FILE = "config/manifest_all_day.json"

''' Set to False when deployed on an actual device with available pins. '''
SHOULD_MOCK_GPIOZERO = True

''' How often to execute control loop. '''
SLEEP_CYCLE_S = 10

''' DECLARE GPIO '''
SOLENOID_00 = "GPIO20"
SOLENOID_01 = "GPIO21"
SOLENOID_02 = "GPIO22"
SOLENOID_03 = "GPIO23"
GPIO_REGISTRY = [SOLENOID_00, SOLENOID_01, SOLENOID_02, SOLENOID_03]

''' DANGER: Maybe don't change these. '''
FTIME = "%Y-%m-%d %H:%M"
DAWN = "dawn"
SUNRISE = "sunrise"
NOON = "noon"
SUNSET = "sunset"
DUSK = "dusk"
ASTRAL = [DAWN,SUNRISE, NOON,SUNSET,DUSK]
