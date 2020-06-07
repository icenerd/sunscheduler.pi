# python.irrigation

An irrigation system intended for the following configuration:
- Raspberry Pi Zero W
- SainSmart Relay Module or similar.


## Installation
- Create your own manifest file in the 'config' folder. This file contains the details about where you are in the world for Sun calculations and a schedule for daily LED behavior.
- Edit 'ENVIRONMENT.py' to suit your needs.


## Suggested cron job entries
- 'calculate_schedule_for_today.py' after midnight every day.
- 'calculate_schedule_for_today.py' when the system boots, in case it's been offline.
- 'gpiozero_process.py' when the system boots.


### Links

- [Astral](https://astral.readthedocs.io/en/latest/index.html)
- [Gpiozero](https://gpiozero.readthedocs.io/en/stable/)