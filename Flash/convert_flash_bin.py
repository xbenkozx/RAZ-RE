import argparse, os
from PIL import Image



mem_map = [
    ['BG_1',            (80, 160),  0x00],
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

vape_activation_time_addr  = 0xF800
vape_in_use_flag_addr      = 0xF804

def loadImage(f, size, mem_offset):
    xdim = size[0]
    ydim = size[1]
    length = xdim * ydim
    data = []
    i = 0

    offset = mem_offset

    
    f.seek(offset)
    while(len(data) < length):
        d = int.from_bytes(f.read(2), byteorder='big')
        data.append(d)

    im = Image.new("RGB",(xdim,ydim))
    for y in range(ydim):
        for x in range(xdim):
            px = data[i]
            i = i + 1
            im.putpixel((x,y),((px&0xF800) >> 8, (px&0x07E0) >> 3, (px&0x001F) << 3))

    return im

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='RAZ/KRAZE External Flash Conversion',
                    description='A tool for converting RAZ/KRAZE vape external memory to images.')
    parser.add_argument('-f', '--file', help="BIN file path")
    parser.add_argument('-c', '--config', action='store_true', help='Output vape config only')
    args = parser.parse_args()

    bin_file_path = args.file

    if not os.path.exists('images'):
        os.mkdir('images')

    vape_activation_time    = 0
    vape_in_use_flag        = 0

    if bin_file_path != None and bin_file_path != "" and os.path.exists(bin_file_path):
        with open(bin_file_path, 'rb') as f:
            if not args.config:
                for img in mem_map:
                    im = loadImage(f, img[1], img[2])
                    im.save('images/' + img[0] + '.jpg')

            f.seek(vape_activation_time_addr)
            vape_activation_time = int.from_bytes(f.read(4), byteorder='big')

            f.seek(vape_in_use_flag_addr)
            vape_in_use_flag = int.from_bytes(f.read(1), byteorder='big')

            print(f'Vape Activation Time: {str(vape_activation_time / 1000)}s ({str(vape_activation_time)})')
            print(f'In-Use Flag: {hex(vape_in_use_flag)}')

            # write vape in use flag and vape time to file
            with open('vape_config.txt', 'w') as cf:
                cf.write(f'Vape Activation Time: {str(vape_activation_time / 1000)}s ({str(vape_activation_time)})\n')
                cf.write(f'In-Use Flag: {hex(vape_in_use_flag)}')


    
    else:
        print("Error: Invalid file path")