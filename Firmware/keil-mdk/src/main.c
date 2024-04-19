
#include "main.h"
#include <stdio.h>
#include <stdint.h>
/**
 * @brief  Main program.
 */
#define LED_PIN GPIO_PIN_5
#define LED_GPIO GPIOA

#define BUFFER_SIZE 4096
<<<<<<< HEAD
=======
volatile int page[1];
>>>>>>> 8444998287286b5181f8ce6164742ed808c94c9e
volatile int lvl_reset_flag[1];
volatile int continue_flag[1];
volatile int write_flag[1];
volatile int status[1];
uint8_t lvl_buffer[5];
uint8_t lvl_buffer_read[5];
uint8_t buffer[BUFFER_SIZE];
__IO uint32_t FlashID = 0;
uint32_t status_register;

uint8_t sFLASH_ReadRegister(uint8_t reg)
{
    uint8_t flashstatus = 0;

    /*!< Select the FLASH: Chip Select low */
    sFLASH_CS_LOW();

    /*!< Send "Read Status Register" instruction */
    sFLASH_SendByte(sFLASH_CMD_RDSR_1);
    
    flashstatus = sFLASH_SendByte(reg);

    /*!< Deselect the FLASH: Chip Select high */
    sFLASH_CS_HIGH();
		
		return flashstatus;
}

int main(void)
{
	
	/* LED Setup */
	GPIO_Init(LED_GPIO, LED_PIN, GPIO_MODE_OUTPUT_PP);
	Delay(100);
	GPIO_Off(LED_GPIO, LED_PIN);
	
	sFLASH_Init();
	
	while(1){
		Delay(100);
		FlashID = sFLASH_ReadID();
		if(FlashID != 0) break;
	}
	
	// Check Flash ID
	if(FlashID == sFLASH_GD25Q80_ID){
		status[0] = 1;
		
		// Wait for continue flag
		while(continue_flag[0] == 0)
			;
		continue_flag[0] = 0;
		
<<<<<<< HEAD
		// Reset continue flag
=======
		status[0] = 2;
>>>>>>> 8444998287286b5181f8ce6164742ed808c94c9e
		continue_flag[0] = 0;
		status[0] = 2;
		
		// If level reset flag is set, execute the level reset
		if(lvl_reset_flag[0] == 1){
			lvl_buffer[4] = 0xBB;
			sFLASH_EraseSector(0xf8000);
			sFLASH_WriteBuffer(lvl_buffer, 0xf8000, 5);
			status[0] = 3;
			
		}
		//for(int i=0; i<4096; i++){
			//buffer[i] = 0xe1;
		//}
		
<<<<<<< HEAD
		//Reset lvl_buffer to 0x0
		lvl_buffer[0] = 0x0;
		lvl_buffer[1] = 0x0;
		lvl_buffer[2] = 0x0;
		lvl_buffer[3] = 0x0;
		lvl_buffer[4] = 0x0;
		
		// Read the juice level
		sFLASH_ReadBuffer(lvl_buffer, 0xf8000, 5);
=======
		//Delay(10);
		sFLASH_ReadBuffer(lvl_buffer_read, 0xf8000, 5);
>>>>>>> 8444998287286b5181f8ce6164742ed808c94c9e
		
		volatile int tmp_page = -1;
		
		// If the write flag is set, initialize write
		if(write_flag[0] == 1){
<<<<<<< HEAD
			// Reset write flag
			write_flag[0] = 0; 
			// Erase all flash memory, getting read for writing data
			sFLASH_EraseBulk(); 
			
			// Set status to 5. This will be used when wait for data to be written to buffer
			status[0] = 5;
			for(uint32_t i=0; i<256; i++){ // For each block
				//Wait for status to be set to 4 (or anything else)
				while(status[0] == 5) ; 
				GPIO_On(LED_GPIO, LED_PIN);
				//Calculate the flash memory address to be written
				uint32_t addr = i * BUFFER_SIZE;
				// Write the block of data to flash
				sFLASH_WriteBuffer(buffer, addr, BUFFER_SIZE); 
				// Set status to 5 so that it will wait for next data to be written to buffer
				status[0] = 5; 
				GPIO_Off(LED_GPIO, LED_PIN);
			}
		}else{
			status[0] = 5;
			for(uint32_t i=0; i<256; i++){
				//Wait for status to be set to 4 (or anything else)
				while(status[0] == 5) ; 
				GPIO_On(LED_GPIO, LED_PIN);
				//Calculate the flash memory address to be read
				uint32_t addr = i * BUFFER_SIZE;
				// Read the block of data from flash
				sFLASH_ReadBuffer(buffer, addr, BUFFER_SIZE); 
				// Set status to 5 so that it will wait for next data to be read from buffer
				status[0] = 5;
				GPIO_Off(LED_GPIO, LED_PIN);
=======
			write_flag[0] = 0;
			sFLASH_EraseBulk();
			Delay(10);
			status[0] = 5;
			for(uint32_t i=0; i<256; i++){
				while(status[0] == 5) ;
				GPIO_On(LED_GPIO, LED_PIN);
				uint32_t addr = i * BUFFER_SIZE;
				sFLASH_WriteBuffer(buffer, addr, BUFFER_SIZE);
				status[0] = 5;
				GPIO_Off(LED_GPIO, LED_PIN);
			}
			//sFLASH_EraseBulk();
			//Delay(10);
			//while(1){
				//if(tmp_page != page[0]){
					//status[0] = 4;
					//GPIO_On(LED_GPIO, LED_PIN);
					//tmp_page = page[0];
					//uint32_t addr = page[0] * BUFFER_SIZE;
					//sFLASH_WriteBuffer(buffer, addr, BUFFER_SIZE);
					//for(int i=0; i<16; i++){
						//int offset = (i * 256);
						//uint32_t sector_addr = addr + offset;
						//pointer = sector_addr;
						//Delay(1000);
						
					//}
					//sFLASH_ReadBuffer(buffer, addr, BUFFER_SIZE);
					//status[0] = 5;
					//GPIO_Off(LED_GPIO, LED_PIN);
				//}
				
			//}
		}else{
			while(1){
				if(tmp_page != page[0]){
					status[0] = 6;
					GPIO_On(LED_GPIO, LED_PIN);
					tmp_page = page[0];
					uint32_t addr = page[0] * BUFFER_SIZE;
					sFLASH_ReadBuffer(buffer, addr, BUFFER_SIZE);
					GPIO_Off(LED_GPIO, LED_PIN);
					status[0] = 7;
				}
>>>>>>> 8444998287286b5181f8ce6164742ed808c94c9e
			}
		}
	}else{
		// If there is an error reading the Flash ID, pulse the light 3 times for 1 second delay
		GPIO_On(LED_GPIO, LED_PIN);
		Delay(1000);
		GPIO_Off(LED_GPIO, LED_PIN);
		Delay(1000);
		GPIO_On(LED_GPIO, LED_PIN);
		Delay(1000);
		GPIO_Off(LED_GPIO, LED_PIN);
		Delay(1000);
		GPIO_On(LED_GPIO, LED_PIN);
		Delay(1000);
		GPIO_Off(LED_GPIO, LED_PIN);
		while(1)
			;
	}
}
void Delay(volatile uint32_t count)
{
	volatile uint32_t t_delay = count * 0x500;
	for (; t_delay >0; t_delay--);
}
void GPIO_Off(GPIO_Module *GPIOx, uint16_t Pin) {  GPIO_SetBits(GPIOx, Pin); }
void GPIO_On(GPIO_Module* GPIOx, uint16_t Pin) { GPIO_ResetBits(GPIOx, Pin); }
void GPIO_Init(GPIO_Module* GPIOx, uint16_t Pin, uint32_t GpioMode) {
    GPIO_InitType GPIO_InitStructure;

    /* Check the parameters */
    assert_param(IS_GPIO_ALL_PERIPH(GPIOx));

    /* Enable the GPIO Clock */
    if (GPIOx == GPIOA)
    {
        RCC_EnableAPB2PeriphClk(RCC_APB2_PERIPH_GPIOA, ENABLE);
    }
    else if (GPIOx == GPIOB)
    {
        RCC_EnableAPB2PeriphClk(RCC_APB2_PERIPH_GPIOB, ENABLE);
    }
    else if (GPIOx == GPIOC)
    {
        RCC_EnableAPB2PeriphClk(RCC_APB2_PERIPH_GPIOC, ENABLE);
    }
    else if (GPIOx == GPIOF)
    {
        RCC_EnableAPB2PeriphClk(RCC_APB2_PERIPH_GPIOF, ENABLE);
    }
    else
    {
        return;
    }

    /* Configure the GPIO pin */
    if (Pin <= GPIO_PIN_ALL)
    {
        GPIO_InitStruct(&GPIO_InitStructure);
        GPIO_InitStructure.Pin = Pin;
        GPIO_InitStructure.GPIO_Mode = GpioMode;
        GPIO_InitPeripheral(GPIOx, &GPIO_InitStructure);
    }
}


/* Assert failed function by user.
 * @param file The name of the call that failed.
 * @param line The source line number of the call that failed.
 */
#ifdef USE_FULL_ASSERT
void assert_failed(const uint8_t* expr, const uint8_t* file, uint32_t line)
{
    while (1)
    {
    }
}
#endif // USE_FULL_ASSERT

/**
 * @}
 */
