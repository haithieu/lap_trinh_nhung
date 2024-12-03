import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

TRIG = 23  
ECHO = 24  
khoang_cach = 40

IN1 = 5
IN2 = 6
ENA = 12 
IN3 = 13
IN4 = 19
ENB = 26  
SENSOR_1 = 27  # GPIO27
SENSOR_2 = 17  # GPIO17
SENSOR_3 = 22  # GPIO22
SENSOR_4 = 18  # GPIO18


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

pwm = GPIO.PWM(25, 50)
pwm.start(0)


GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_1, GPIO.IN)
GPIO.setup(SENSOR_2, GPIO.IN)
GPIO.setup(SENSOR_3, GPIO.IN)
GPIO.setup(SENSOR_4, GPIO.IN)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwm_left = GPIO.PWM(ENA, 1000)  # Táº§n sá»‘ 1kHz
pwm_right = GPIO.PWM(ENB, 1000)  # Táº§n sá»‘ 1kHz
pwm_left.start(0)
pwm_right.start(0)

def xe_tien():
    pwm_left.ChangeDutyCycle(40)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm_right.ChangeDutyCycle(40)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def xe_lui():
    pwm_left.ChangeDutyCycle(50)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_right.ChangeDutyCycle(50)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def xe_re_phai():
    pwm_left.ChangeDutyCycle(35)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_right.ChangeDutyCycle(65)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def xe_re_trai():
    pwm_left.ChangeDutyCycle(65)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm_right.ChangeDutyCycle(35)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def dung_xe():
    pwm_left.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm_right.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def xe_tranh_vat_ben_trai():
    xe_re_trai()
    time.sleep(1)
    xe_tien()
    time.sleep(0.35)
    xe_re_phai()
    time.sleep(1)
    xe_tien()
    time.sleep(0.35)
    xe_re_phai()
    time.sleep(1.2)
    while True:
        sensor_1_state = GPIO.input(SENSOR_1)
        sensor_2_state = GPIO.input(SENSOR_2)
        sensor_3_state = GPIO.input(SENSOR_3)
        sensor_4_state = GPIO.input(SENSOR_4)
        if sensor_1_state == 0 and sensor_2_state == 0 and sensor_3_state == 0 and sensor_4_state == 0:
            xe_tien()
	    time.sleep(0.5)
        else:
            break
def xe_tranh_vat_ben_phai():
    xe_re_phai()
    time.sleep(1)
    xe_tien()
    time.sleep(0.35)
    xe_re_trai()
    time.sleep(1)
    xe_tien()
    time.sleep(0.35)
    xe_re_trai()
    time.sleep(1.2)
    while True:
        sensor_1_state = GPIO.input(SENSOR_1)
        sensor_2_state = GPIO.input(SENSOR_2)
        sensor_3_state = GPIO.input(SENSOR_3)
        sensor_4_state = GPIO.input(SENSOR_4)
        if sensor_1_state == 0 and sensor_2_state == 0 and sensor_3_state == 0 and sensor_4_state == 0:
            xe_tien()
		time.sleep(0.5)
        else:
            break
    
def do_khoang_cach():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        bat_dau = time.time()

    while GPIO.input(ECHO) == 1:
        ket_thuc = time.time()
    thoi_gian = ket_thuc - bat_dau
    khoang_cach = (thoi_gian * 34300) / 2  
    return khoang_cach

def goc_servo(goc):
    if goc < 0:
        goc = 0
    elif goc > 180:
        goc = 180
    chu_ky = 2 + (goc / 18)  
    chu_ky = max(2, min(12, chu_ky))
    GPIO.output(25, True)
    pwm.ChangeDutyCycle(chu_ky)
    time.sleep(0.5)
    GPIO.output(25, False)
    pwm.ChangeDutyCycle(0)

def phat_hien_vat():
    kc_truoc = do_khoang_cach()
    if kc_truoc < 20:
        print("Dung xe")
        dung_xe()

        # Xoay servo sang trai kiem tra
        goc_servo(45)
        time.sleep(1)
        kc_phai = do_khoang_cach()
        print(f"Khoang cach ben phai: {kc_phai:.2f} cm")

        # Xoay servo sang phai kiem tra
        goc_servo(135)
        time.sleep(1)
        kc_trai = do_khoang_cach()
        print(f"Khoang cach ban trai: {kc_trai:.2f} cm")

        # Xoay servo ve vi tri ban dau
        goc_servo(90)
        time.sleep(1)

        if kc_trai > 20 and kc_phai > 20:
            xe_tranh_vat_ben_trai()
            print("Xe re trai")
        
        elif kc_trai > 20:
            xe_tranh_vat_ben_trai()
            print("Xe re trai")

        elif kc_phai > 20:
            xe_tranh_vat_ben_phai()
            print("Xe re phai")

def do_line():

        sensor_1_state = GPIO.input(SENSOR_1)
        sensor_2_state = GPIO.input(SENSOR_2)
        sensor_3_state = GPIO.input(SENSOR_3)
        sensor_4_state = GPIO.input(SENSOR_4)

        if sensor_1_state == 0 and sensor_2_state == 1 and sensor_3_state == 1 and sensor_4_state == 0:
            xe_tien()
        elif sensor_1_state == 0 and sensor_2_state == 0 and sensor_3_state == 1 and sensor_4_state == 0:
            xe_re_phai()
        elif sensor_1_state == 0 and sensor_2_state == 0 and sensor_3_state == 1 and sensor_4_state == 1:
            xe_re_phai()
        elif sensor_1_state == 0 and sensor_2_state == 0 and sensor_3_state == 0 and sensor_4_state == 1:
            xe_re_phai()
        elif sensor_1_state == 0 and sensor_2_state == 1 and sensor_3_state == 0 and sensor_4_state == 0:
            xe_re_trai()
        elif sensor_1_state == 1 and sensor_2_state == 1 and sensor_3_state == 0 and sensor_4_state == 0:
            xe_re_trai()
        elif sensor_1_state == 1 and sensor_2_state == 0 and sensor_3_state == 0 and sensor_4_state == 0:
            xe_re_trai()
        else:
            dung_xe()



try:
    time.sleep(1)
    goc_servo(90)
    time.sleep(1)
  
    while True:
        sensor_1_state = GPIO.input(SENSOR_1)
        sensor_2_state = GPIO.input(SENSOR_2)
        sensor_3_state = GPIO.input(SENSOR_3)
        sensor_4_state = GPIO.input(SENSOR_4)
        if sensor_1_state == 1 or sensor_2_state == 1 or sensor_3_state == 1 or sensor_4_state == 1:
            phat_hien_vat()
        do_line()
       