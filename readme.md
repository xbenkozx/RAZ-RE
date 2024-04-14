# RAZ/KRAZE Disposable Vape RE
Reverse-enginering for RAZ/KRAZE disposible vapes. These devices use a Nation N32G0 Cortex M0 ARM microcontroller, ST7735 80x160 TFT display and 8Mb flash storage. 

Thanks to ginbot86 for creating the Flash Memory Map and Display output tables. 

Please check out his repo for some additional information on this vape [https://github.com/ginbot86/ColorLCDVape-RE](https://github.com/ginbot86/ColorLCDVape-RE).

## Hardware
These vapes use the following hardware:
- Nations Tech [N32G031K8Q7-1](https://www.nationstech.com/uploadfile/file/20220907/1662539811646982.pdf) microcontroller, featuring a 48MHz Arm Cortex-M0 core, 64k of internal Flash memory, 8k of SRAM
- Giantech Semiconductor [GT25Q80A](https://uploadcdn.oneyac.com/upload/document/1676268194927_6539.pdf) 8Mbit (1Mbyte) SPI NOR Flash
- LowPowerSemi [LP4068](https://pdf1.alldatasheet.com/datasheet-pdf/download/1244042/POWER/LP4068.html) linear Li-ion battery charger, configured for ~550mA charge current
- LowPowerSemi LDO voltage regulator, labeled "LPS 2NDJ1" but exact model is unknown
- Generic 5-pin SOT-23 vape controller, labeled "AjCH" with electret-type microphone sensing element
- 0.96-inch 80x160 IPS TFT display

## Nation N32G031 Cortex M0 Microcontroller
There are varations in boards. Please refer to <i>[Firmware Readme](/Firmware/readme.md)</i> for more information on board versions and firmware. 

<span style="color:red;"><b>NOTE: USING INCORRECT FIRMWARE CAN RESULT IN DAMAGE TO DEVICE AND/OR FIRE HAZARDS.</b></span>

## Display
| Pin | Name   | Function                                   |
|-----|--------|--------------------------------------------|
| 1   | TP0/NC | Unused                                     |
| 2   | TP1/NC | Unused                                     |
| 3   | SDIN   | SPI data to LCD                            |
| 4   | SCLK   | SPI clock                                  |
| 5   | RS     | Logic Select (low = command, high = data)  |
| 6   | #RST   | Reset (active-low)                         |
| 7   | #CS    | Chip select (active-low)                   |
| 8   | GND    | Power supply/Signal ground                 |
| 9   | NC     | Not connected                              |
| 10  | VDD    | Power supply (3.3V)                        |
| 11  | LEDK   | LED backlight cathode                      |
| 12  | LEDA   | LED backlight anode                        |
| 13  | GND    | Power supply/Signal ground                 |

## External Flash Memory
The external GT25Q80A 8Mbit (1Mbyte) SPI NOR flash memory is used to store the LCD images and animations as well as the vape coil timer that is used to display the vape juice level. The microcontroller uses DMA (Direct Memory Access) to stream image data from the external Flash into the LCD, as data transfers occur as contiguous 4096-byte chunks, corresponding to a single NOR Flash page. Analysis of the microcontroller's memory indicates that the DMA memory buffer lies in RAM addresses 0x2000022C-0x2000062B.

### External Flash Image Format
All images are stored on the external Flash as raw RGB565 16-bit bitmaps (i.e. each pixel takes up 2 bytes of data). Conversion tools, such as ImageConverter565 from Rinky-Dink Electronics' [UTFT library](http://www.rinkydinkelectronics.com/library.php?id=51), can be used to convert image formats like JPEG/PNG into a raw binary file that can be patched into the external Flash at the corresponding offset. There is no metadata stored with the raw images, so the image dimensions must be manually supplied, as shown in the table below.

### External Flash Memory Map
| Index (#) | Offset (Hex) | Length (Hex) | Frame H (px) | Frame V (px) | Category                          | Unused? | Seq (#) |
| --------- | ------------ | ------------ | ------------ | ------------ | --------------------------------- | ------- | ------- |
| 0         | 0            | 6400         | 80           | 160          | Background                        |         | 0       |
| 1         | 6400         | 2880         | 72           | 72           | Battery Icon                      |         | 0       |
| 2         | 8C80         | 2880         | 72           | 72           | Battery Icon                      |         | 1       |
| 3         | B500         | 2880         | 72           | 72           | Battery Icon                      |         | 2       |
| 4         | DD80         | 2880         | 72           | 72           | Battery Icon                      |         | 3       |
| 5         | 10600        | 2880         | 72           | 72           | Battery Icon                      |         | 4       |
| 6         | 12E80        | 2880         | 72           | 72           | Battery Icon                      |         | 5       |
| 7         | 15700        | 2880         | 72           | 72           | Battery Icon                      |         | 6       |
| 8         | 17F80        | 2880         | 72           | 72           | Battery Icon                      |         | 7       |
| 9         | 1A800        | 2880         | 72           | 72           | Battery Icon                      |         | 8       |
| 10        | 1D080        | 2880         | 72           | 72           | Battery Icon                      |         | 9       |
| 11        | 1F900        | 2880         | 72           | 72           | Battery Icon                      |         | 10      |
| 12        | 22180        | 2880         | 72           | 72           | Juice Icon                        |         | 0       |
| 13        | 24A00        | 2880         | 72           | 72           | Juice Icon                        |         | 1       |
| 14        | 27280        | 2880         | 72           | 72           | Juice Icon                        |         | 2       |
| 15        | 29B00        | 2880         | 72           | 72           | Juice Icon                        |         | 3       |
| 16        | 2C380        | 2880         | 72           | 72           | Juice Icon                        |         | 4       |
| 17        | 2EC00        | 2880         | 72           | 72           | Juice Icon                        |         | 5       |
| 18        | 31480        | 2880         | 72           | 72           | Juice Icon                        |         | 6       |
| 19        | 33D00        | 6400         | 80           | 160          | Vaping Animation                  |         | 0       |
| 20        | 3A100        | 6400         | 80           | 160          | Vaping Animation                  |         | 1       |
| 21        | 40500        | 6400         | 80           | 160          | Vaping Animation                  |         | 2       |
| 22        | 46900        | 6400         | 80           | 160          | Vaping Animation                  |         | 3       |
| 23        | 4CD00        | 6400         | 80           | 160          | Vaping Animation                  |         | 4       |
| 24        | 53100        | 6400         | 80           | 160          | Vaping Animation                  |         | 5       |
| 25        | 59500        | 6400         | 80           | 160          | Vaping Animation                  |         | 6       |
| 26        | 5F900        | 6400         | 80           | 160          | Vaping Animation                  |         | 7       |
| 27        | 65D00        | 6400         | 80           | 160          | Vaping Animation                  |         | 8       |
| 28        | 6C100        | 6400         | 80           | 160          | Vaping Animation                  |         | 9       |
| 29        | 72500        | 6400         | 80           | 160          | Vaping Animation                  |         | 10      |
| 30        | 78900        | 6400         | 80           | 160          | Vaping Animation                  |         | 11      |
| 31        | 7ED00        | 6400         | 80           | 160          | Vaping Animation                  |         | 12      |
| 32        | 85100        | 6400         | 80           | 160          | Vaping Animation                  |         | 13      |
| 33        | 8B500        | 6400         | 80           | 160          | Vaping Animation                  |         | 14      |
| 34        | 91900        | 6400         | 80           | 160          | Vaping Animation                  |         | 15      |
| 35        | 97D00        | 6400         | 80           | 160          | Plugin Background 1               | Unused  | 16      |
| 36        | 9E100        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 0       |
| 37        | 9F8CA        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 1       |
| 38        | A1094        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 2       |
| 39        | A285E        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 3       |
| 40        | A4028        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 4       |
| 41        | A57F2        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 5       |
| 42        | A6FBC        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 6       |
| 43        | A8786        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 7       |
| 44        | A9F50        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 8       |
| 45        | AB71A        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 9       |
| 46        | ACEE4        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 10      |
| 47        | AE6AE        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 11      |
| 48        | AFE78        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 12      |
| 49        | B1642        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 13      |
| 50        | B2E0C        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 14      |
| 51        | B45D6        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 15      |
| 52        | B5DA0        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 16      |
| 53        | B756A        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 17      |
| 54        | B8D34        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 18      |
| 55        | BA4FE        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 19      |
| 56        | BBCC8        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 20      |
| 57        | BD492        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 21      |
| 58        | BEC5C        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 22      |
| 59        | C0426        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 23      |
| 60        | C1BF0        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 24      |
| 61        | C33BA        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 25      |
| 62        | C4B84        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 26      |
| 63        | C634E        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 27      |
| 64        | C7B18        | 17CA         | 35           | 87           | Logo Wipe (RAZ)                   |         | 28      |
| 65        | C92E2        | 6400         | 80           | 160          | Plugin Background 2               | Unused  | 0       |
| 66        | CF6E2        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 0       |
| 67        | D0662        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 1       |
| 68        | D15E2        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 2       |
| 69        | D2562        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 3       |
| 70        | D34E2        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 4       |
| 71        | D4462        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 5       |
| 72        | D53E2        | 6400         | 80           | 160          | Plugin Background 3               |         | 0       |
| 73        | DB7E2        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 0       |
| 74        | DC67C        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 1       |
| 75        | DD516        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 2       |
| 76        | DE3B0        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 3       |
| 77        | DF24A        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 4       |
| 78        | E00E4        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 5       |
| 79        | E0F7E        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 6       |
| 80        | E1E18        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 7       |
| 81        | E2CB2        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 8       |
| 82        | E3B4C        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 9       |
| 83        | E49E6        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 10      |
| 84        | E5880        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 11      |
| 85        | E671A        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 12      |
| 86        | E75B4        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 13      |
| 87        | E844E        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 14      |
| 88        | E92E8        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 15      |
| 89        | EA182        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 16      |
| 90        | EB01C        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 17      |
| 91        | EBEB6        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 18      |
| 92        | ECD50        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 19      |
| 93        | EDBEA        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 20      |
| 94        | EEA84        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 21      |
| 95        | EF91E        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 22      |
| 96        | F07B8        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 23      |
| 97        | F1652        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 24      |
| 98        | F24EC        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 25      |
| 99        | F3386        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 26      |
| 100       | F4220        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 27      |
| 101       | F50BA        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 28      |
| 102       | F5F54        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 29      |
| 103       | F6DEE        | E9A          | 21           | 89           | Charger Logo Wipe (KRAZE)         |         | 30      |
| 104       | F8000        | 4            |  N/A         |  N/A         | Total Vape Time x0.01s (LSB->MSB) |         |  N/A    |
| 105       | F8004        | 1            |  N/A         |  N/A         | Vape In Use Flag (0xBB)           |         |  N/A    |

### Notes
  1. Some animation frames found in external Flash memory are used for different branding: RAZ in the USA and KRAZE.
  2. The juice meter value is derived from the vape timer, but the exact formula to derive it has not yet known. However, what is known is that it has no overflow protection and setting the value back to 0x00000000 will reset the juice meter.
  3. If Flash locations 0xF8000-0xF8004 are erased to 0xFF bytes, this flag byte will be reinitialized to 0xBB and the timer will be reinitialized to 0x00000000, also effectively resetting the juice meter. Setting the flag byte at 0xF8004 to anything that is not 0xBB will accomplish the same effect. Additionally, any other bytes in this Flash sector will be clobbered to 0xFF, since a page erase is issued whenever the counter is updated; only the timer and flag bytes are preserved by the firmware.

  ### Resetting the Vape Juice Meter
  As described in <i>External Flash Memory Map</i>, notes 2 and 3 above, filling external Flash locations 0xF8000-0xF8004 with 0xFF will reset the juice meter to full, permitting reuse of the vape once the reservoir is refilled. The microcontroller itself then needs to be reset by pulling the nRST pin to ground, or by power cycling it by disconnecting and reconnecting the battery; this will likely have already happened if one is desoldering and resoldering the external Flash for reprogramming/patching.

  ### Firmware Version Bitmap
  Inside the firmware Flash dump, at addresses 0x7066-0x7E75, appears to be a bitmap version of the aforementioned version number. It appears to be only 60x30 pixels in size, but there are 0x00 padding bytes around this bitmap that do not align to 120-byte boundaries (60 pixels), making determining the "true" image size difficult without decompiling the firmware and finding the function that triggers the version screen.

## Keil MDK / C Library Examples
Nation Tech has a library for Keil MDK IDE. This library is included in the N32G031xx_V2.2.0.zip file. This file also includes examples for different functions of the core.