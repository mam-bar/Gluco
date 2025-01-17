import random
import math
import time


class Sensor:
    def __init__(self):
        # where to begin on curve
        self.x = random.uniform(0, 2 * math.pi)
        self.generator = self.ins_vals()

    def ins_vals(self):
        amplitude = (138.2 - 70) / 2  # average higher and lower bands of insulin
        offset = 70 + amplitude
        noise_level = 2
        while True:  # Continuous generator loop
            sine_value = amplitude * math.sin(self.x) + offset
            ins_val = sine_value + random.uniform(
                -noise_level, noise_level
            )  # add some noise to make it more realistic!
            self.x += 0.005 * math.pi
            yield round(ins_val, 2)

    def sense(self):
        measurement = next(self.generator)
        return measurement

    def dropInsulin(self):
        self.x = 1.5 * math.pi


if __name__ == "__main__":
    a = Sensor()
    while True:
        print(a.sense())
        time.sleep(1)
