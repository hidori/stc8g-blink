#ifdef __INTELLISENSE__
#define __SDCC_SYNTAX_FIX
#endif

#include "fw_hal.h"

#define LED_GPIO_SetMode GPIO_P3_SetMode
#define LED_GPIO_PIN GPIO_Pin_1

#define LED_PIN P31
#define LED_WAIT 500

int main(void)
{
	LED_GPIO_SetMode(LED_GPIO_PIN, GPIO_Mode_Output_PP);

	while (1)
	{
		LED_PIN = SET;
		SYS_Delay(LED_WAIT);

		LED_PIN = RESET;
		SYS_Delay(LED_WAIT);
	}
}
