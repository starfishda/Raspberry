import RPi.GPIO as GPIO
import time
import smbus
import threading

I2C_CH = 1
BH1750_DEV_ADDR = 0x23

CONT_H_RES_MODE     = 0x10
CONT_H_RES_MODE2    = 0x11
CONT_L_RES_MODE     = 0x13
ONETIME_H_RES_MODE  = 0x20
ONETIME_H_RES_MODE2 = 0x21
ONETIME_L_RES_MODE  = 0x23

pin = 18 # PWM pin num 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
cnt = 0

'''
 조도값 읽는 함수
'''
def readIlluminance():
  i2c = smbus.SMBus(I2C_CH)
  luxBytes = i2c.read_i2c_block_data(BH1750_DEV_ADDR, CONT_H_RES_MODE, 2)
  lux = int.from_bytes(luxBytes, byteorder='big')
  i2c.close()
  return lux

'''
 1초에 한번씩 돌면서 조도값 출력
'''
def readIlluminanceThread():
  while True:
    print('{0} lux'.format(readIlluminance()))
    if (readIlluminance() < 500):
      p.ChangeDutyCycle(1)
      print("angle : 1")
    else:
      p.changeDutyCycle(0)
    time.sleep(1)

print('starting BH1750')
print('Press Enter key to exit')
# 쓰레드 생성
thd = threading.Thread(target=readIlluminanceThread)
# 쓰레드를 데몬으로 설정
thd.daemon = True
# 쓰레드 시작
thd.start()
# 키 입력 대기, 엔터 키가 입력이 되면 다음으로 넘어가서 'done'을 출력하고 프로그램 종료
input()
print('done')
p.stop()

GPIO.cleanup()