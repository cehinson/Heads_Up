
from sensors.sensor import Sensor

import PIL


class VisionSensor(Sensor):
    '''Input from a region of the screen'''

    def __init__(self, rect):
        raise NotImplementedError
