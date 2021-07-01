from os import remove
from cflib.crazyflie.commander import Commander
from math import sqrt, log, exp
from time import time

MAX_VELOCITY = 0.3
TARGET_THRESHOLD = 0.05

class UAVController:   
    
    def __init__(self, motion_commander:Commander):
        self.mc = motion_commander
        
        self.addTarget(0, 0, 0, 0)


    def removeTarget(self):

        self.target_is_reached = True

    def addTarget(self, x, y, z, yaw=0, duration=2):

        self.targetx = x
        self.targety = y
        self.targetz = z
        self.targetw = yaw

        self.target_is_reached = False

        self.commandTime = time()
        self.duration = duration

    def isThereTarget(self):
        return not self.target_is_reached

    def isSettled(self):
        
        if self.isThereTarget():
            
            if  (abs(self.targetx - self.locx) < TARGET_THRESHOLD) and\
                (abs(self.targety - self.locy) < TARGET_THRESHOLD) and\
                (abs(self.targetz - self.locz) < TARGET_THRESHOLD):

                self.removeTarget()
        
        return not self.isThereTarget()

    def control(self):

        if self.isSettled():

            self.positioning(
                self.targetx,
                self.targety,
                self.targetz, 
                self.targetw
            )
        
        else:

            self.move(
                self.targetx,
                self.targety,
                self.targetz, 
                self.targetw,
                max(self.duration - (time() - self.commandTime), 0.1)
            )
        
            print(f'remaining time: {max(self.duration - (time() - self.commandTime), 0.1)} second\n\n')


    def land(self, duration=2):
        self.addTarget(
            self.locx,
            self.locy,
            0.1,
            self.locw,
            duration=duration
        )


    def setVelocity(self, x, y, z, yaw=0):
 
        self.mc.start_linear_motion(x, y, z, yaw)
        

    def locationTuner(self, locx, locy, locz, yaw):

        self.locx = locx
        self.locy = locy
        self.locz = locz
        self.locw = yaw

        print(f'estimated position: [{self.locx}, {self.locy}, {self.locz}, {self.locw}]')

    
    def move(self, x, y, z, yaw=0, duration=2):
        
        print('MOVING')
        print(f'target position:    [{x}, {y}, {z}, {yaw}]')
        
        self.velx = self.linearVelocity(x - self.locx, duration)
        self.vely = self.linearVelocity(y - self.locy, duration)
        self.velz = self.linearVelocity(z - self.locz, duration)
        self.velw = self.linearVelocity(yaw - self.locw, 0.1)
        
        print(f'velocity:           [{self.velx}, {self.vely}, {self.velz}, {self.velw}]')

        self.setVelocity(self.velx, self.vely, self.velz, self.velw)


    def positioning(self, x, y, z, yaw=0):

        print('POSITIONING')
        print(f'target position:    [{x}, {y}, {z}, {yaw}]')
        
        self.velx = self.logaritmicVelocity(x - self.locx)
        self.vely = self.logaritmicVelocity(y - self.locy)
        self.velz = self.logaritmicVelocity(z - self.locz)
        self.velw = self.logaritmicVelocity(yaw - self.locw)
        
        print(f'velocity:           [{self.velx}, {self.vely}, {self.velz}, {self.velw}]')

        self.setVelocity(self.velx, self.vely, self.velz, self.velw)

    def linearVelocity(self, dist,t):
        if dist == 0:
            return 0
        return min(MAX_VELOCITY, 2*abs(dist)/t) * dist / abs(dist)


    def logaritmicVelocity(self, dist):
        if dist == 0:
            return 0
        return min(MAX_VELOCITY, self.tanh(abs(dist))) * dist / abs(dist)

    def tanh(self, z):
        return (exp(z) - exp(-z)) / (exp(z) + exp(-z))

    