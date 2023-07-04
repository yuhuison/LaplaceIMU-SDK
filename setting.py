import serial  # 导入serial模块，用于串口通信
import time  # 导入time模块，用于处理时间相关操作
import serial.tools.list_ports  # 导入serial.tools.list_ports模块，用于获取可用串口列表

def start_assign_wifi(ssid, password):
    ret = []  # 创建一个空列表，用于存储配网成功的传感器串口号
    searcher = serial.tools.list_ports.comports()  # 获取可用串口列表
    for port in searcher:  # 遍历每个可用串口
        port_name = port.device  # 获取串口号
        guid = port.hwid  # 获取总线类型GUID
        for dev_id in ["VID_303A&PID_1001"]:  # 遍历每个设备ID
            if dev_id in guid:  # 如果设备ID在总线类型GUID中
                ser = serial.Serial(port_name, 9600, parity=serial.PARITY_NONE, bytesize=8,
                                    stopbits=serial.STOPBITS_ONE)  # 打开串口连接
                ser.open()  # 打开串口连接
                time.sleep(0.4)  # 等待0.4秒，确保串口连接稳定
                buffer = ser.read_all().decode()  # 读取串口接收缓冲区的数据并解码为字符串
                if "ESP-ROM:esp32c3" in buffer or "[LaplaceMoCap]" in buffer:
                    # 如果缓冲区中包含"ESP-ROM:esp32c3"或"[LaplaceMoCap]"
                    ser.write(("#=#20001#=#" + ssid + "#=#" + password + "#=#" + "\n").encode())
                    # 向串口发送配网指令，格式为"#=#20001#=#ssid#=#password#=#"
                    time.sleep(1)  # 等待1秒，确保配网指令发送完成并接收到响应
                    buffer = ser.read_all().decode()  # 读取串口接收缓冲区的数据并解码为字符串
                    if "[CODE 20001 SET WIFI 200]" in buffer:
                        # 如果缓冲区中包含"[CODE 20001 SET WIFI 200]"
                        ret.append(port_name)  # 将串口号添加到配网成功的列表中
                ser.close()  # 关闭串口连接

    return ret  # 返回配网成功的传感器串口号列表

print(start_assign_wifi("123", "456"))  # 执行配网操作并打印配网成功的传感器串口号列表
