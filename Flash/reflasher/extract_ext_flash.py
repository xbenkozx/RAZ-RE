import os, time, threading
import telnetlib
import swd

BLOCKS                  = 256
BLOCK_SIZE              = 4096
FLASH_START_ADDR        = 0

DATA_BUFFER_ADDR        = 0x20000004
PAGE_SET_ADDR           = 0x20001018
WRITE_F_ADDR            = 0x20001020
LVL_RESET_F_ADDR        = 0x20001014
CONTINUE_F_ADDR         = 0x20001004
LEVEL_BUFFER_ADDR       = 0x20001008
LEVEL_READ_BUFFER_ADDR  = 0x2000100D

PROGMEM_ADDR            = 0x08000000
PROGMEM_LEN             = 0x10000
FLASH_KEY_REG           = 0x40022004
FLASH_CTRL_REG          = 0x40022010
FLASH_KEY_1             = 0x45670123
FLASH_KEY_2             = 0xCDEF89AB
FLASH_ADDR_REG          = 0x40022014

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
    data1 = bytes(dev.read_mem(PROGMEM_ADDR, PROGMEM_LEN))
    data2 = bytes(dev.read_mem(PROGMEM_ADDR, PROGMEM_LEN))

    if data1 == data2:
        print("Success")
        with open(file_path, "wb") as f:
            f.write(bytes(data1))
            return True
    else:
        print("Failed")
    return False

def erase_prog_mem():
    print("Erasing PROG_MEM")
    dev.set_mem32(FLASH_KEY_REG, FLASH_KEY_1) # KEY1
    dev.set_mem32(FLASH_KEY_REG, FLASH_KEY_2) # KEY2
    if int.from_bytes(bytes(dev.read_mem32(FLASH_CTRL_REG, 4)), 'little') == 0: #Check for lock bit
        dev.set_mem32(FLASH_CTRL_REG, 0x4)
        dev.set_mem32(FLASH_CTRL_REG, 0x44)
        return True
    return False

def upload_bin(file_path):
    if erase_prog_mem():
        print("Uploading FW: " + file_path)
        reset_halt()
        dev.set_mem32(FLASH_KEY_REG, FLASH_KEY_1) # KEY1
        dev.set_mem32(FLASH_KEY_REG, FLASH_KEY_2) # KEY2
        if int.from_bytes(bytes(dev.read_mem32(FLASH_CTRL_REG, 4)), 'little') == 0: #Check for lock bit
            dev.set_mem32(FLASH_CTRL_REG, 0x1)
            dev.set_mem32(FLASH_ADDR_REG, PROGMEM_ADDR)
            with open(file_path, 'rb') as f:
                data = f.read(0x10000)
                offset = 0
                for offset in range(0, PROGMEM_LEN, 4):
                    # print("=", end='', flush=True)
                    b = int.from_bytes(data[offset:offset+4], 'little')
                    dev.set_mem32(PROGMEM_ADDR + offset, b)
                    k = int.from_bytes(bytes(dev.read_mem32(PROGMEM_ADDR + offset, 4)), 'little')
                    if k != b:
                        print(hex(PROGMEM_ADDR + offset), hex(b))
                        print(hex(k))
                        print(hex(int.from_bytes(bytes(dev.read_mem32(PROGMEM_ADDR + offset, 4)), 'little')))
                        break
                # print("")
        
def dump_flash(file_path, dump_mem=True):
    print("Dumping Flash> " + file_path)
    # print("BUFFER_MEM_ADDR:\t" + hex(DATA_BUFFER_ADDR))
    # print("PAGE_SET_MEM_ADDR:\t" + hex(PAGE_SET_ADDR))
    # print("WRITE_SET_MEM_ADDR:\t" + hex(WRITE_SET_ADDR))
    print("BLOCK_SIZE:\t\t" + str(BLOCK_SIZE))
    print("BLOCKS:\t\t\t" + str(BLOCKS))

    data = b''

    dev.write_mem8(LVL_RESET_F_ADDR, [1]) #Set juice level reset flag
    dev.write_mem32(LEVEL_BUFFER_ADDR, [0, 0, 0, 0]) #Optional - Set juice level 0x0 = FULL, 0x2FFFF = empty
    # dev.write_mem32(LEVEL_BUFFER_ADDR, [1]) #Set to one to write to memory
    # dev.write_mem32(LEVEL_BUFFER_ADDR, [1])
    time.sleep(0.1)
    dev.write_mem8(CONTINUE_F_ADDR, [1])
    time.sleep(0.5)

    print(bytes(dev.read_mem(LEVEL_READ_BUFFER_ADDR, 5)))

    if dump_mem:
        print(0, end=":")
        for page in range(FLASH_START_ADDR, FLASH_START_ADDR + BLOCKS):
            if(page % 64 == 0 and page != 0):
                print("")
                print(int(page / 64), end=":")
            print("=", end="", flush=True)
            dev.write_mem8(PAGE_SET_ADDR, [page])
            time.sleep(0.05)
            d = bytes(dev.read_mem(DATA_BUFFER_ADDR, BLOCK_SIZE))
            data += d

        print("")
        with open(file_path, 'wb') as f:
            f.write(data)
    
flash_dump_path = "fdump.bin"
fw_dump_path = "/flash/reflasher/fw_dump_tmp.bin"
reflasher_path = "flash/reflasher/reflasher.bin"

# reset_halt()
# upload_bin("flash/reflasher/XD0007_MB_V0.6G1.bin")
# reset()

# reset_halt()
# dump_fw(fw_dump_path)
reset_halt()
upload_bin(reflasher_path)
reset()
dump_flash(flash_dump_path, False)
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