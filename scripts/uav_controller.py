from pycrazyswarm import Crazyswarm
from point import Point

class UAVController:
    
    def __init__(self):
        swarm = Crazyswarm(crazyflies_yaml="crazyflies.yaml")
        self.timeHelper = swarm.timeHelper
        self.uavs = swarm.allcfs.crazyflies
        self.s = len(self.uavs)
    

    def takeoff(self, uav_id, z=1, duration=1, sleep=0):
        
        self.uavs[uav_id].takeoff(z, duration)
        self.sleep(sleep)        


    def land(self, uav_id, z=0.05, duration=1, sleep=0):

        self.uavs[uav_id].land(z, duration)
        self.sleep(sleep)


    def getPosition(self, uav_id):

        return self.uavs[uav_id].position()


    def cmdVelocity(self, uav_id, x, y, z, w=0):

        self.uavs[uav_id].cmdVelocityWorld([x, y, z], w)
    

    def goTo(self, uav_id, point:Point, yaw=0, duration=1, sleep=0):

        self.uavs[uav_id].goTo(point.vector(), yaw, duration)
        self.sleep(sleep)

    def sleep(self, second):
        self.timeHelper.sleep(second)