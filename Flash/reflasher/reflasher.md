# RAZ/KRAZE ReFlasher
This is a tool for extracting and loading memory onto the external flash chip. You can replace stock images and animations with your own as well as set the juice level.

## How It Works
Since there is no direct access to the external flash, custom firmware is uploaded to the MCU and used as a buffer to exchange data via SDRAM memory access. When the custom FW first boots it waits for a continue flag. During this wait, you can set the WRITE_DATA_FLAG flag, RESET_LEVEL_FLAG and the RESET_LEVEL_VALUE. Once the CONTINUE_FLAG is set, the program will continue.

A PAGE byte can be set to read through pages in the flash memory. Once the PAGE is set to a integer between 0 and 0x1000, 4096 bytes of data will be read off the flash and stored in SDRAM where it can be read from the FLASH_DATA_ADDR. Once the PAGE is incremented a new block of data will be read and loaded into SDRAM. This can be repeated for all data block on the flash storage.

## Usage
<span style="color:red;"><b>NOTE: This program is only to be used with XD0007_MB_V0.6B and XD0007_MB_V0.6G1 board revisions. Using it on incompatible boards my result in damage to the device and/or bodily injury.</b></span>

It is built in python and can be executed in terminal with the following arguments:

| Arg                               | Description                                                   |
| --------------------------------- | ------------------------------------------------------------- |
| -v --verbose                      | Prints verbose output                                         |
| -i --inf <<i>file_path</i>>       | Define the input file path for the flash memory binary file   |
| -o --out <<i>file_path</i>>       | Define the output file path for the flash memory binary file<br/>If not defined, it will not dump the flash memory |
| -u --upload <<i>file_path</i>>    | Upload FW from specified BIN file                             |
| -d --download <<i>file_path</i>>  | Download FW to specified BIN file                             |
| -r --reflasher <<i>file_path</i>> | (<i>optional</i>) Define the reflasher.bin FW file path.<br/>If not defined, it will assume reflasher.bin is in your current working directory. |
| -l --level <<i>value</i>>         | Set the level indicator value. Value can be HEX, INT or percentage (<i>0x0 = FULL, 0x40000 = EMPTY</i>) |
| -e --extract <<i>file_path</i>> <<i>image_dir</i>> | Extract the images and battery data from the flash binary file|
| -c --compile <<i>file_path</i>> <<i>image_dir</i>> | Compile images and battery data to a flash binary file        |


Requires python verison 3.10.10 and pyswd library.

### Examples

Dump the flash memory
> python3 reflasher.py -o flash_dump.bin

Upload to the flash memory
> python3 reflasher.py -i flash_upload.bin

Set the juice level value to full
> python3 reflasher.py -l 0


