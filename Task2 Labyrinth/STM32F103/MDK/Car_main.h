#ifndef _CAR_MAIN_H
#define _CAR_MAIN_H
#include "stdint.h"

typedef struct
{
    int32_t L;
    int32_t R;
    int32_t B;
} Car;

typedef enum
{
    idle = 0, // 0:����-ԭ��ֱ��
    run,      // 1:������
    barrier,  // 2:�����ϰ���
    find_R_way, // 3:����ѭ��
    find_delay, // 4:����ѭ��
    find_L_way, // 5:����ѭ��
    find_delay_V, // 6:����ѭ��
    find_way,   //7
    leisure   // ��ʱ����
} State_car;

typedef struct
{
    int8_t a;
    int8_t b;
    int8_t c;
    int8_t d;
} sensor;


typedef struct {
	char flag;     //��־λ
	int  L_V;  //�����ٶ�
	int  R_V;  //�����ٶ�
	int  B_V;  //�����ٶ�
	
} Color_V;

void Car_main(void);
void car_tim(void);
void SYS_Task(void);
void OLED_Task(void);

#endif
