from pycrazyswarm import Crazyswarm
from point import Point

swarm = Crazyswarm(crazyflies_yaml="crazyflies.yaml")
timeHelper = swarm.timeHelper
uavs = swarm.allcfs.crazyflies
s = len(uavs)

class UAV:
    
    def __init__(self, id):
        self.uav = uavs[id]
        self.takeoff(z=0.1)


    def takeoff(self, z=1, duration=1, sleep=0):
        
        self.uav.takeoff(z, duration)
        self.sleep(sleep)        


    def land(self, z=0.05, duration=1, sleep=0):

        self.uav.land(z, duration)
        self.sleep(sleep)


    def getPosition(self):

        return Point(vector=self.uav.position())


    def cmdVelocity(self, x, y, z, w=0):

        self.uav.cmdVelocityWorld([x, y, z], w)
    

    def goTo(self, point:Point, yaw=0, relative=False, duration=1, sleep=0):

        self.uav.goTo(point.vector(), yaw, duration, relative=relative)
        self.sleep(sleep)

    def sleep(self, second):
        timeHelper.sleep(second)

uavs = [UAV(i) for i in range(s)]
