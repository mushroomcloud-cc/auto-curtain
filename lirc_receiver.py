#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

# 红外输出电压 board 2脚
# gnd 低电平 board 6脚
# 使用BCM的26号脚，board的37号脚
# 使用board编码的7号脚为in1  11号为in2
# BCM in1 4, in2 17
Motor_control_in1= 4
Motor_control_in2= 17
PIN = 26

# 这是初始化红外及输出脚
def inital_lirc():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Motor_control_in1,GPIO.OUT)
	GPIO.setup(Motor_control_in2,GPIO.OUT)
	GPIO.output(Motor_control_in1, 0)
	GPIO.output(Motor_control_in2, 0)
	GPIO.setup(PIN,GPIO.IN,GPIO.PUD_UP)
	print("irm test start...")

# 判断红外信号内容，7是开，9是关,64是加，21是保存，25是减少
def lirc(value):
	if value==7:
		print("openning")
		GPIO.output(Motor_control_in1, 1) 
		GPIO.output(Motor_control_in2, 0)
	elif value==9:
		print("closing")
		GPIO.output(Motor_control_in1, 0) 
		GPIO.output(Motor_control_in2, 1)
	elif value==64:
		print("add")
		#这部分添加加时间的代码
	elif value==25:
		print("reduce")
		#这部分添加减少时间的代码
	elif value==21:
		print("write")
		#这部分添加确认保存的代码		
	else:
		print("No this code")

		
		
# 这部分是主程序。
inital_lirc()
while True:
	if GPIO.input(PIN) == 0:
		count = 0
		while GPIO.input(PIN) == 0 and count < 200:
			count += 1
			time.sleep(0.00006)

		count = 0
		while GPIO.input(PIN) == 1 and count < 80:
			count += 1
			time.sleep(0.00006)

		idx = 0
		cnt = 0
		data = [0,0,0,0]
		for i in range(0,32):
			count = 0
			while GPIO.input(PIN) == 0 and count < 15:
				count += 1
				time.sleep(0.00006)

			count = 0
			while GPIO.input(PIN) == 1 and count < 40:
				count += 1
				time.sleep(0.00006)

			if count > 8:
				data[idx] |= 1<<cnt
			if cnt == 7:
				cnt = 0
				idx += 1
			else:
				cnt += 1
		if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
			# this print is check the code value
			print(data[2])
			# 判断红外信号
			lirc(data[2])
