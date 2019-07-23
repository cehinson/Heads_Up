from src.sensors import Camera
from threading import Thread

cam = Camera

t1 = Thread(target=cam.next_frame)
t2 = Thread(target=cam.segment)

t1.start()
t2.start()