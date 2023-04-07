# First we do the imports
from msilib.schema import Billboard
from fhict_cb_01.CustomPymata4 import CustomPymata4
import time, sys, requests

# Then we define the pins
POTPIN = 0
BUTTON1PIN = 9
LED_PINS = [5, 7]
Buzzer = 3

# We make a variable that changes when the button is pressed and one that is the timer
prevLevel = 1
timer = 0
level1 = 0
rotate = 0

# The JSONs must go to these specific pages
url1 = "http://127.0.0.1:5000/prep.html"
url2 = "http://127.0.0.1:5000/oven.html"
url3 = "http://127.0.0.1:5000/ready.html"


def setup():
    # Then comes the setup function where we setup all the necessary pinmodes and such and so
    global board
    board = CustomPymata4(com_port="COM3")
    board.displayOn()
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.set_pin_mode_analog_input(POTPIN)
    board.set_pin_mode_digital_output(Buzzer)
    for pin in LED_PINS:
        board.set_pin_mode_digital_output(pin)


def loopdeloop():
    # And then the loop
    global level1, rotate, prevLevel
    # We have to make it sleep 1 second at first because otherwise the first button read is immediately 0
    # It also makes it easier to read how much time is being set
    time.sleep(1)
    rotate, timestamp = board.analog_read(POTPIN)
    level1, time_stamp1 = board.digital_read(BUTTON1PIN)
    board.digital_pin_write(7, 0)  # Yellow
    board.digital_pin_write(5, 0)  # Green
    print(rotate)
    board.displayShow(rotate)
    board.digital_pin_write(Buzzer, 0)

    if level1 == 0:
        prevLevel = 0

    # If the button press is registered then it starts this sequence the rotate value of the pot pin is the timer in this case
    if prevLevel == 0:

        timer = rotate
        # While the timer isn't 0 it sends a json to app.py that the pizza is in the oven and that makes app.py redirect from the prep page to the oven page
        while timer != 0:
            prepi = 1
            prepeth = {"glomp": prepi}
            log = requests.post(url1, json=prepeth)
            if log.status_code != 200:
                print(log.text)
            board.digital_pin_write(7, 1)  # Yellow
            board.displayShow(timer)
            timer -= 1
            time.sleep(1)

        # When time is up it makes the green LED glow and a soft tone starts playing for 20 seconds to signify that the pizza is ready
        # The JSON here makes app.py send from oven.html to ready.html
        timeth = 20
        while timeth != 0:
            board.digital_pin_write(7, 0)
            board.digital_pin_write(5, 1)
            board.digital_pin_write(Buzzer, 1)
            time.sleep(0.001)  # Add a delay for the buzzer to make the tone audible
            board.digital_pin_write(Buzzer, 0)
            time.sleep(0.001) # Add a delay for the buzzer to make the tone audible
            doney = "T"
            doneth = {"sjwomp": doney}
            log = requests.post(url2, json=doneth)
            if log.status_code != 200:
                print(log.text)
            timeth -= 1
            time.sleep(1)
            # After the 20 seconds, it sends a JSON that makes app.py redirect to the leave a review page; this should somewhat represent the time taken to eat the food, however, if this were made a realistic time, then it wouldn't be fun to test
        reviewi = 1
        revieweth = {"blonk": reviewi}
        log = requests.post(url3, json=revieweth)
        if log.status_code != 200:
            print(log.text)

        time.sleep(5)

        prevLevel = 1

#This is the function that makes everything run
setup()

while True:
    try:
        loopdeloop()
    except KeyboardInterrupt: # crtl+C
        print('shutdown')
        board.shutdown()
        sys.exit(0)
