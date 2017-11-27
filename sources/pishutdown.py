#!/usr/bin/python
# shutdown/reboot(/power on) Raspberry Pi com botao desligar/reiniciar

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time

# O botao deve ser conectado ao pino 5
shutdownPin = 5

# Se o botao for pressionado por mais de 3 segundos, o raspberry sera desligado
# Caso contrario, reiniciara
shutdownMinSeconds = 3

# Debounce para evitar micro falhas
debounceSeconds = 0.01

GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None


def buttonStateChanged(pin):
    global buttonPressedTime

    if not (GPIO.input(pin)):
        # Botao pressionado
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
    else:
        # Botao aberto
        if buttonPressedTime is not None:
            elapsed = (datetime.now() - buttonPressedTime).total_seconds()
            buttonPressedTime = None
            if elapsed >= shutdownMinSeconds:
                # Botao foi pressionado por tempo maior que o minimo, desligar.
		start = time.time()
		while (time.time() < start + 5):
			print '.'
		call(['shutdown', '-h', 'now'], shell=False)
            elif elapsed >= debounceSeconds:
                # Botao foi pressionado por tempo curto, reiniciar.
		start = time.time()
		while (time.time() < start + 5):
			print '.'
		call(['shutdown', '-r', 'now'], shell=False)


# Associar o evento de mudanca de estado do botao a rotina acima
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

while True:
    # Diminuir o tempo de uso do CPU
    time.sleep(5)
