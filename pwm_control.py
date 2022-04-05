import Jetson.GPIO as GPIO
import time


class PWM:
    def __init__(self, pin=32, hz=100, min_duty_cycle=5, max_duty_cycle=25):
        # servo that I used the  duty cycle ranges is [5, 25]
        # for ESC the range of duty cycle is [1, 10]
        self.pin = pin
        self.hz = hz
        self.pwm = None
        self.min_duty_cycle = min_duty_cycle
        self.max_duty_cycle = max_duty_cycle

    def start(self, duty_cycle=0, sleep=0.05):
        GPIO.setwarnings(False)
        # Set Jetson to use pin number when referencing GPIO pins.
        # Can use GPIO.setmode(GPIO.BCM) instead to use Broadcom SOC channel names.
        GPIO.setmode(GPIO.BOARD)
        # Set GPIO pin 12 to output mode.
        GPIO.setup(self.pin, GPIO.OUT)
        # Initialize PWM on pwmPin 100Hz frequency
        self.pwm = GPIO.PWM(self.pin, self.hz)
        self.pwm.start(duty_cycle)
        time.sleep(sleep)

    def pixelsToDutyCycle(self, offset, max):
        difference = self.max_duty_cycle - self.min_duty_cycle
        liberty = 100
        if offset > max:
            offset = max
        elif offset < -1 * max:
            offset = -1 * max
        m = difference / liberty
        duty_cycle = offset * m + self.min_duty_cycle
        return duty_cycle

    def percentageToDutyCycle(self, percentage: float) -> float:
        difference = self.max_duty_cycle - self.min_duty_cycle
        # wheel max angle
        liberty_percentage = 100.
        # slope
        m = difference / liberty_percentage
        # upper and lower bound
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        # duty cycle
        duty_cycle = (percentage * m) + self.min_duty_cycle
        return duty_cycle

    def setDutyCycle(self, value):
        self.pwm.ChangeDutyCycle(value)

    def percentage(self, percentage, sleep=0.5):
        # duty cycle conversion
        duty_cycle = self.percentageToDutyCycle(percentage)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(sleep)

    def cleanPWM(self):
        # stop PWM
        self.pwm.stop()
        # resets GPIO ports used back to input mode
        GPIO.cleanup()
