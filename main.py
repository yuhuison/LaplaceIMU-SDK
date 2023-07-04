import dataclasses  # 导入dataclasses模块，用于创建不可变的数据类
import struct  # 导入struct模块，用于处理二进制数据和C结构体
import threading  # 导入threading模块，用于实现多线程编程
from math import isnan  # 从math模块导入isnan函数，用于检查是否为NaN值
import time  # 导入time模块，用于处理时间相关操作
import socket  # 导入socket模块，用于网络通信
import torch  # 导入torch模块，用于深度学习相关操作

@dataclasses.dataclass
class ImuData:
    accX: float = 0.0  # 加速度X分量，默认为0.0
    accY: float = 0.0  # 加速度Y分量，默认为0.0
    accZ: float = 0.0  # 加速度Z分量，默认为0.0
    i: float = 0.0  # i分量，默认为0.0
    j: float = 0.0  # j分量，默认为0.0
    k: float = 0.0  # k分量，默认为0.0
    real: float = 1  # 实数部分，默认为1

class LaplaceImu:
    data: ImuData = ImuData(0, 0, 0, 0, 0, 0)  # 创建ImuData对象data，并初始化各属性为0
    last_data_time: int = 0  # 上一次数据接收时间，默认为0
    ggid = 0  # 设备ID，默认为0
    fps = 0  # 帧率，默认为0

    def __init__(self, imuid):
        self.ggid = imuid  # 初始化ggid为传入的imuid

class IMUSet:
    imus: dict = dict()  # 创建一个字典用于存储Imu对象，键为ggid，值为LaplaceImu对象
    living: bool = True  # 表示IMUSet对象是否处于运行状态，默认为True

    def __init__(self):
        self.t = threading.Thread(target=self.running)  # 创建一个线程对象，目标函数为running

    def start(self):
        self.t.start()  # 启动线程

    def stop(self):
        self.living = False  # 停止IMUSet对象的运行

    def running(self):
        def mills():
            return int(round(time.time() * 1000))  # 获取当前时间的毫秒表示

        HOST = '0.0.0.0'  # 主机IP地址
        PORT = 42605  # 端口号
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建UDP套接字
        sock.bind((HOST, PORT))  # 绑定IP地址和端口号
        tt = mills()  # 获取当前时间的毫秒表示
        while self.living:  # 当IMUSet对象处于运行状态时
            data, addr = sock.recvfrom(1024)  # 接收数据和发送方的地址
            msg = struct.unpack("<ifffffffL", data)  # 解析接收到的二进制数据
            ggid, i, j, k, real, accX, accY, accZ, mill_time = msg  # 将解析后的数据赋值给变量
            if real == 0:
                real = 1  # 如果real为0，则将其设置为1
            if not (isnan(ggid) or isnan(accX) or isnan(accY) or isnan(accZ)):
                # 如果ggid、accX、accY、accZ中有任何一个值为NaN，则不执行以下代码
                if ggid not in self.imus.keys():
                    self.imus[ggid] = LaplaceImu(ggid)  # 如果ggid不在imus的键中，则创建一个LaplaceImu对象
                imu = self.imus[ggid]  # 获取对应ggid的LaplaceImu对象
                if mill_time > imu.last_data_time:
                    imu.last_data_time = mill_time  # 更新最后接收数据的时间
                    imu.fps = imu.fps + 1  # 帧率加1
                    imu.data = ImuData(accX, accY, accZ, i, j, k, real)  # 更新imu的数据
                    if mills() - tt > 1000:  # 如果当前时间与tt的差值大于1秒
                        for imu in self.imus.values():
                            if imu.fps != 0:
                                imu.fps = 0  # 将所有imu的帧率重置为0
                        tt = mills()  # 更新tt为当前时间的毫秒表示
