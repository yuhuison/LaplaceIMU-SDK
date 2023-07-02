import serial
import time
import serial.tools.list_ports


def start_assign_wifi(ssid, password):
    ret = []
    searcher = serial.tools.list_ports.comports()
    for port in searcher:
        port_name = port.device  # 获取串口号
        guid = port.hwid  # 获取总线类型GUID
        for dev_id in ["VID_303A&PID_1001"]:
            if dev_id in guid:
                ser = serial.Serial(port_name, 9600, parity=serial.PARITY_NONE, bytesize=8,
                                    stopbits=serial.STOPBITS_ONE)
                ser.open()
                time.sleep(0.4)
                buffer = ser.read_all().decode()
                if "ESP-ROM:esp32c3" in buffer or "[LaplaceMoCap]" in buffer:
                    ser.write(("#=#20001#=#" + ssid + "#=#" + password + "#=#" + "\n").encode())
                    time.sleep(1)
                    buffer = ser.read_all().decode()
                    if "[CODE 20001 SET WIFI 200]" in buffer:
                        ret.append(port_name)
                ser.close()

    return ret


print(start_assign_wifi("123", "456"))
