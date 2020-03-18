from centerVideo import *
from sensor import *
frm time import *

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
            pwm_orders[3] = "000"
            pwm_orders[4] = "300"
        elif x < 640 / 2 and y > 480 / 2:
            pwm_orders[1] = "300"
            pwm_orders[2] = "000"
            pwm_orders[3] = "300"
            pwm_orders[4] = "000"
        elif x > 640 / 2 and y > 480 / 2:
            pwm_orders[1] = "000"
            pwm_orders[2] = "000"
            pwm_orders[3] = "300"
            pwm_orders[4] = "300"

        with Serial(
            port="/dev/ttyACM0", baudrate=115200, timeout=1, writeTimeout=1
        ) as port_serie:
            for num_pwm, angle in pwm_orders:
                message = bytearray(
                    [str(num_pwm), ";", angle[0], angle[1], angle[2], "a"]
                )
                port_serie.write(message)
                time.sleep(0.001)
