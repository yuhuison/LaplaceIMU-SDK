import dataclasses
import struct
import threading
from math import isnan
import time
import socket
import torch


@dataclasses.dataclass
class ImuData:
    accX: float = 0.0
    accY: float = 0.0
    accZ: float = 0.0
    i: float = 0.0
    j: float = 0.0
    k: float = 0.0
    real: float = 1


class LaprasImu:
    data: ImuData = ImuData(0, 0, 0, 0, 0, 0)
    last_data_time:int = 0
    ggid = 0
    fps = 0

    def __init__(self, imuid):
        self.ggid = imuid


class IMUSet:
    imus: dict = dict()
    living:bool = True
    def __init__(self):
        self.t = threading.Thread(target=self.running)

    def start(self):
        self.t.start()

    def stop(self):
        self.living = False

    def running(self):
        def mills():
            return int(round(time.time() * 1000))

        HOST = '0.0.0.0'
        PORT = 42605
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((HOST, PORT))
        tt = mills()
        while self.living:
            data, addr = sock.recvfrom(1024)
            msg = struct.unpack("<ifffffffL", data)
            ggid, i, j, k, real, accX, accY, accZ, mill_time = msg
            if real == 0:
                real = 1
            if not (isnan(ggid) or isnan(accX) or isnan(accY) or isnan(
                    accZ)):
                if ggid not in self.imus.keys():
                    self.imus[ggid] = LaprasImu(ggid)
                imu = self.imus[ggid]
                if mill_time > imu.last_data_time:
                    imu.last_data_time = mill_time
                    imu.fps = imu.fps + 1
                    imu.data = ImuData(accX, accY, accZ, i, j, k, real)
                    if mills() - tt > 1000:
                        for imu in self.imus.values():
                            if imu.fps != 0:
                                imu.fps = 0
                        tt = mills()
