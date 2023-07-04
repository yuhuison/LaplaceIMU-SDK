# LaplaceIMU-SDK
LaplaceIMU-SDK采用了目前最高精度的BNO085作为核心芯片，BNO085用于VR头显级别的追踪，传感器的固件之后也会开源，通过BNO085的资料可以进行多种多样的操作。

# main.py
这段代码实现了一个IMU（惯性测量单元）数据接收和处理的功能。其中，ImuData类定义了IMU数据的各个属性，LaplaceImu类表示一个IMU设备，IMUSet类用于管理多个IMU设备。running方法在一个独立的线程中运行，通过UDP协议接收IMU数据，并将数据解析后存储到imus字典中对应的LaplaceImu对象中。同时，该方法还会计算帧率并定时重置帧率计数器。
## Usage 使用样例
```python
set = IMUSet()
set.start()
while True:
  time.sleep(1) # 每秒执行一次读取
  for imu in set.imus:
    print(imu.data)
```

# setting.py
这段代码实现了通过串口与传感器进行配网的功能。start_assign_wifi函数会遍历可用的串口列表，根据设备ID判断是否为目标传感器。如果是目标传感器，将会打开串口连接，并发送配网指令。配网指令的格式为#=#20001#=#ssid#=#password#=#，其中ssid和password分别为要设置的Wi-Fi的名称和密码。发送配网指令后，等待一段时间以确保指令发送完成并接收到响应。如果接收到的响应中包含[CODE 20001 SET WIFI 200]，则表示配网成功，将该串口号添加到配网成功的列表中。最后，函数返回配网成功的传感器串口号列表，并在主程序中打印该列表。

## Usage 使用样例
在使用前将传感器用Type-C USB线插入到任何一个串口中，之后运行下面代码。
```python
start_assign_wifi(ssid, password)
```
