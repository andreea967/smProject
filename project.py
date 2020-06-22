import time
import pigpio
import RPi.GPIO as GPIO
import array

a3 = 220
e5 = 659
d5 = 587
a4 = 440
f3 = 175
f5 = 698
d3 = 147
g3 = 196
c5 = 523
b4 = 494
g4 = 392
e3 = 165
a5 = 880
e4 = 330

dl1 = 0.7
dl2 = 0.2
dl3 = 0.3
dl4 = 0.1
dl5 = 0.4

sequence_1_notes = array.array('i', [a4, c5, a4, a4, d5, a4, g4, a4, e5, a4, a4, f5, e5, c5, a4, e5, a5, a4, g4, g4, e4, b4, a4])
sequence_1_delays = array.array('f', [dl2, dl2, dl2, dl3, dl3, dl3, dl2, dl2, dl2, dl2, dl3, dl3, dl2, dl2, dl2, dl2, dl3, dl3, dl2, dl3, dl3, dl4, dl5])

pi = pigpio.pi()

buzzer = 12

pi.set_mode(buzzer, pigpio.OUTPUT)
GPIO.setmode(GPIO.BOARD)

trig = 18
echo = 16
redled = 11
greenled = 13
blueled = 15

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.setup(redled, GPIO.OUT)
GPIO.setup(greenled, GPIO.OUT)
GPIO.setup(blueled, GPIO.OUT)

def song():
        for i in range(0,23):
                pi.hardware_PWM(buzzer, sequence_1_notes[i], 50000)
                time.sleep(sequence_1_delays[i])
                pi.hardware_PWM(buzzer, 0, 0)
                time.sleep(dl4)

                GPIO.output(greenled, GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(greenled, GPIO.LOW)
                time.sleep(0.01)

def calculate_distance():
        GPIO.output(trig, GPIO.HIGH)

        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)

        start = time.time()
        stop = time.time()

        while GPIO.input(echo) == 0:
                start = time.time()

        while GPIO.input(echo) == 1:
                stop = time.time()

        duration = stop - start

        distance = 34300/2 * duration
        if distance < 0.5 and distance > 400:
                return 0
        else:
                return distance

try:

        while True:
                if calculate_distance() < 25:
                        pi.hardware_PWM(buzzer, 500, 500000)
                        time.sleep(0.05)

                        pi.hardware_PWM(buzzer, 0, 0)
                        time.sleep(0.035)

                        GPIO.output(redled, GPIO.HIGH)
                        time.sleep(0.035)

                        GPIO.output(redled, GPIO.LOW)
                        time.sleep(0.025)
                elif calculate_distance() > 25 and calculate_distance() < 75:
                        pi.hardware_PWM(buzzer, 300, 400000)
                        time.sleep(0.05)

                        GPIO.output(blueled, GPIO.HIGH)
                        time.sleep(0.3)

                        GPIO.output(blueled, GPIO.LOW)
                        time.sleep(0.2)

                        pi.hardware_PWM(buzzer, 0, 0)
                        time.sleep(0.03)

                elif calculate_distance() > 75:
                        GPIO.output(greenled, GPIO.HIGH)
                        time.sleep(0.5)

                        GPIO.output(greenled, GPIO.LOW)
                        time.sleep(0.2)
                        song()
except KeyboardInterrupt:
        pass

pi.write(buzzer, 0)
pi.stop()

GPIO.cleanup()

