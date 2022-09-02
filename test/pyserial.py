import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    print(p.device)
    print(p.name)
    print(p.description)
    print(p.hwid)
    print(p.vid)
    print(p.pid)
    print(p.serial_number)
    print(p.location)
    print(p.manufacturer)
    print(p.product)
    print(p.interface)