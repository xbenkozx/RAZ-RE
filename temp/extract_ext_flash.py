import os, time, threading
import telnetlib
import swd

BLOCKS                  = 256
BLOCK_SIZE              = 4096
FLASH_START_ADDR        = 0
BUFFER_MEM_ADDR         = 0x20000004
PAGE_SET_MEM_ADDR       = 0x20001004
WRITE_SET_MEM_ADDR      = 0x0

dev = swd.Swd()
print(dev.get_version().str)
print("Target Voltage:", dev.get_target_voltage())
#print("MCU ID:", hex(dev.get_idcode()))
cm = swd.CortexM(dev)



def reset_halt():
    try:
        cm.reset_halt()
    except:
        pass
def reset():
    try:
        cm.reset()
    except:
        pass

def dump_fw(file_path):
    print("Extracting FW: ", end='', flush=True)
    data1 = bytes(dev.read_mem(0x08000000, 0x1000))
    data2 = bytes(dev.read_mem(0x08000000, 0x1000))

    if data1 == data2:
        print("Pass")
        with open(file_path, "wb") as f:
            f.write(bytes(data1))
            return True
    else:
        print("Failed")
    return False

def write_mem(addr, data):
    # try:
        dev.write_mem(addr, data)
    # except:
    #     pass
def erase_prop_mem():
    print("Erasing PROG_MEM")
    dev.set_mem32(0x40022004, 0x45670123) # KEY1
    dev.set_mem32(0x40022004, 0xCDEF89AB) # KEY2
    if int.from_bytes(bytes(dev.read_mem32(0x40022010, 4)), 'little') == 0: #Check for lock bit
        dev.set_mem32(0x40022010, 0x4)
        dev.set_mem32(0x40022010, 0x44)
        




def upload_bin(file_path):
    erase_prop_mem()
    reset_halt()
    dev.set_mem32(0x40022004, 0x45670123) # KEY1
    dev.set_mem32(0x40022004, 0xCDEF89AB) # KEY2
    if int.from_bytes(bytes(dev.read_mem32(0x40022010, 4)), 'little') == 0: #Check for lock bit
        dev.set_mem32(0x40022010, 0x1)
        with open(file_path, 'rb') as f:
            data = f.read(0x100)
            #print(data)
            dev.write_mem16(0x08000000, [0, 0])

def dump_flash():
    print("BUFFER_MEM_ADDR:\t" + hex(BUFFER_MEM_ADDR))
    print("PAGE_SET_MEM_ADDR:\t" + hex(PAGE_SET_MEM_ADDR))
    print("WRITE_SET_MEM_ADDR:\t" + hex(WRITE_SET_MEM_ADDR))
    print("BLOCK_SIZE:\t\t" + str(BLOCK_SIZE))
    print("BLOCKS:\t\t\t" + str(BLOCKS))

    data = b''

    print(0, end=":")
    for page in range(FLASH_START_ADDR, FLASH_START_ADDR + BLOCKS):
        if(page % 64 == 0 and page != 0):
            print("")
            print(int(page / 64), end=":")
        print("=", end="", flush=True)
        dev.write_mem8(PAGE_SET_MEM_ADDR, [page])
        time.sleep(0.05)
        d = bytes(dev.read_mem(BUFFER_MEM_ADDR, BLOCK_SIZE))
        data += d

    print("")
    with open("dump.bin", 'wb') as f:
        f.write(data)
        # openocd.run(f"write_memory {hex(PAGE_SET_MEM_ADDR)} 8 {str(page)}")
        # time.sleep(.1)
        # tn_line = openocd.run(f"read_memory {hex(BUFFER_MEM_ADDR)} 8 {str(BLOCK_SIZE)}")
        # # print(tn_line)
        # for line in tn_line.split('\r\n'):
        #     if':' in line:
        #         hex_s = line.split(':')[1].replace(' ', '')
        #         print(hex_s)
        #         # barr = bytes.fromhex(hex_s)
        #         # data += barr
    

fw_dump_path = "fw_dump_tmp.bin"
reflasher_path = "reflasher.bin"

#reset_halt()
#dump_fw(fw_dump_path)
upload_bin(reflasher_path)

reset_halt()
upload_bin(fw_dump_path)
reset()

#dump_flash()





















#os.system("openocd -f interface/stlink.cfg -f target/n32g0x.cfg")

# from openocd import OpenOcdTclRpc

# openocd = OpenOcdTclRpc()
# openocd.__enter__()

# print(openocd.run('reset'))

# cwd = os.getcwd().replace("\\", r"/")

# def dump_fw():
#     print("Extracting FW")
#     openocd.run("reset halt")
#     time.sleep(1)
    
#     d = openocd.run(f'dump_image "{cwd}/fw_dump_tmp.bin" 0x0 0x1000')
#     if "dumped 4096" in d:
#         #Verify
#         print("Verifing FW")
#         d = openocd.run(f'verify_image "{cwd}/fw_dump_tmp.bin" 0x0')
#         if "verified 4096" in d:
#             print("Success")
#             return True
#         else:
#             print("Verification Failed")
#     else:
#         print("Error: FW Download Failed")
#     return False


# def dump_flash():
#     print("BUFFER_MEM_ADDR:\t" + hex(BUFFER_MEM_ADDR))
#     print("PAGE_SET_MEM_ADDR:\t" + hex(PAGE_SET_MEM_ADDR))
#     print("WRITE_SET_MEM_ADDR:\t" + hex(WRITE_SET_MEM_ADDR))
#     print("BLOCK_SIZE:\t\t" + str(BLOCK_SIZE))
#     print("BLOCKS:\t\t\t" + str(BLOCKS))

#     openocd.run("reset run")
#     time.sleep(1)

#     data = b''

#     print(0, end=":")
#     for page in range(FLASH_START_ADDR, FLASH_START_ADDR + BLOCKS):
#         if(page % 64 == 0 and page != 0):
#             print("")
#             print(int(page / 64), end=":")
#         print("=", end="", flush=True)
        
#         openocd.run(f"write_memory {hex(PAGE_SET_MEM_ADDR)} 8 {str(page)}")
#         time.sleep(.1)
#         tn_line = openocd.run(f"read_memory {hex(BUFFER_MEM_ADDR)} 8 {str(BLOCK_SIZE)}")
#         # print(tn_line)
#         for line in tn_line.split('\r\n'):
#             if':' in line:
#                 hex_s = line.split(':')[1].replace(' ', '')
#                 print(hex_s)
#                 # barr = bytes.fromhex(hex_s)
#                 # data += barr
#     print("")
#     with open("dump.bin", 'wb') as f:
#         f.write(data)

# #dump_fw()
# dump_flash()
# tn.close