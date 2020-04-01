from centerVideo import *
from serial import *
from time import *

if __name__ == "__main__":
    while True:
        x, y = get_target_position(True, True, 56)
        pwm_orders = {}
        if x < 640 / 2 and y < 480 / 2:
            pwm_orders[1] = "300"
            pwm_orders[2] = "300"
            pwm_orders[3] = "000"
            pwm_orders[4] = "000"
        elif x > 640 / 2 and y < 480 / 2:
            pwm_orders[1] = "000"
            pwm_orders[2] = "300"
            pwm_orders[3] = "300"
            pwm_orders[4] = "000"
        elif x < 640 / 2 and y > 480 / 2:
            pwm_orders[1] = "300"
            pwm_orders[2] = "000"
            pwm_orders[3] = "000"
            pwm_orders[4] = "300"
        elif x > 640 / 2 and y > 480 / 2:
            pwm_orders[1] = "000"
            pwm_orders[2] = "000"
            pwm_orders[3] = "300"
            pwm_orders[4] = "300"

        with Serial(
            port="/dev/ttyUSB0", baudrate=115200, timeout=1, writeTimeout=1
        ) as port_serie:
            for num_pwm, angle in pwm_orders.items():
                message = bytearray(
                    [ord(str(num_pwm)), ord(";"), ord(angle[0]), ord(angle[1]), ord(angle[2]), ord("a")]
                )
                port_serie.write(message)
                time.sleep(0.001)
