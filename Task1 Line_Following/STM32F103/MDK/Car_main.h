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
    idle = 0, // 0:空闲-原地直立
    run,      // 1:自由跑
    barrier,  // 2:看到障碍物
    find_R_way, // 3:正常循迹
    find_delay, // 4:正常循迹
    find_L_way, // 5:正常循迹
    find_delay_V, // 6:正常循迹
    find_way,   //7
    leisure   // 暂时不用
} State_car;

typedef struct
{
    int8_t a;
    int8_t b;
    int8_t c;
    int8_t d;
} sensor;


typedef struct {
	char flag;     //标志位
	int  L_V;  //左轮速度
	int  R_V;  //右轮速度
	int  B_V;  //后轮速度
	
} Color_V;

void Car_main(void);
void car_tim(void);
void SYS_Task(void);
void OLED_Task(void);

#endif
