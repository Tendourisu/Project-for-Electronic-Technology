// ��������ͷ�ļ�
#include "include.h"
#include "Car_main.h"


uint16_t Distance_1 = 0.0;
uint16_t Distance_2 = 0.0;
sensor Car_sensors;
char text[128];

int main(void)
{
	//-----------------------ϵͳ��ʼ������----------------------------
	HAL_Init();			  // ��ʼ��HAL��
	SystemClock_Config(); // ����ʱ��9��Ƶ,72M
	delay_init(72);		  // ��ʼ����ʱ����
	JTAG_Set(SWD_ENABLE); // ��SWD�ӿ� �������������SWD�ӿڵ���
	//-----------------------------------------------------------------
	uart_init(USART_3, 115200);			//��ʼ������    ����LQMV4�Ӿ�ģ��  
	uart_init(USART_2, 115200);			//��ʼ������    �����ӿ�
	LED_Init();			// LED��ʼ��
	OLED_Init();		// OLED��ʼ��   
	OLED_Show_LQLogo(); // ��ʾLOGO
	delay_ms(500);		// ��ʱ�ȴ�
	OLED_CLS();			// ����
	OLED_P8x16Str(20, 0, "test");
	Ultrasonic_Init();
	sensor_init();                  //��紫������ʼ��
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
		OLED_P6x8Str(0, 3, text); // �ַ���		
		
		delay_ms(10);
		
	}
}

