#!/usr/bin/python
# Teste de serviços no Raspberry Pi para controlar led indicador de estado

import subprocess
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

while True:
	p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
	out, err = p.communicate()
	if ('freeradius' in out):
		print('freeradius running')
		if('hostapd' in out):
			print('hostapd running')
			GPIO.output(7, True)
		else:
			GPIO.output(7, False)
	else:
		GPIO.output(7, False)
	
	time.sleep(5);
