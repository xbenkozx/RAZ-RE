# Nation N32G031 Cortex M0 Microcontroller
There are 3 different board versions with the following board identifiers:
- XD0007_MB_V0.6B
- XD0007_MB_V0.6G1
- YK656-XD0007-A-V1.8

Research is ongoing for decompiling the program image binary.

## Firmware Versions
Board versions XD0007_MB_V0.6B and XD0007_MB_V0.6G1 use similar FW and can be interchanged. All pinouts other than UART RX/TX are the same. Version YK656-XD0007-A-V1.8 uses a different pinout and cannot be used with the other FW versions.

<span style="color:orange;">Please note that the LED pin on the XD0007_MB_V0.6B/XD0007_MB_V0.6G1 is used as the coil trigger on the YK656-XD0007-A-V1.8 board. Take exteme caution and remove the coil cartrige from the vapes before changing FW or programming as not doing so may lead to a fire.</span>

At this moment, the pinout for the YK656-XD0007-A-V1.8 is undefined.

## Pinout
| PIN |      Name      | XD0007_MB_V0.6B                  | XD0007_MB_V0.6G1                 | YK656-XD0007-A-V1.8 |
|:---:|:--------------:|----------------------------------|----------------------------------|---------------------|
| 1   | VCC            | 3V                               | 3V                               |                     |
| 2   | PC14-OSC32_IN  | CHARGE_ISET                      | CHARGE_ISET                      |                     |
| 3   | PC15-OSC32_OUT | NC                               | NC                               |                     |
| 4   | NRST           | RST PAD & PU-RES                 | PU-RES                           |                     |
| 5   | VDDA           | BATTERY VCC                      | 3V                               |                     |
| 6   | PA0            | VAPE ACTIVATE                    | VAPE ACTIVATE                    |                     |
| 7   | PA1            | H311 - 3                         | H311 - 3                         |                     |
| 8   | PA2            | UART TX PAD                      | NC                               |                     |
| 9   | PA3            | UART RX PAD                      | NC                               |                     |
| 10  | PA4            | H311 - 2                         | H311 - 2                         |                     |
| 11  | PA5            | LEDs                             | LEDs                             |                     |
| 12  | PA6            | DISP_BL_ENABLE                   | DISP_BL_ENABLE                   |                     |
| 13  | PA7            | PB0                              | PB0                              |                     |
| 14  | PB0            | BATT+ WITH VOLTAGE   DIVIDER     | CART-VCC WITH VOLTAGE   DIVIDER  |                     |
| 15  | PB1            | NC                               | NC                               |                     |
| 16  | PB2            | CHARGE_STS                       | CHARGE_STS                       |                     |
| 17  | VDD            | GND                              | GND                              |                     |
| 18  | PA8            | EXT_FLASH_SPI_CS                 | EXT_FLASH_SPI_CS                 |                     |
| 19  | PA9            | EXT_FLASH_SPI_SCLK               | EXT_FLASH_SPI_SCLK               |                     |
| 20  | PA10           | EXT_FLASH_SPI_MISO               | EXT_FLASH_SPI_MISO               |                     |
| 21  | PA11           | EXT_FLASH_SPI_MOSI               | EXT_FLASH_SPI_MOSI               |                     |
| 22  | PA12           | NC                               | NC                               |                     |
| 23  | PA13           | SWDIO                            | SWDIO                            |                     |
| 24  | PA14           | SWDCLK                           | SWDCLK                           |                     |
| 25  | PA15           | DISP_SPI_NSS/CS                  | DISP_SPI_NSS/CS                  |                     |
| 26  | PB3            | DISP_SPI_SCLK                    | DISP_SPI_SCLK                    |                     |
| 27  | PB4            | FALSH PWR?                       | FALSH PWR?                       |                     |
| 28  | PB5            | DISP_SPI_MOSI                    | DISP_SPI_MOSI                    |                     |
| 29  | PB6            | DISP_RST                         | DISP_RST                         |                     |
| 30  | PB7            | DISP_RS                          | DISP_RS                          |                     |
| 31  | BOOT0          | GND                              | GND                              |                     |
| 32  | PB8            | VAPE COIL TRIGGER                | VAPE COIL TRIGGER                |                     |

## SWD Debugger
The N32G031 ARM chip is built with a SWD debugging port. This is how you can read and write internal program flash memory. The debugging port is exposed via CC1 and CC2 pins on the USB-C port at the bottom of the device. Standard USB-C cables will not work as per USB-C protocol, CC pins are designated for determining USB VCC voltage.

To be able to access the debugging port on the N32G031, you will need the following.
- USB-C pigtail with CC access. ([Amazon Link](https://www.amazon.com/dp/B0C1YXM9PF))
- ST-Link USB debugging tool. ([Amazon Link](https://www.amazon.com/dp/B07RBK7RHQ))

<i>Note: Other SWD debugging tools may be used such as the Segger J-Link.</i>

Connect each of the CC wires to the SWDIO and SWDCLK pins on the ST-Link.

## OpenOCD
[OpenOCD](https://openocd.org/) is a tool for communicating with an ARM processor via SWD/JTAG. Please refer to OpenOCD documention for installation and setup.

Included in this repo is an OpenOCD configuration for the N32G031 located in the openocd directory. Copy this file to your OpenOCD targets folder.

### Connecting OpenOCD
Once you have installed OpenOCD and copied the N32 configuration file, run the following command in terminal.
> openocd -f interface/stlink.cfg -f target/n32g0x.cfg

On successful connection, you should get the following print out (<i>If the devices does not connect, try reversing the USB-C cable.</i>):
> xPack Open On-Chip Debugger 0.12.0+dev-01312-g18281b0c4-dirty (2023-09-04-22:32)<br/>
> Licensed under GNU GPL v2<br/>
> For bug reports, read
>         http://openocd.org/doc/doxygen/bugs.html<br/>
> Info : auto-selecting first available session transport "hla_swd". To override use 'transport select <transport>'.<br/>
> Info : The selected transport took over low-level target control. The results might differ compared to plain JTAG/SWD<br/>
> Info : clock speed 1800 kHz<br/>
> Info : STLINK V2J44S7 (API v2) VID:PID 0483:3748<br/>
> Info : Target voltage: 3.267509<br/>
> Info : [stm32h7x.cpu0] Cortex-M7 r1p1 processor detected<br/>
> Info : [stm32h7x.cpu0] target has 8 breakpoints, 4 watchpoints<br/>
> Info : starting gdb server for stm32h7x.cpu0 on 3333<br/>
> Info : Listening on port 3333 for gdb connections<br/>
> [stm32h7x.cpu0] halted due to debug-request, current mode: Thread<br/>
> xPSR: 0x01000000 pc: 0x0800e680 msp: 0x20010158<br/>
> Info : Listening on port 6666 for tcl connections<br/>
> Info : Listening on port 4444 for telnet connections<br/>
> Info : accepting 'telnet' connection on tcp/4444

Mark the cable to know the correct orientation for later use.

### OpenOCD Telnet Session
Once connected, you can now open a telnet connection to your localhost on port 4444. This will allow you to send OpenOCD commands to the device.

Open a new terminal window and enter:
>telnet localhost 4444

### OpenOCD Terminal
The following are commands on reading and writing to the device. Please refer to the [OpenOCD documentation](https://openocd.org/doc/html/General-Commands.html) for commands.

#### Read Memory
The internal flash memory on the N32 chip is unlocked and unencrypted. To view the memory use the following command:
> mdw 0x0 1
This will read back 1 block of 32 bytes in hex format from address 0x0. Addresses 0x800000 - 0x801FFFF are also mapped to 0x0 - 0x1FFFF.

#### Dump Memory
The following command will dump the entire contents of the program memory to a file name <i>fw_dump.bin</i>:
>dump_image fw_dump.bin 0x0 0x1FFFF

#### Disable Write Protection
By default, the chip write protection is enabled after reset. It is locked so memory corruption does not occur. To unlock the program memory for writing you must enter two keys into the FLASH_KEY register (0x40022004).

KEY_1
>write_memory 0x40022004 32 0x45670123;

KEY_2
>write_memory 0x40022004 32 0xCDEF89AB;

<br/>
Confirm the memory is unlocked by reading the FLASH_CTRL register (0x40022010):

>mdw 0x40022010 1

<i>LOCKED = 0x00000080, UNLOCKED = 0x00000000</i>

#### Mass Erase Memory
In order to write to memory, the memory will need to be erased. Erase all the data with the following:

<br/>
Set the FLASH_CTRL.MER bit to' 1'

>write_memory 0x40022010 32 0x4

Set the FLASH_CTRL.START bit to' 1'

>write_memory 0x40022010 32 0x44

#### Write image to memory
Make sure write protection is disabled. If it is not, refer above to disable write protection.

To upload an binary image to the program memory do the following:

<br/>
Enable Programming Mode:

>write_memory 0x40022010 32 0x210;

Upload the binary image:

>load_image fw_dump.bin 0x0

Reset the device to run the program.

>reset run

Or halt the program on reset:

>reset halt









<!-- # Erase Page
Set the FLASH_CTRL.PER bit to' 1';
>write_memory 0x40022010 32 0x2

Select the page to be erased with the FLASH_ADD register;
>write_memory 0x40022014 32 0x08000000

Set the FLASH_CTRL.START bit to' 1'
>write_memory 0x40022010 32 0x42

<br/>

# Erase All Flash (Mass Erase)
Set the FLASH_CTRL.MER bit to' 1'

>write_memory 0x40022010 32 0x4

Set the FLASH_CTRL.START bit to' 1'

>write_memory 0x40022010 32 0x44

<br/>

# Erase Options
Unlock the OPTWE bit using KEY1 and KEY2 in the FLASH_OPTKEY register.

>write_memory 0x40022008 32 0x45670123; write_memory 0x40022008 32 0xCDEF89AB;

<p>The FLASH_CTRL register should read 0x200 if successful.</p>
Set the OPTER bit to '1'

>write_memory 0x40022010 32 0x220;

Set the START bit to '1'

>write_memory 0x40022010 32 0x260;

On reboot, read protection will be enabled. This will need to be disabled. <br/><i>Note: Disabling Read Protection will clear the flash memory.</i>

# Disable Read Protection
Follow the steps above to disable flash write protection and flash options write protection.
<br/>

Enable Programming mode

>write_memory 0x40022010 32 0x210;

<br/>
Set the bytes to disable read protection

>write_memory 0x1ffff600 32 0xffff5aa5; -->












