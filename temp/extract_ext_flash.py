import sys, time
import telnetlib

tn = telnetlib.Telnet("localhost", 4444)

def read_data(single_line = False):
    s = tn.read_until(b'>', 1.0)
    return s


def cmd(command):
    tn.write((f"{command}\r\n").encode())
    return read_data(True)


cmd("reset run")
print(read_data().decode())
time.sleep(1)

data = b''
start_address = 0
pages = 256 #0x2000
page_size = 4096

for page in range(start_address, start_address + pages):
    if(page % 16 == 0 and page != 0):
        print("")
    print("=", end="", flush=True)
    
    cmd('mwb 0x200010CC ' + str(page))
    time.sleep(0.1)
    tn_line = cmd('mdb 0x2000004C ' + str(page_size)).decode()
    #print(tn_line)
    for line in tn_line.split('\r\n'):
        if':' in line:
            hex = line.split(':')[1].replace(' ', '')
            barr = bytes.fromhex(hex)
            data += barr
print("")
with open("dump.bin", 'wb') as f:
    f.write(data)

tn.close