import sensor, image, time, display
from pyb import Pin, Timer, LED, UART
from pid import PID
from LQ_Module import motor, Enc_AB
from image import SEARCH_EX, SEARCH_DS
import time
import math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
sensor.set_hmirror(True)
sensor.set_vflip(True)

clock = time.clock()

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# Please use the TAG36H11 tag family for this script - it's the recommended tag family to use.


# -------------------------- 硬件初始化 --------------------------
# 显示屏初始化
lcd = display.SPIDisplay()
lcd.clear()
pic = image.Image("/pic0.jpg")
lcd.write(pic)

# 电机初始化
motor1 = motor(timer=4, chl=1, freq=10000, pin_pwm="P7", pin_io="P22")
motor2 = motor(timer=4, chl=2, freq=10000, pin_pwm="P8", pin_io="P23") #L
motor3 = motor(timer=4, chl=3, freq=10000, pin_pwm="P9", pin_io="P24") #R

while True:
    SPEED_L= 0
    SPEED_R= 0
    SPEED_B= 0
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags():
        SPEED_L= 0
        SPEED_R= 0  
        SPEED_B= 0
        img.draw_rectangle(tag.rect(), color=(255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
        tag_center = (tag.cx(), tag.cy())
        tag_area = tag.w() * tag.h()
        print_args = (tag.family(), tag.id(), (180 * tag.rotation()) / math.pi)
        print(tag_center, tag_area)
        if abs(tag_center[0] - 80) > 2:
            if tag_center[0] - 80 > 2: # turn right
                SPEED_B += 0
                SPEED_L += 400
                SPEED_R += 400
            elif tag_center[0] - 80 < -2: # turn left
                SPEED_B += 0
                SPEED_L += -400
                SPEED_R += -400
        if tag_area < 700: # move forward
            SPEED_B += 0
            SPEED_L += 2400
            SPEED_R += -2400
        elif tag_area > 1000: # move backward      
            SPEED_B += 0
            SPEED_L += -2400
            SPEED_R += 2400


    print(SPEED_B, SPEED_L, SPEED_R)
    motor2.run(SPEED_L)
    motor3.run(SPEED_R)
    motor1.run(SPEED_B)
    lcd.write(img)
    time.sleep_ms(50)