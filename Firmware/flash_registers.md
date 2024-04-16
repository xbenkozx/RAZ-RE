# Flash Registers
| REGISTER     | Address | Default Value  |
|--------------|---------|----------------| 
| FLASH_AC     | 0x40022000 | 0x0000 0030 |
| FLASH_KEY    | 0x40022004 | 0xXXXX XXXX |
| FLASH_OPTKEY | 0x40022008 | 0xXXXX XXXX |
| FLASH_STS    | 0x4002200C | 0x0000 0000 |
| FLASH_CTRL   | 0x40022010 | 0x0000 0080 |
| FLASH_ADD    | 0x40022014 | 0x0000 0000 |
| FLASH_OB     | 0x4002201C | 0x03FF FFFC |
| FLASH_WRP    | 0x40022020 | 0x0000 FFFF |
| FLASH_ECC    | 0x40022024 | 0x0000 0000 |

<br/>

# Flash Register Map
![register map](/images/reg_map.png)

<br/>

# FLASH_AC
| Bit Field | Name     | Description |
|-----------|----------|-------------|
| 5         | PRFTBFS  | Pre-fetch buffer status<br/>This bit indicates the state of the pre-fetch buffer<br/>0: The pre-fetch buffer is disabled.<br/>1: The pre-fetch buffer is enabled. |
| 4         | PRFTBFE  | The pre-fetch buffer is enabled</br>0: Disables the pre-fetch buffer.</br>1: Enables the pre-fetch buffer.|
| 3:2       | Reserved | Reserved,the reset value must be maintained |
| 1:0       | LATENCY  | Time delay<br/>These bits represent the ratio of the SYSCLK (system clock) cycle to the flash access time<br/>00: Zero periodic delay, when 0 < SYSCLK ≤ 18MHz<br/>01: A periodic delay, when 18MHz < SYSCLK ≤ 36MHz<br/>10: Two periodic delay, when 36MHz < SYSCLK ≤ 48MHz<br/>11: Reserved |

<br/>

# FLASH_STS
| Bit Field | Name     | Description |
|-----------|----------|-------------|
| 31:8      | Reserved | Reserved,the reset value must be maintaine |
| 7         | ECCERR   | ECC error<br/>Error reading FLASH, hardware set this to '1', write '1' to clear this state |
| 6         | Reserved | Reserved,the reset value must be maintained |
| 4         | WRPERR   | Write protection error<br/>When attempting to program a write protected flash address, hardware sets this to '1' and writing '1' clears this state. |
| 3         | Reserved | Reserved,the reset value must be maintained |
| 2         | PGERR    | Programming errors<br/>When trying to program to an address whose content is not '0xFFFF_FFFF', the hardware sets this to '1'. Writing '1' clears this state.<br/><i>Note: Before programming, the FLASH_CTRL.START bit must be cleared.</i> |
| 1         | Reserved | Reserved,the reset value must be maintained |
| 0         | BUSY     | Busy<br/>This bit indicates that a flash operation is in progress.This bit is set to '1' at the start of the flash operation; This bit is cleared to '0' at the end of the operation or when an error occurs. |

<br/>

# FLASH_CTRL

| Bit Field | Name | Description |
|-----------|-|-|
| 31:14 | Reserved  | Reserved,the reset value must be maintained |
| 13    | ECCERRITE | ECC error interrupt<br/>This bit allows interrupts to occur when the FLASH_STS.ECCERR bit changes to '1'.<br/>0: Forbid interruption.<br/>1: Interrupts are allowed. |
| 12    | EOPITE    | Allow operation completion interrupt.<br/>This bit allows an interrupt to be generated when the FLASH_STS.EOP bit becomes '1'.<br/>0: Forbid interruption.<br/>1: Interrupts are allowed. |
| 11    | Reserved  | Reserved,the reset value must be maintained |
| 10    | ERRITE    | Allow error status to be interrupted<br/>This bit allows interrupts in the event of Flash errors (when FLASH_STS.PGERR/ FLASH_STS<br/>WRPERR is set to '1').<br/>0: Forbid interruption.<br/>1: Interrupts are allowed. |
| 9     | OPTWE     | Allows option bytes to be written<br/>When the bit is' 1 ', programmatic manipulation of the option byte is allowed. When the correct key sequence is written to the FLASH_OPTKEY register, the bit is set to '1'.<br/>Software can clear this bit. |
| 8     | Reserved  | Reserved,the reset value must be maintained |
| 7     | LOCK      | Lock<br/>This bit can only be written as '1'.When the bit is' 1 ', Flash and FLASH_CTRL are locked. Hardware clears this bit to '0' after detecting a correct unlock sequence.<br/>After an unsuccessful unlock operation, this bit cannot be changed until the next system reset.|
| 6     | START     | Start<br/>An erase operation is triggered when the bit is' 1 '.This bit can only be set by software to '1' and cleared to '0' when FLASH_STS.BUSY changes to '1'. |
| 5     | OPTER     | Erase option bytes<br/>0: Disable option bytes erase mode;<br/>1: Enable option bytes erase mode. |
| 4     | OPTPG     | Program option bytes<br/>0: Disable option bytes program mode;<br/>1: Enable option bytes program mode. |
| 3     | Reserved  | Reserved,the reset value must be maintained |
| 2     | MER       | Mass erase<br/>0: Disable mass erase mode.<br/>1: Enable mass erase mode. |
| 1     | PER       | Page erase<br/>0: Disable mass erase mode.<br/>1: Enable mass erase mode. |
| 0     | PG        | Program<br/>0: Disable Program mode.<br/>1: Enable Program mode. |

