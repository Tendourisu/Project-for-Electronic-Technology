#include "Car_main.h"
#include "include.h"


#include "stdlib.h"

#define WAY_Flag 0		//赛道选择，1:黑底白线	0:白底黑线
#define SPEED 650

Car Target_V; // 目标转速
Car ENC_V;	  // 实际转速
Car Moto_PWM; // 控制电机计算出的PWM
int excep = 0;
int stat = 0;
//0:forward
//1:right
//2:left

int count;
#define CONS 7
float E_V = 0.0;
int32_t car_V;
sensor Car_sensor;
uint8_t Car_all;

uint16_t Dis = 0.0;
char txt[128];


void Car_main(void)
{
	
	LED_Init();						//初始化LED	
	KEY_Init();						//初始化按键
	OLED_Init();    				//OLED初始化
	OLED_CLS();						//清屏
	uart_init(USART_2,115200);		//初始化串口
	uart_init(USART_3,115200);		//初始化串口
	//Encoder_Init_TIM2();			//编码器初始化
	Encoder_Init_TIM3();			//编码器初始化
	Encoder_Init_TIM4();			//编码器初始化
	MotorInit();					//电机初始化
	sensor_init();                  //光电传感器初始化
	count = 0;
	while(1)
	{
	Car_sensor.a = Read_sensor(sensor1);
	Car_sensor.b = Read_sensor(sensor4);
	Car_sensor.c = Read_sensor(sensor3);
	Car_sensor.d = Read_sensor(sensor2);
	Dis = Get_Distance_1();
		Car_all = ((Car_sensor.a & 1) << 3) | ((Car_sensor.b & 1) << 2) | ((Car_sensor.c & 1) << 1) | ((Car_sensor.d & 1) << 0);
		
		E_V = (Car_sensor.a * 1.5 + Car_sensor.b * 1.2) - (Car_sensor.c * 1.2 + Car_sensor.d * 1.5);
		
	if (Car_all == 0x00 && excep == 0)
	{
		stat = 0;
	}
	else if(Car_all == 0x0f && excep == 0)
	{
		excep = 1;
		count = 0;
		OLED_CLS();
	}
	else if ((E_V > 1.5 || E_V == 1.5) && excep == 0)
	{
		stat = 2;
	}
	else if ((E_V < -1.5 || E_V == -1.5) && excep == 0)
	{
		stat = 1;
	}
	else if (excep == 1){
		if (Car_all == 0x00){
			stat = 0;
			excep = 0;
		}
		else if (count < CONS && excep == 1){
			stat = 4;
		}
		else if (CONS < count && count < CONS*3 && excep == 1){
			stat = 3;
		}
		else if (3*CONS < count && count < CONS*4 && excep == 1){
			stat = 4;
		}
		else if (4*CONS < count && excep == 1){
			stat = 0;
		}
		else if (!(Car_all == 0x0f) && excep == 1){
			excep = 0;
			
			if (E_V > 1.5 || E_V == 1.5){
				stat = 4;
			}
			else if (E_V < -1.5 || E_V == -1.5){
				stat = 3;
			}
			else{
				stat = 0;
			}
		}
	}
	
	if (Dis < 6 && excep != 2){
		excep = 2;
	}
	
	if (excep == 2){
		if (stat == 5 && stat != 6){
			stat = 6;
		}		
		if (stat != 5 && stat != 6){
			stat = 5;
		}

	}
	
	if (stat == 0) // forward
	{
		Moto_PWM.L = SPEED;
		Moto_PWM.R = -SPEED;
		Moto_PWM.B = 0;
	}
	else if (stat == 1) // turn right
	{
		Moto_PWM.L = -300*E_V;
		Moto_PWM.R = -300*E_V;
		Moto_PWM.B = -300*E_V;
	}
	else if (stat == 2) // turn left
	{
		Moto_PWM.L = -300*E_V;
		Moto_PWM.R = -300*E_V;
		Moto_PWM.B = -300*E_V;
	}
	else if (stat == 3) // turn right while excep == 1
	{
		Moto_PWM.L = SPEED;
		Moto_PWM.R = SPEED;
		Moto_PWM.B = SPEED;
	}
	else if (stat == 4) // turn left while excep == 1
	{
		Moto_PWM.L = -SPEED;
		Moto_PWM.R = -SPEED;
		Moto_PWM.B = -SPEED;
	}
	else if (stat == 5){
		Moto_PWM.L = 0;
		Moto_PWM.R = 0;
		Moto_PWM.B = 0;
		MotorCtrl3w(2000, -500, -500);
		delay_ms(2000);
	}
	else if (stat == 6){
		Moto_PWM.L = 0;
		Moto_PWM.R = 0;
		Moto_PWM.B = 0;
		MotorCtrl3w(SPEED, SPEED,SPEED);
		delay_ms(700);
		excep = 0;
	}
	// 输出限幅
	Moto_PWM.L = ((Moto_PWM.L) < (-6000) ? (-6000) : ((Moto_PWM.L) > (6000) ? (6000) : (Moto_PWM.L)));
	Moto_PWM.R = ((Moto_PWM.R) < (-6000) ? (-6000) : ((Moto_PWM.R) > (6000) ? (6000) : (Moto_PWM.R)));
	Moto_PWM.B = ((Moto_PWM.B) < (-6000) ? (-6000) : ((Moto_PWM.B) > (6000) ? (6000) : (Moto_PWM.B)));
	if (Moto_PWM.L ==0 && Moto_PWM.R ==0 && Moto_PWM.B ==0)
	{
		Moto_PWM.L = -SPEED;
		Moto_PWM.R = SPEED;
		Moto_PWM.B = 0;
		
	}
	Dis = Get_Distance_1();
	MotorCtrl3w(Moto_PWM.B, Moto_PWM.L,Moto_PWM.R);	// 最终电机输出

		OLED_Task();		//屏幕显示		
	}
	//
	//sprintf(txt, "Dis=%3d cm", Dis);
	//OLED_P8x16Str(0, 6, txt);   // 显示字符串
}
/*********************************************************************
* 函数名 ：void car_tim(void)
* 参  数 ：无
* 返回值 ：无
* 功  能 ：三轮小车 循线程序
* 说  明 ：assume that the signal for trajectory is 0
********************************************************************/
void car_tim(void)
{
	
#if	WAY_Flag
	Car_sensor.a = Read_sensor(sensor1);
	Car_sensor.b = Read_sensor(sensor4);
	Car_sensor.c = Read_sensor(sensor3);
	Car_sensor.d = Read_sensor(sensor2);
#else

	
	

#endif
	

#if	WAY_Flag
	if (Car_sensor.a == 1 && Car_sensor.b == 1 && Car_sensor.c == 1 && Car_sensor.d == 1)
	{
		car_V = -800;
	}
	else
	{
		if (abs(E_V) > 2) // 弯道
			car_V = 900;
		else // 直道
			car_V = 1200;
	}
	
#else

#endif
	

	//MotorCtrl3w(-600, 600,600);
	//Dis = Get_Distance();
}


void OLED_Task(void)
{
	//char txt[64];
	
	// 屏幕显示
	sprintf(txt, "%d %d %d %d E:%.1f", Car_sensor.a, Car_sensor.b, Car_sensor.c, Car_sensor.d, E_V);
	OLED_P6x8Str(0, 2, txt); // 字符串
	sprintf(txt, "L:%d R:%d B:%d ", Moto_PWM.L, Moto_PWM.R, Moto_PWM.B);
	OLED_P6x8Str(0, 3, txt); // 字符串
	sprintf(txt, "count: %d", count);
	OLED_P6x8Str(0, 4, txt); // 字符串
	sprintf(txt, "stat:%d,excep:%d\n",stat,excep);
	OLED_P6x8Str(0, 5, txt);
	sprintf(txt, "Dis=%3d cm", Dis);
	OLED_P8x16Str(0, 6, txt);   // 显示字符串
	delay_ms(70);
	count++;
}
