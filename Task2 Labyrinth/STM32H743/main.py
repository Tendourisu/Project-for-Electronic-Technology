"""
巡线+踢球融合程序：先巡线，检测到小球面积达标后切换至踢球模式
"""
# 导入必要模块
import sensor, image, time, display
from pyb import Pin, Timer, LED, UART
from pid import PID
from LQ_Module import motor, Enc_AB

# -------------------------- 全局参数配置 --------------------------
# 模式标志位：0-巡线模式，1-踢球模式
mode = 0
excep = 0
Dis_L = 20
Dis_R = 20
stat = 0
count = 0            # 全局计数器，默认初始为0
CONS = 12            # 常量 CONS 的默认值
CLOSE = 12
FAR = 25


# 电机初始化
motor1 = motor(timer=4, chl=1, freq=10000, pin_pwm="P7", pin_io="P22") # left -> right
motor2 = motor(timer=4, chl=2, freq=10000, pin_pwm="P8", pin_io="P23") # right -> left
motor3 = motor(timer=4, chl=3, freq=10000, pin_pwm="P9", pin_io="P24") # back -> forward


# 编码器初始化
Enc1 = Enc_AB(Timer(12, freq=5), Enc_A="P21", Enc_B="P27")
Enc2 = Enc_AB(Timer(13, freq=5), Enc_A="P29", Enc_B="P28")
Enc3 = Enc_AB(Timer(14, freq=5), Enc_A="P26", Enc_B="P25")

encoder_valueL = 0
encoder_valueR = 0
encoder_valueB = 0


# 串口初始化（用于通信）
uart = UART(3, 115200)

def main():
    global CLOSE, stat
    global FAR, Dis_L, Dis_R
    time.sleep_ms(100)
    if uart.any():                              # 如果接收到任何消息
        receive = uart.read().decode().strip()  # 将接收到的消息提取出来
        receive = receive.splitlines()[-1]
        numbers = list(map(int, receive.split()))
        if len(numbers) != 6:
            return
        Car_sensor1, Car_sensor2, Car_sensor3, Car_sensor4, Dis_L, Dis_R = numbers
    if stat == 0 and (Dis_L > FAR and Dis_R < CLOSE):
        stat = 0
    elif stat == 0 and (Dis_L < CLOSE and Dis_R < CLOSE):
        stat = 1
    elif stat == 1 and (Dis_L < CLOSE and Dis_R < CLOSE):
        stat = 1
    elif stat == 1 and (Dis_L > FAR and Dis_R < CLOSE):
        stat = 0
    elif stat == 0 and Dis_L > FAR and Dis_R > FAR:
        stat = 2
    elif stat == 2 and (Dis_L > FAR and Dis_R > FAR):
        stat = 2
    elif stat == 2 and Dis_R < CLOSE and Dis_L > FAR:
        stat = 0
    if stat == 0:
        motor2.run(2600)     # 直行
        motor3.run(-2400)
        motor1.run(0)
        print(stat)
        if Dis_R > 8: #微调
            motor2.run(2600+400)     # 偏右一点
            motor3.run(-2400)
            motor1.run(0)
        if Dis_R < 8:
            motor2.run(2600)     # 偏左一点
            motor3.run(-2400-600)
            motor1.run(0)
    elif stat == 1:
        motor2.run(-2400) # 左转
        motor3.run(-2400)
        motor1.run(-2400)
        print(stat)
    elif stat == 2:
        print(stat, Dis_L, Dis_R)
        motor2.run(2400)     # 直行
        motor3.run(-2400)
        motor1.run(0)
        time.sleep_ms(1000)
        motor2.run(2400) # 右转一点
        motor3.run(2400)
        motor1.run(2400)
        time.sleep_ms(730)
        motor2.run(2400)     # 直行
        motor3.run(-2400)
        motor1.run(0)
        time.sleep_ms(1100)
        motor2.run(0)     # 停
        motor3.run(0)
        motor1.run(0)
        time.sleep_ms(500)

    # if CLOSE > Dis:
    #     motor1.run(-4000)
    #     motor2.run(3000)
    #     motor3.run(0)
    #     time.sleep_ms(50)
    # elif Dis > FAR:
    #     motor1.run(-3000)
    #     motor2.run(4000)
    #     motor3.run(0)
    #     time.sleep_ms(50)
    # else:
    #     motor1.run(-3000)
    #     motor2.run(3000)
    #     motor3.run(0)
    #     time.sleep_ms(50)
clock = time.clock()
#motor2.run(2600)     # 直行
#motor3.run(-2400)
#motor1.run(0)
#time.sleep_ms(1300)
#motor2.run(2400) # 右转一点
#motor3.run(2400)
#motor1.run(2400)
#time.sleep_ms(700)
#motor2.run(2400)     # 直行
#motor3.run(-2400)
#motor1.run(0)
#time.sleep_ms(1000)
while True:
    clock.tick()
    main()


