
#include "main.h"
#include <stdio.h>
#include <stdint.h>
/**
 * @brief  Main program.
 */
#define LED_PIN GPIO_PIN_5
#define LED_GPIO GPIOA

#define BUFFER_SIZE 4096
int page[1];
int write_flag[1];
uint8_t buffer[BUFFER_SIZE];
__IO uint32_t FlashID = 0;

int main(void)
{
	/* LED Setup */
	GPIO_Init(LED_GPIO, LED_PIN, GPIO_MODE_OUTPUT_PP);
	Delay(100);
	GPIO_Off(LED_GPIO, LED_PIN);
	
	sFLASH_Init();
	
	while(1){
		FlashID = sFLASH_ReadID();
		if(FlashID != 0) break;
	}
	
	if(FlashID == sFLASH_GD25Q80_ID){
		volatile int tmp_page = -1;
		while(1){
			if(tmp_page != page[0]){
				GPIO_On(LED_GPIO, LED_PIN);
				tmp_page = page[0];
				uint32_t addr = page[0] * BUFFER_SIZE;
				sFLASH_ReadBuffer(buffer, addr, BUFFER_SIZE);
				GPIO_Off(LED_GPIO, LED_PIN);
			}
		}
	}else{
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
