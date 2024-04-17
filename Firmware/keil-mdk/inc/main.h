/*****************************************************************************
 * Copyright (c) 2024, Ben Kozlowski
 *
 * ****************************************************************************
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 2 as published by the Free Software Foundation.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * ****************************************************************************/

/**
 * @file main.h
 * @author Ben Kozlowski
 * @version v1.0.0
 *
 * @copyright Copyright (c) 2024, Ben Kozlowski.
 */
#ifndef __MAIN_H__
#define __MAIN_H__

#ifdef __cplusplus
extern "C" {
#endif


#include "n32g031_it.h"
#include "spi_flash.h"

void Delay(volatile uint32_t count);
void GPIO_Init(GPIO_Module* GPIOx, uint16_t Pin, uint32_t GpioMode);
void GPIO_Off(GPIO_Module *GPIOx, uint16_t Pin);
void GPIO_On(GPIO_Module* GPIOx, uint16_t Pin);

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H__ */
/**
 * @}
 */

/**
 * @}
 */

/**
 * @}
 */
