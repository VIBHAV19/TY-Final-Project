import RPi.GPIO as GPIO
import time
import thread

#TODO: This should be done once only
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Arm:
    pinList = {'claw': 20, 'linear': 21, 'height': 16}
    servos = {}
    
    def __init__(self):
        for i in self.pinList:
            GPIO.setup(self.pinList[i], GPIO.OUT)
            
            #Setup PWM 50Hz
            self.servos[i] = [GPIO.PWM(self.pinList[i], 50), 70]
            self.servos[i][0].start(7)
    
    def moveTowards(self, servo_id, pos):
        if self.servos[servo_id][1] < pos:
            for i in range(self.servos[servo_id][1], pos):
                self.servos[servo_id][0].ChangeDutyCycle(i / 10)
                time.sleep(0.01)
        elif self.servos[servo_id][1] > pos:
            for i in range(self.servos[servo_id][1], pos, -1):
                self.servos[servo_id][0].ChangeDutyCycle(i / 10)
                time.sleep(0.01)
        
        self.servos[servo_id][1] = pos
    
    
    def sweepServo(self, servo_id, pos):
        th = threading.Thread(target = Arm.moveTowards, args = (self, servo_id, pos))
        th.start()
        return th
    
    def openClaw(self):
        self.sweepServo('claw', 60).join()
    
    def closeClaw(self):
        self.sweepServo('claw', 105).join()

    def armRestingPos(self):
        arm_a = self.sweepServo('linear', 70)
        arm_b = self.sweepServo('height', 70)
        arm_a.join()
        arm_b.join()
    
    def armReach(self):
        arm_a = self.sweepServo('linear', 105)
        arm_b = self.sweepServo('height', 105)
        arm_a.join()
        arm_b.join()

arm = Arm()
arm.closeClaw()
time.sleep(2)

if __name__ == "__main__":
    while True:
        arm.openClaw()
        arm.armReach()
        time.sleep(1)
        arm.closeClaw()
        time.sleep(1)
        arm.armRestingPos()
        time.sleep(1)
        arm.openClaw()

"""
currPos1=7
currPos2=8
pinList={'claw':20,'linear':21,'height':16}
servos={}

for i in pinList:
    GPIO.setup(pinList[i],GPIO.OUT)
    servos[i]=GPIO.PWM(pinList[i],50)
    servos[i].start(7)

def closeClaw():
    for i in range(60,105):
        servos['claw'].ChangeDutyCycle(i/10)
        time.sleep(0.025)

def openClaw():
    servos['claw'].ChangeDutyCycle(6)

#TODO: Simultaneous both servos
def arm_resting_pos():
    global currPos1, currPos2
    if(currPos1<7):
        for i in range(currPos1*10,70,1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=7):
        for i in range(currPos1*10,70,-1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos1=7
    
    if(currPos2<7):
        for i in range(currPos2*10,70,1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=7):
        for i in range(currPos2*10,70,-1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos2=7

def arm_reach():
    global currPos1, currPos2
    if(currPos1<10.5):
        for i in range(currPos1*10,105,1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=10.5):
        for i in range(currPos1*10,105,-1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos1=10
    
    if(currPos2<7):
        for i in range(currPos2*10,70,1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=7):
        for i in range(currPos2*10,70,-1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos2=10

openClaw()
arm_resting_pos()

time.sleep(1)

arm_reach()
closeClaw()

time.sleep(1)

arm_resting_pos()

time.sleep(2)

openClaw()
"""

'''
> servos['height'].ChangeDutyCycle(4)
>>> servos['linear'].ChangeDutyCycle(3)
>>> servos['linear'].ChangeDutyCycle(12)
>>> servos['linear'].ChangeDutyCycle(11)
>>> servos['height'].ChangeDutyCycle(4)
>>> servos['height'].ChangeDutyCycle(4)
>>> servos['height'].ChangeDutyCycle(5)
>>> servos['height'].ChangeDutyCycle(3)
>>> servos['height'].ChangeDutyCycle(4)
>>> servos['claw'].ChangeDutyCycle(3)
>>> servos['claw'].ChangeDutyCycle(5)
>>> servos['claw'].ChangeDutyCycle(11)
>>> servos['linear'].ChangeDutyCycle(7)
>>> servos['height'].ChangeDutyCycle(8)
'''

