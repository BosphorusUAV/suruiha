from cflib.crazyflie.commander import Commander
from math import sqrt, log

MAX_VELOCITY = 0.3

def multidimensionalSpeed(currx, curry, currz, tarx, tary, tarz, velocity):
    relx = tarx-currx
    rely = tary-curry
    relz = tarz-currz
    speedvec = sqrt((relx * relx) + (rely * rely) + (relz * relz))
    duration = speedvec / velocity
    return relx/duration, rely/duration, relz/duration

class UAVController:
    
    
    def __init__(self, motion_commander:Commander):
        self.mc = motion_commander

    
    def simple_move(self, x, y, z, yaw=0, velocity=0.2):
        
        self.velx, self.vely, self.velz = multidimensionalSpeed(
            self.locx,
            self.locy,
            self.locz,
            x,
            y,
            z,
            velocity
        )

        self.setVelocity(
            self.velx,
            self.vely,
            self.velz
        )


    def setVelocity(self, x, y, z, yaw=0):
 
        self.mc.start_linear_motion(x, y, z, yaw)
        

    def locationTuner(self, locx, locy, locz, yaw):

        self.locx = locx
        self.locy = locy
        self.locz = locz
        self.locyaw = yaw

        print(f'estimated position: [{self.locx}, {self.locy}, {self.locz}]')

    
    def move(self, x, y, z, yaw=0, duration=2):
        print(f'target position: [{x}, {y}, {z}]')
        
        self.velx = self.calculateVelocity(x - self.locx, duration)
        self.vely = self.calculateVelocity(y - self.locy, duration)
        self.velz = self.calculateVelocity(z - self.locz, duration)
        self.velyaw = self.calculateVelocity(yaw, self.locyaw, 0.1)
        
        print(f'velocity: [{self.velx}, {self.vely}, {self.velz}]')

        self.setVelocity(self.velx, self.vely, self.velz, self.velyaw)


    def positioning(self, x, y, z):
        print(f'target position: [{x}, {y}, {z}]')
        
        self.velx = self.calculateVelocity(x - self.locx, 0.1)
        self.vely = self.calculateVelocity(y - self.locy, 0.1)
        self.velz = self.calculateVelocity(z - self.locz, 0.1)
        
        print(f'velocity: [{self.velx}, {self.vely}, {self.velz}]')

        self.setVelocity(self.velx, self.vely, self.velz)

    def calculateVelocity(self, dist,t):
        if dist == 0:
            return 0
        return min(MAX_VELOCITY, 2*abs(dist)/t) * dist / abs(dist)