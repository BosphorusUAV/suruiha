from cflib.crazyflie.commander import Commander
from math import sqrt, log

MAX_VELOCITY = 1

def multidimensionalSpeed(currx, curry, currz, tarx, tary, tarz, velocity):
    relx = tarx-currx
    rely = tary-curry
    relz = tarz-currz
    speedvec = sqrt((relx * relx) + (rely * rely) + (relz * relz))
    duration = speedvec / velocity
    return relx/duration, rely/duration, relz/duration

class UAVController(Commander):
    
    
    def __init__(self, crazyflie=None):
        super().__init__(crazyflie)

    
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

        self.send_velocity_world_setpoint(x, y, z, yaw)
        

    def locationTuner(self, locx, locy, locz):

        self.locx = locx
        self.locy = locy
        self.locz = locz

        
    def positioning(self, x, y, z):
        
        self.velx = self.calculateVelocity(x - self.locx, 0.1)
        self.vely = self.calculateVelocity(y - self.locy, 0.1)
        self.velz = self.calculateVelocity(z - self.locz, 0.1)
        
        self.setVelocity(self.velx, self.vely, self.velz)

    def calculateVelocity(dist,t):
        return min(MAX_VELOCITY, 2*dist/t)