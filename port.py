import socket

target ="127.0.0.1"
open_ports = []

print("Scanning Open Ports.....\n")

for port in range(1,65536):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.05)
    if s.connect_ex((target,port))==0:
        open_ports.append(port)
        print(f"OPEN PORT :{port}")
    s.close()
print("\n Total Open Ports:",len(open_ports))
print("Open Ports:",open_ports)        
