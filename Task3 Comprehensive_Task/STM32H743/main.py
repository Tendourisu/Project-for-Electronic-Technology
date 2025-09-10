"""
巡线+踢球融合程序：先巡线，检测到小球面积达标后切换至踢球模式
"""
# 导入必要模块
import sensor, image, time, display
from pyb import Pin, Timer, LED, UART
from pid import PID
from LQ_Module import motor, Enc_AB
from image import SEARCH_EX, SEARCH_DS
# -------------------------- 全局参数配置 --------------------------
# 模式标志位：0-巡线模式，1-踢球模式
mode = 0
excep = 0
Dis = 20
stat = 0
count = 0            # 全局计数器，默认初始为0
CONS = 12            # 常量 CONS 的默认值
TRN = True
KICK = False
OBS = True
#踢球相关参数
ball_threshold = [(24, 86, 22, 71, -8, 57)]# 小球颜色阈值
line_threshold = [(77, 100, -36, 7, -24, 27)] # 地线阈值
arrow_threshold = [(23, 73, -64, -22, -6, 80)] # 绿箭阈值
# goal_threshold = [       # 球门颜色阈值
#     (27, 62, -61, -37, 9, 59)
# ]
ball_size_threshold = 750  # 小球面积阈值（超过此值切换模式）
# size_target = 23000          # 踢球模式目标面积

# # PID控制器初始化
# pid_ball = PID(p=11, i=0, d=0, imax=50)     # 寻球PID
# pid_goal = PID(p=21, i=0, d=0, imax=50)     # 寻门PID
# pid_speed = PID(p=0.09, i=0, d=0, imax=50)  # 速度PID

# 全局变量

# step = 0                # 踢球模式步骤
# turnflag = 0            # 小球丢失转向标志

# -------------------------- 硬件初始化 --------------------------
# 显示屏初始化
lcd = display.SPIDisplay()
lcd.clear()
pic = image.Image("/pic0.jpg")
lcd.write(pic)

# # 按键初始化（K0控制启动/停止）
# button_0 = Pin('P30', Pin.IN, Pin.PULL_UP)

# 电机初始化
motor1 = motor(timer=4, chl=1, freq=10000, pin_pwm="P7", pin_io="P22")
motor2 = motor(timer=4, chl=2, freq=10000, pin_pwm="P8", pin_io="P23")
motor3 = motor(timer=4, chl=3, freq=10000, pin_pwm="P9", pin_io="P24")

# 编码器初始化
Enc1 = Enc_AB(Timer(12, freq=5), Enc_A="P21", Enc_B="P27")
Enc2 = Enc_AB(Timer(13, freq=5), Enc_A="P29", Enc_B="P28")
Enc3 = Enc_AB(Timer(14, freq=5), Enc_A="P26", Enc_B="P25")

encoder_valueL = 0
encoder_valueR = 0
encoder_valueB = 0

# 摄像头初始化
# sensor.reset()
# sensor.set_hmirror(True)
# sensor.set_pixformat(sensor.RGB565)
# sensor.set_framesize(sensor.LCD)  # 80x60
# sensor.skip_frames(time=2000)
# sensor.set_auto_gain(False)
# sensor.set_auto_whitebal(False)

# Reset sensor
sensor.reset()

# # Set sensor settings
# sensor.set_contrast(1)
# sensor.set_gainceiling(16)
# # Max resolution for template matching with SEARCH_EX is QQVGA
# sensor.set_framesize(sensor.QQVGA)
# # You can set windowing to reduce the search image.
# #sensor.set_windowing(((640-80)//2, (480-60)//2, 80, 60))
# sensor.set_pixformat(sensor.GRAYSCALE)


sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.LCD)  # 80x60
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_hmirror(True)
sensor.set_vflip(True)
# Load template.
# Template should be a small (eg. 32x32 pixels) grayscale image.
templateL = image.Image("L.pgm")

# 串口初始化（用于通信）
uart = UART(3, 115200)



# -------------------------- 辅助函数 --------------------------
def find_max(blob_all):
    max_size=0
    for blob in blob_all:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            mac_size = blob[2]*blob[3]
    return max_blob

def handle_kick_direction(img):
    # 处理踢球逻辑
    global mode
    # 识别小球、矩形和线
    balls = img.find_blobs(ball_threshold, pixels_threshold=50, area_threshold=50, merge=True)
    rects = img.find_blobs(line_threshold, pixels_threshold=50, area_threshold=50, merge=True)
    if balls:
        ball = find_max(balls)
        img.draw_rectangle(ball.rect())
    else:
        return
    if rects:
        rect = find_max(rects)
        img.draw_rectangle(rect.rect())
    else:
        return

    ball_center = (ball.x() + 0.5 * ball.w(), ball.y() + 0.5 * ball.h())
    rect_center = (rect.x() + 0.5 * rect.w(), rect.y() + 0.5 * rect.h())

    if (abs(ball_center[0] - 60) > 2) or (abs(rect_center[0] - ball_center[0]) > 2):
        if abs(ball_center[0] - 60) > 2:
            if ball_center[0] - 60 > 2:
                motor2.run(1200)
                motor3.run(1200)
                motor1.run(1200)
                time.sleep_ms(50)
            else:
                motor2.run(-1200)
                motor3.run(-1200)
                motor1.run(-1200)
                time.sleep_ms(50)
        elif abs(rect_center[0] - 60) > 2:
            if rect_center[0] - 64 > 2:
                motor2.run(0)
                motor3.run(0)
                motor1.run(-3000)
                time.sleep_ms(50)
            else:
                motor2.run(0)
                motor3.run(0)
                motor1.run(3000)
                time.sleep_ms(50)
    else:
        print("*****")
        motor2.run(2400)
        motor3.run(-2100)
        motor1.run(0)
        time.sleep_ms(500)
        print("*****")
        mode = 4 # start kicking



def start_kicking(img):
    global KICK, OBS
    global mode
    global count
    # 初始化速度变量
    speed_L = 0
    speed_R = 0
    speed_B = 0

    arrows = img.find_blobs(arrow_threshold, pixels_threshold=50, area_threshold=50, merge=True)
    if arrows:
        arrow = find_max(arrows)
        img.draw_rectangle(arrow.rect())
        arrow_center = (arrow.x() + 0.5 * arrow.w(), arrow.y() + 0.5 * arrow.h())
    else:
        arrow_center = (60, 80)




    if abs(arrow_center[0] - 60) > 2:
        if arrow_center[0] - 60 > 2: # turn right
            motor2.run(2400 + 100)
            motor3.run(-2000 + 100)
            motor1.run(0)
            time.sleep_ms(50)
            count = count + 1
        elif arrow_center[0] - 60 < -2: # turn left
            motor2.run(2400)
            motor3.run(-2800)
            motor1.run(0)
            time.sleep_ms(50)
            count = count + 1
    else:
        motor2.run(2400)
        motor3.run(-2100)
        motor1.run(0)
        time.sleep_ms(50)
        count = count + 1
        print(count)
        if (count > 85):
            motor2.run(-2400)
            motor3.run(2400)
            motor1.run(0)
            time.sleep_ms(600)
            motor2.run(2400 + 300) # turn right
            motor3.run(2400 - 200)
            motor1.run(0)
            time.sleep_ms(300)
            mode = 0 # as usual
            KICK = True
            OBS = False

def handle_line_tracking(img):
    """处理巡线逻辑（基于Car_sensor的方法）"""
    global mode, stat, excep, count, E_V, Car_all, Dis
    global encoder_valueB
    global encoder_valueL
    global encoder_valueR
    global OBS
    global TRN
    global KICK
    SPEED = 2200
   # 检测小球（判断是否切换模式）
    ball_blobs = img.find_blobs(ball_threshold, pixels_threshold=50, area_threshold=50, merge=True)
    if ball_blobs:
        ball_blob = find_max(ball_blobs)
        ball_area = ball_blob[2] * ball_blob[3]

        img.draw_rectangle(ball_blob[0:4], color=(0, 255, 0))  # 绿色框标记小球
        if ball_area > ball_size_threshold and KICK == False:
            mode = 3  # 切换至踢球模式
            return

    if uart.any():                              # 如果接收到任何消息
        receive = uart.read().decode().strip()  # 将接收到的消息提取出来
        receive = receive.splitlines()[-1]
        numbers = list(map(int, receive.split()))
        if len(numbers) != 5:
            return
        Car_sensor1, Car_sensor2, Car_sensor3, Car_sensor4, Dis = numbers
        Car_sensor3 = 1 - Car_sensor3
        Car_sensor4 = 1 - Car_sensor4
        E_V = (Car_sensor1 * 1.5 + Car_sensor2 * 1.2) - (Car_sensor3 * 1.2 + Car_sensor4 * 1.5)
    else:
        return
#    img.to_grayscale()

#    l = img.find_template(templateL, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))

#    if l:
#        img.draw_rectangle(l)
    #Car_sensor1 = (receive >> 3) & 1  # 取第4位（最高位）
    #Car_sensor2 = (receive >> 2) & 1  # 取第3位
    #Car_sensor3= (receive >> 1) & 1  # 取第2位
    #Car_sensor4 = receive & 1         # 取第1位（最低位）

    # 正常巡线逻辑（基于Car_sensor）
    # 计算偏差值E_V（模拟原C代码的传感器加权偏差）

    # 计算传感器状态组合值
    Car_all = ((Car_sensor1 & 1) << 3) | ((Car_sensor2 & 1) << 2) | ((Car_sensor3 & 1) << 1) | ((Car_sensor4 & 1) << 0)

    # 状态判断逻辑（按原 C 代码转换）
    if Car_all == 0x00  and excep == 0:
        stat = 0
    elif (E_V >= 1.5) and excep == 0:
        stat = 1
    elif (E_V <= -1.5) and excep == 0:
        stat = 2


#    if l and TRN == False:
#        stat = 4
#        TRN = True
#        print("****")

    if Dis < 12 and OBS == False:
        stat = 5
        OBS = True

    # 电机控制逻辑
    speed_L = 0
    speed_R = 0
    speed_B = 0

    if stat == 0:  # 直行
        speed_L = SPEED
        speed_R = -SPEED
        speed_B = 0
    elif stat == 1:  # 右转
        speed_L = -1000 * E_V
        speed_R = -1000 * E_V
        speed_B = -1000 * E_V
    elif stat == 2:  # 左转
        speed_L = -1000 * E_V
        speed_R = -1000 * E_V
        speed_B = -1000 * E_V
    elif stat == 3:  # 异常右转
        speed_L = SPEED
        speed_R = SPEED
        speed_B = SPEED
        motor2.run(speed_L)
        motor3.run(speed_R)
        motor1.run(speed_B)
        time.sleep_ms(1000)
        motor2.run(2400)
        motor3.run(-2400)
        motor1.run(0)
        time.sleep_ms(500)
        speed_L = 0
        speed_R = 0
        speed_B = 0
    elif stat == 4:  # 异常左转
        speed_L = -SPEED     #左转
        speed_R = -SPEED
        speed_B = -SPEED*1.5
        motor2.run(speed_L)
        motor3.run(speed_R)
        motor1.run(speed_B)
        time.sleep_ms(400)
        motor2.run(2400)    #直行
        motor3.run(-2400)
        motor1.run(0)
        time.sleep_ms(850)
        motor2.run(2400)    #右转
        motor3.run(2400)
        motor1.run(2400*1.5)
        time.sleep_ms(400)
        motor2.run(2400)    #直行
        motor3.run(-2400)
        motor1.run(0)
        time.sleep_ms(2750)
        motor2.run(2400)   #右转
        motor3.run(2400)
        motor1.run(2400*1.5)
        time.sleep_ms(400)
        motor2.run(2400)   #直行
        motor3.run(-2400)
        motor1.run(0)
        time.sleep_ms(1250)
        motor2.run(-2400)   #左转
        motor3.run(-2400)
        motor1.run(-2400*1.5)
        time.sleep_ms(300)
    elif stat == 5:  # 避障停止/恢复
        # motor2.run(4200)
        # motor3.run(-1400)
        # motor1.run(400)
        # time.sleep_ms(2000)
        # speed_L = SPEED
        # speed_R = SPEED
        # speed_B = SPEED
        # motor2.run(speed_L)
        # motor3.run(speed_R)
        # motor1.run(speed_B)
        # time.sleep_ms(1500)
        # speed_L = 0
        # speed_R = 0
        # speed_B = 0
        while True:
            if abs(encoder_valueB) >= 1137:

                break
            encoder_valueB += Enc1.Get()
            encoder_valueL += Enc2.Get()
            encoder_valueR += Enc3.Get()

            motor1.run(-6000)
            motor2.run(2000)
            motor3.run(1000)

            print(encoder_valueB, encoder_valueL, encoder_valueR)
            print("****")
            time.sleep_ms(100)



        motor1.run(-2000)
        motor2.run(-2000)
        motor3.run(-2000)
        time.sleep_ms(1500)

        OBS = True
        mode = 0

    # 速度限幅
    speed_L = max(-6000, min(6000, speed_L))
    speed_R = max(-6000, min(6000, speed_R))
    speed_B = max(-6000, min(6000, speed_B))

    # 防止全零状态（原C代码逻辑）
    if speed_L == 0 and speed_R == 0 and speed_B == 0:
        speed_L = SPEED
        speed_R = -SPEED
        speed_B = 0
    #print(speed_L, speed_R, speed_B, stat, excep)
    # 执行电机控制

#    speed_L = 2400
#    speed_R = -2000
#    speed_B = 0

    motor2.run(speed_L)
    motor3.run(speed_R)
    motor1.run(speed_B)
    # print(stat)

def handle_kick_ball(img):
    """踢球模式占位函数：原有详细实现被注释，可在需要时恢复完整逻辑。"""
    # 原始实现在文件中已被注释。这里提供最小占位以避免未定义错误。
    # 在真实踢球模式下，应恢复文件中注释的完整算法。
    global mode
    # 简单行为：保持停止状态并返回
    motor2.run(0)
    motor3.run(0)
    motor1.run(0)
    KICK = True



# -------------------------- 主循环 --------------------------
clock = time.clock()
while True:

    clock.tick()
    img = sensor.snapshot()

    arrows = img.find_blobs(arrow_threshold, pixels_threshold=50, area_threshold=50, merge=True)
    if arrows:
        arrow = find_max(arrows)
        img.draw_rectangle(arrow.rect())
    # 模式切换逻辑
    if mode == 3:
        handle_kick_direction(img)
    elif mode == 4:
        start_kicking(img)
    else:
        handle_line_tracking(img)
    #motor2.run(0)
    #motor3.run(0)
    #motor1.run(0)
    lcd.write(img)

