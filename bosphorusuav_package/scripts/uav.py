from pycrazyswarm import Crazyswarm
from point import Point

second = 2
class Timer:
    def __init__(self):
        self.timeHelper = swarm.timeHelper
    def sleep(self, duration):
        self.timeHelper.sleep(duration*second)

swarm = Crazyswarm(crazyflies_yaml="crazyflies.yaml")
timeHelper = Timer()
uavs = swarm.allcfs.crazyflies
s = len(uavs)

class UAV:
    
    def __init__(self, id):
        self.uav = uavs[id]
        self.takeoff(z=0.1)


    def takeoff(self, z=1, duration=1, sleep=0):
        
        self.uav.takeoff(z, duration*second)
        self.sleep(sleep)        


    def land(self, z=0.05, duration=1, sleep=0):

        self.uav.land(z, duration*second)
        self.sleep(sleep)


    def getPosition(self):

        return Point(vector=self.uav.position())


    def cmdVelocity(self, x, y, z, w=0):

        self.uav.cmdVelocityWorld([x, y, z], w)
    

    def goTo(self, point:Point, yaw=0, relative=False, duration=1, sleep=0):

        self.uav.goTo(point.vector(), yaw, duration*second, relative=relative)
        self.sleep(sleep)

    def sleep(self, duration):
        timeHelper.sleep(duration*second)

uavs = [UAV(i) for i in range(s)]
