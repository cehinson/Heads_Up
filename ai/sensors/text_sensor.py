
from sensors.vision_sensor import VisionSensor

import pytesseract


class TextSensor(VisionSensor):
    '''Text input from a region of the screen'''

    def __init__(self):
        raise NotImplementedError
