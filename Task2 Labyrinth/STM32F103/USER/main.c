// 包含所有头文件
#include "include.h"
#include "Car_main.h"


uint16_t Distance_1 = 0.0;
uint16_t Distance_2 = 0.0;
sensor Car_sensors;
char text[128];

int main(void)
{
	//-----------------------系统初始化配置----------------------------
	HAL_Init();			  // 初始化HAL库
	SystemClock_Config(); // 设置时钟9倍频,72M
	delay_init(72);		  // 初始化延时函数
	JTAG_Set(SWD_ENABLE); // 打开SWD接口 可以利用主板的SWD接口调试
	//-----------------------------------------------------------------
	uart_init(USART_3, 115200);			//初始化串口    连接LQMV4视觉模块  
	uart_init(USART_2, 115200);			//初始化串口    蓝牙接口
	LED_Init();			// LED初始化
	OLED_Init();		// OLED初始化   
	OLED_Show_LQLogo(); // 显示LOGO
	delay_ms(500);		// 延时等待
	OLED_CLS();			// 清屏
	OLED_P8x16Str(20, 0, "test");
	Ultrasonic_Init();
	sensor_init();                  //光电传感器初始化
//===================================================================

	while (1)
	{
		Car_sensors.a = Read_sensor(sensor1);
		Car_sensors.b = Read_sensor(sensor4);
		Car_sensors.c = Read_sensor(sensor3);
		Car_sensors.d = Read_sensor(sensor2);
		Distance_1 = Get_Distance_1();
		Distance_2 = Get_Distance_2();
		sprintf(text, "%d %d %d %d %d %d\n", Car_sensors.a, Car_sensors.b, Car_sensors.c, Car_sensors.d, Distance_1, Distance_2);
		
		uart_SendBuf(&USART3_Handler, (uint8_t*)text);
		
		OLED_CLS();
		OLED_P6x8Str(0, 3, text); // 字符串		
		
		delay_ms(10);
		
	}
}

