import os, time, argparse, swd
from PIL import Image

# -------------------------------------
# REFLASHER FW MEMORY ADDRESSES
# -------------------------------------
DATA_BUFFER_ADDR        = 0x20000004
LEVEL_BUFFER_ADDR       = 0x20001008
STATUS_REG_ADDR         = 0x20001014
WRITE_FLAG_ADDR         = 0x20001018
LVL_RESET_FLAG_ADDR     = 0x20001010
CONTINUE_FLAG_ADDR      = 0x20001004

# -------------------------------------
# MCU PROG MEM
# -------------------------------------
MCU_PROGMEM_ADDR        = 0x08000000
MCU_PROGMEM_LEN         = 0x10000

# -------------------------------------
# MCU FLASH REGISTERS
# -------------------------------------
MCU_FLASH_KEY_REG       = 0x40022004
MCU_FLASH_CTRL_REG      = 0x40022010
MCU_FLASH_ADDR_REG      = 0x40022014

# -------------------------------------
# MCU FLASH KEYS
# -------------------------------------
MCU_FLASH_KEY_1         = 0x45670123
MCU_FLASH_KEY_2         = 0xCDEF89AB

# -------------------------------------
# SPI FLASH
# -------------------------------------
FLASH_BLOCKS            = 256
FLASH_BLOCK_SIZE        = 4096
FLASH_START_ADDR        = 0x0

# -------------------------------------
# SPI FLASH MISC DATA MAP
# -------------------------------------
ACTIVATION_TIME_ADDR    = 0xF800 #LENGTH 4
IN_USE_FLAG_ADDR        = 0xF804

# -------------------------------------
# SPI FLASH IMAGE DATA MAP
# -------------------------------------
mem_map = [
    ['BG_1',            (80, 160),  0x0],
    ['BATT_0',          (72,72),    0x6400],
    ['BATT_1',          (72,72),    0x8c80],
    ['BATT_2',          (72,72),    0xb500],
    ['BATT_3',          (72,72),    0xdd80],
    ['BATT_4',          (72,72),    0x10600],
    ['BATT_5',          (72,72),    0x12e80],
    ['BATT_6',          (72,72),    0x15700],
    ['BATT_7',          (72,72),    0x17f80],
    ['BATT_8',          (72,72),    0x1a800],
    ['BATT_9',          (72,72),    0x1d080],
    ['BATT_10',         (72,72),    0x1f900],
    ['TANK_0',          (72,72),    0x22180],
    ['TANK_1',          (72,72),    0x24a00],
    ['TANK_2',          (72,72),    0x27280],
    ['TANK_3',          (72,72),    0x29b00],
    ['TANK_4',          (72,72),    0x2c380],
    ['TANK_5',          (72,72),    0x2ec00],
    ['TANK_6',          (72,72),    0x31480],
    ['FIRE_1',          (80,160),   0x33d00],
    ['FIRE_2',          (80,160),   0x3a100],
    ['FIRE_3',          (80,160),   0x40500],
    ['FIRE_4',          (80,160),   0x46900],
    ['FIRE_5',          (80,160),   0x4cd00],
    ['FIRE_6',          (80,160),   0x53100],
    ['FIRE_7',          (80,160),   0x59500],
    ['FIRE_8',          (80,160),   0x5f900],
    ['FIRE_9',          (80,160),   0x65d00],
    ['FIRE_10',         (80,160),   0x6c100],
    ['FIRE_11',         (80,160),   0x72500],
    ['FIRE_12',         (80,160),   0x78900],
    ['FIRE_13',         (80,160),   0x7ed00],
    ['FIRE_14',         (80,160),   0x85100],
    ['FIRE_15',         (80,160),   0x8b500],
    ['FIRE_16',         (80,160),   0x91900],
    ['PLUG_0',          (80,160),   0x97d00],
    ['RAZ_ANIM_0',      (35, 87),   0x9e100],
    ['RAZ_ANIM_1',      (35, 87),   0x9F8CA],
    ['RAZ_ANIM_2',      (35, 87),   0xA1094],
    ['RAZ_ANIM_3',      (35, 87),   0xA285E],
    ['RAZ_ANIM_4',      (35, 87),   0xA4028],
    ['RAZ_ANIM_5',      (35, 87),   0xA57F2],
    ['RAZ_ANIM_6',      (35, 87),   0xA6FBC],
    ['RAZ_ANIM_7',      (35, 87),   0xA8786],
    ['RAZ_ANIM_8',      (35, 87),   0xA9F50],
    ['RAZ_ANIM_9',      (35, 87),   0xAB71A],
    ['RAZ_ANIM_10',     (35, 87),   0xACEE4],
    ['RAZ_ANIM_11',     (35, 87),   0xAE6AE],
    ['RAZ_ANIM_12',     (35, 87),   0xAFE78],
    ['RAZ_ANIM_13',     (35, 87),   0xB1642],
    ['RAZ_ANIM_14',     (35, 87),   0xB2E0C],
    ['RAZ_ANIM_15',     (35, 87),   0xB45D6],
    ['RAZ_ANIM_16',     (35, 87),   0xB5DA0],
    ['RAZ_ANIM_17',     (35, 87),   0xB756A],
    ['RAZ_ANIM_18',     (35, 87),   0xB8D34],
    ['RAZ_ANIM_19',     (35, 87),   0xBA4FE],
    ['RAZ_ANIM_20',     (35, 87),   0xBBCC8],
    ['RAZ_ANIM_21',     (35, 87),   0xBD492],
    ['RAZ_ANIM_22',     (35, 87),   0xBEC5C],
    ['RAZ_ANIM_23',     (35, 87),   0xC0426],
    ['RAZ_ANIM_24',     (35, 87),   0xC1BF0],
    ['RAZ_ANIM_25',     (35, 87),   0xC33BA],
    ['RAZ_ANIM_26',     (35, 87),   0xC4B84],
    ['RAZ_ANIM_27',     (35, 87),   0xC634E],
    ['RAZ_ANIM_28',     (35, 87),   0xC7B18],
    ['PLUG_1',          (80,160),   0xc92e2],
    ['CHARGING_0',      (31,64),    0xcf6e2],
    ['CHARGING_1',      (31,64),    0xd0662],
    ['CHARGING_2',      (31,64),    0xd15e2],
    ['CHARGING_3',      (31,64),    0xd2562],
    ['CHARGING_4',      (31,64),    0xd34e2],
    ['CHARGING_5',      (31,64),    0xd4462],
    ['PLUG_2',          (80, 160),  0xd53e2],
    ['KRAZE_ANIM_0',    (21, 89),   0xDB7E2],
    ['KRAZE_ANIM_1',    (21, 89),   0xDC67C],
    ['KRAZE_ANIM_2',    (21, 89),   0xDD516],
    ['KRAZE_ANIM_3',    (21, 89),   0xDE3B0],
    ['KRAZE_ANIM_4',    (21, 89),   0xDF24A],
    ['KRAZE_ANIM_5',    (21, 89),   0xE00E4],
    ['KRAZE_ANIM_6',    (21, 89),   0xE0F7E],
    ['KRAZE_ANIM_7',    (21, 89),   0xE1E18],
    ['KRAZE_ANIM_8',    (21, 89),   0xE2CB2],
    ['KRAZE_ANIM_9',    (21, 89),   0xE3B4C],
    ['KRAZE_ANIM_10',   (21, 89),   0xE49E6],
    ['KRAZE_ANIM_11',   (21, 89),   0xE5880],
    ['KRAZE_ANIM_12',   (21, 89),   0xE671A],
    ['KRAZE_ANIM_13',   (21, 89),   0xE75B4],
    ['KRAZE_ANIM_14',   (21, 89),   0xE844E],
    ['KRAZE_ANIM_15',   (21, 89),   0xE92E8],
    ['KRAZE_ANIM_16',   (21, 89),   0xEA182],
    ['KRAZE_ANIM_17',   (21, 89),   0xEB01C],
    ['KRAZE_ANIM_18',   (21, 89),   0xEBEB6],
    ['KRAZE_ANIM_19',   (21, 89),   0xECD50],
    ['KRAZE_ANIM_20',   (21, 89),   0xEDBEA],
    ['KRAZE_ANIM_21',   (21, 89),   0xEEA84],
    ['KRAZE_ANIM_22',   (21, 89),   0xEF91E],
    ['KRAZE_ANIM_23',   (21, 89),   0xF07B8],
    ['KRAZE_ANIM_24',   (21, 89),   0xF1652],
    ['KRAZE_ANIM_25',   (21, 89),   0xF24EC],
    ['KRAZE_ANIM_26',   (21, 89),   0xF3386],
    ['KRAZE_ANIM_27',   (21, 89),   0xF4220],
    ['KRAZE_ANIM_28',   (21, 89),   0xF50BA],
    ['KRAZE_ANIM_29',   (21, 89),   0xF5F54],
    ['KRAZE_ANIM_30',   (21, 89),   0xF6DEE]
]


class ReFlasher:

    verbose = False
    flash_output_file = ""
    flash_input_file = ""
    reflasher_fw_file = ""
    level_value = None
    
    def __init__(self):
        self.dev    = None
        self.cm     = None
    
    def connect(self):
        self.dev = swd.Swd()
        self.cm = swd.CortexM(self.dev)
        print(self.dev.get_version().str)
        print("Target Voltage:", self.dev.get_target_voltage())
        print("MCU ID:", hex(self.dev.get_idcode()))

    def reset_halt(self):
        try:
            self.cm.reset_halt()
        except:
            pass
    def reset(self):
        try:
            self.cm.reset()
        except:
            pass
    def dump_fw(self, file_path):
        print("Extracting FW: ", end='', flush=True)
        data1 = bytes(self.dev.read_mem(MCU_PROGMEM_ADDR, MCU_PROGMEM_LEN))
        data2 = bytes(self.dev.read_mem(MCU_PROGMEM_ADDR, MCU_PROGMEM_LEN))

        if data1 == data2:
            print("Success")
            with open(file_path, "wb") as f:
                f.write(bytes(data1))
                return True
        else:
            print("Failed")
        return False
    def upload_fw(self, file_path):
        if self.erase_prog_mem():
            print("Uploading FW: " + file_path)
            self.reset_halt()
            self.dev.set_mem32(MCU_FLASH_KEY_REG, MCU_FLASH_KEY_1) # KEY1
            self.dev.set_mem32(MCU_FLASH_KEY_REG, MCU_FLASH_KEY_2) # KEY2
            if int.from_bytes(bytes(self.dev.read_mem32(MCU_FLASH_CTRL_REG, 4)), 'little') == 0: #Check for lock bit
                self.dev.set_mem32(MCU_FLASH_CTRL_REG, 0x1)
                self.dev.set_mem32(MCU_FLASH_ADDR_REG, MCU_PROGMEM_ADDR)
                with open(file_path, 'rb') as f:
                    data = f.read(0x10000)
                    offset = 0
                    for offset in range(0, MCU_PROGMEM_LEN, 4):
                        if self.verbose:
                            print("=", end='', flush=True)
                        b = int.from_bytes(data[offset:offset+4], 'little')
                        self.dev.set_mem32(MCU_PROGMEM_ADDR + offset, b)
                        k = int.from_bytes(bytes(self.dev.read_mem32(MCU_PROGMEM_ADDR + offset, 4)), 'little')
                        if k != b:
                            print(hex(MCU_PROGMEM_ADDR + offset), hex(b))
                            print(hex(k))
                            print(hex(int.from_bytes(bytes(self.dev.read_mem32(MCU_PROGMEM_ADDR + offset, 4)), 'little')))
                            break
                    if self.verbose:
                        print("")

        #TODO: Verfify upload
    def erase_prog_mem(self):
        print("Erasing PROG_MEM")
        self.dev.set_mem32(MCU_FLASH_KEY_REG, MCU_FLASH_KEY_1) # KEY1
        self.dev.set_mem32(MCU_FLASH_KEY_REG, MCU_FLASH_KEY_2) # KEY2
        if int.from_bytes(bytes(self.dev.read_mem32(MCU_FLASH_CTRL_REG, 4)), 'little') == 0: #Check for lock bit
            self.dev.set_mem32(MCU_FLASH_CTRL_REG, 0x4)
            self.dev.set_mem32(MCU_FLASH_CTRL_REG, 0x44)
            return True
        return False
    
    
    def set_level_value(self):
        self.dev.write_mem8(LVL_RESET_FLAG_ADDR, [1]) #Set juice level reset flag
        self.dev.write_mem32(LEVEL_BUFFER_ADDR, self.level_value) #Optional - Set juice level 0x0 = FULL, 0x2FFFF = empty
        time.sleep(0.1)
        self.dev.write_mem8(CONTINUE_FLAG_ADDR, [1])
        time.sleep(0.5)
        if self.verbose:
            print(bytes(self.dev.read_mem(LEVEL_BUFFER_ADDR, 5)))


    def upload_flash(self):
        if os.path.exists(self.flash_input_file):
            print("Writing Flash < " + self.flash_input_file)
            if self.verbose:
                print("BLOCK_SIZE:\t\t" + str(FLASH_BLOCK_SIZE))
                print("BLOCKS:\t\t\t" + str(FLASH_BLOCKS))
                
            with open(self.flash_input_file, 'rb') as f:
                
                buffer = f.read()
                self.dev.write_mem8(WRITE_FLAG_ADDR, [1])
                self.dev.write_mem8(CONTINUE_FLAG_ADDR, [1])
                
                # Wait for erase
                while(int.from_bytes(bytes(self.dev.read_mem8(STATUS_REG_ADDR, 1)), 'big') != 5):
                        pass
                
                # Write data to memory
                for block in range(FLASH_BLOCKS):
                    bl_data = buffer[block * FLASH_BLOCK_SIZE: (block * FLASH_BLOCK_SIZE) + FLASH_BLOCK_SIZE]
                    # self.dev.write_mem8(STATUS_REG_ADDR, [1])
                    for offset in range(0, len(bl_data), 4):
                        d = [bl_data[offset], bl_data[offset+1], bl_data[offset+2], bl_data[offset+3]]
                        self.dev.write_mem32(DATA_BUFFER_ADDR + offset, d)

                    #Se to 4 to write data to flash
                    self.dev.write_mem8(STATUS_REG_ADDR, [4]) 

                    #Wait for write to complete
                    while(int.from_bytes(bytes(self.dev.read_mem8(STATUS_REG_ADDR, 1)), 'big') != 5):
                            pass

                self.dev.write_mem8(CONTINUE_FLAG_ADDR, [0])
                        
        else:
            print(f"Error - Invalid file path: {self.flash_input_file}")       
    def dump_flash(self, file_path=""):
        print("Dumping Flash > " + file_path)
        if self.verbose:
            print("BLOCK_SIZE:\t\t" + str(FLASH_BLOCK_SIZE))
            print("BLOCKS:\t\t\t" + str(FLASH_BLOCKS))

        self.dev.write_mem8(CONTINUE_FLAG_ADDR, [1])

        # Read data from memory
        data = b''
        if file_path != "":
            if self.verbose:
                print(0, end=":")
            for block in range(FLASH_BLOCKS):
                if(block % 64 == 0 and block != 0):
                    if self.verbose:
                        print("")
                        print(int(block / 64), end=":")
                if self.verbose:
                    print("=", end="", flush=True)

                #Se to 4 to write data to memory from flash
                self.dev.write_mem8(STATUS_REG_ADDR, [4])

                #Wait for read to complete
                while(int.from_bytes(bytes(self.dev.read_mem8(STATUS_REG_ADDR, 1)), 'big') != 5):
                        pass

                # Read from memory and add to existing data buffer
                d = bytes(self.dev.read_mem(DATA_BUFFER_ADDR, FLASH_BLOCK_SIZE))
                data += d
            

            if self.verbose:
                print("")
            with open(file_path, 'wb') as f:
                f.write(data)

class FlashConvert:
    @staticmethod
    def extract_image(fp, size, mem_offset):
        xdim = size[0]
        ydim = size[1]
        length = xdim * ydim
        data = []
        i = 0

        offset = mem_offset
        fp.seek(offset)
        while(len(data) < length):
            d = int.from_bytes(fp.read(2), byteorder='big')
            data.append(d)

        im = Image.new("RGB",(xdim,ydim))
        for y in range(ydim):
            for x in range(xdim):
                px = data[i]
                i = i + 1
                im.putpixel((x,y),((px & 0xF800) >> 8, (px & 0x07E0) >> 3, (px & 0x001F) << 3))

        return im
    @staticmethod
    def extract(bin_file_path, image_directory):
        if not os.path.exists(image_directory):
            os.mkdir(image_directory)

        if bin_file_path != None and bin_file_path != "" and os.path.exists(bin_file_path):
            vape_activation_time = ""
            vape_in_use_flag = ""
            with open(bin_file_path, 'rb') as f:
                for img in mem_map:
                    im = FlashConvert.extract_image(f, img[1], img[2])
                    im.save(os.path.join(image_directory, img[0] + '.bmp'))

                f.seek(ACTIVATION_TIME_ADDR)
                vape_activation_time = int.from_bytes(f.read(4), byteorder='big')

                f.seek(IN_USE_FLAG_ADDR)
                vape_in_use_flag = int.from_bytes(f.read(1), byteorder='big')

            print(f'Vape Activation Time: {str(vape_activation_time / 100)}s ({str(vape_activation_time)})')
            print(f'In-Use Flag: {hex(vape_in_use_flag)}')

            # with open('vape_config.txt', 'w') as cf:
            #     cf.write(f'Vape Activation Time: {str(vape_activation_time / 100)}s ({str(vape_activation_time)})\n')
            #     cf.write(f'In-Use Flag: {hex(vape_in_use_flag)}')

        else:
            print(f"Error - Invalid file path: {bin_file_path}")
    @staticmethod
    def compile(bin_file_path, image_directory):
        buffer = bytearray(b'\xff') * (FLASH_BLOCK_SIZE * FLASH_BLOCKS)

        for img in mem_map:
            im_data = bytearray()
            im = Image.open(os.path.join(image_directory, img[0] + ".bmp"))
            if im.size == img[1]:
                data_size = im.size[0] * im.size[1] * 2
                for y in range(im.size[1]):
                    for x in range(im.size[0]):
                        px = im.getpixel((x,y))
                        r = 248 if px[0] > 248 else px[0]
                        g = 252 if px[1] > 252 else px[1]
                        b = 248 if px[2] > 248 else px[2]
                        i = (b >> 3) | (g << 3) | (r << 8) 
                        try:
                            b = int.to_bytes(i, 2, 'big')
                            im_data.extend(b)
                        except Exception as ex:
                            print(img[0], x, y)
                            print(px)
                            print(hex(i))
                            print("Error")
                            print(ex)
                            exit()
                if data_size == len(im_data):
                    buffer[img[2]:img[2]+data_size] = im_data
                
            else:
                print("Image size mismatch: " + img[0])
        # print(hex(len(buffer)))
        with open(bin_file_path, 'wb') as f:
            f.write(buffer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='RAZ/KRAZE External Flash Extractor',
                    description='A tool for extracting RAZ/KRAZE vape external memory to binary image.')
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Prints verbose output')
    parser.add_argument('-i', '--inf', help="Define the input file path for the flash memory binary file")
    parser.add_argument('-o', '--out', help="Define the output file path for the flash memory binary file. If not defined, it will not dump the flash memory")
    parser.add_argument('-f', '--force', action='store_true', help="If set, this will force a flash binary dump or upload without reflashing the FW")
    parser.add_argument('-u', '--upload', help="Upload FW from specified BIN file")
    parser.add_argument('-d', '--download', help="Download FW to specified BIN file")
    parser.add_argument('-r', '--reflasher', help="Define the reflasher.bin FW file path. If not defined, it will assume reflasher.bin is in your current working directory.")
    parser.add_argument('-l', '--level', help="Set the level indicator value. Value can be HEX or INT (0x0 = FULL, 0x2FFFF = EMPTY)")
    parser.add_argument('-e', '--extract', nargs=2, help="Extract the images and battery data from the flash binary file")
    parser.add_argument('-c', '--compile', nargs=2, help="Compile images and battery data to a flash binary file")
    args = parser.parse_args()

    swd_require = args.inf != None or args.out != None or args.upload != None or args.download != None or args.level != None

    if swd_require:
        rf = ReFlasher()
        
        rf.connect()
        rf.reset()
        
        rf.verbose = args.verbose

        if args.inf != None:
            rf.flash_input_file = args.inf
            if args.force:
                rf.upload_flash()
        

        if args.out != None:
            rf.flash_output_file = args.out
            if args.force:
                rf.dump_flash(rf.flash_output_file)

        if args.upload != None:
            rf.reset_halt()
            rf.upload_fw(args.upload)

        if args.download != None:
            rf.reset_halt()
            rf.dump_fw(args.download)

        if args.reflasher != None:
            rf.reflasher_fw_file = args.reflasher

        if args.level != None:
            lvl = str(args.level)
            i = 0
            if lvl.startswith("0x"):
                i = int.from_bytes(bytes.fromhex(lvl.removeprefix('0x').rjust(8, '0')), 'big')
            elif lvl.endswith('%'):
                i = int((1-(int(lvl.removesuffix('%')) / 100)) * 0x40000)
            else:
                i = int(lvl)
            
            rf.level_value = [i & 0xff, (i >> 8) & 0xff, (i >> 16) & 0xff, (i >> 24) & 0xff]

        if (args.level != None or args.inf != None or args.out != None) and not args.force:
            fw_dump_path = "tmp_fw.bin"
            if rf.reflasher_fw_file == "":
                rf.reflasher_fw_file = "reflasher.bin"

            rf.reset_halt()
            rf.dump_fw(fw_dump_path)
            rf.upload_fw(rf.reflasher_fw_file)
            rf.reset()
            time.sleep(1)
            rf.set_level_value()
            rf.reset()
            if rf.flash_output_file != "":
                rf.dump_flash(rf.flash_output_file)
                rf.reset()
                if args.extract == "true":
                    args.extract = rf.flash_output_file
            if rf.flash_input_file != "":
                rf.upload_flash(rf.flash_input_file)
                rf.reset()
            time.sleep(0.2)
            rf.reset_halt()
            rf.upload_fw(fw_dump_path)
        rf.reset()

    if args.extract != None:
        FlashConvert.extract(args.extract[0], args.extract[1])
    
    if args.compile != None:
        FlashConvert.compile(args.compile[0], args.compile[1])