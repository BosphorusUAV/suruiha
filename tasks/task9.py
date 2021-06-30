from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms
import numpy as np

n = 8
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:n]


swarm0 = Swarm(uavs)

timeHelper.sleep(10)

rotangles = [(np.pi) / 2, - (np.pi) / 4, 3 * (np.pi) / 4, - 3 * (np.pi) / 2 , (np.pi) / 3]

swarm0.changeFormation(
    formation_type='kare',
    uav_distance=1,
    center=Point(None, None, 1)
)
swarm0.command(duration = 2.5, inorder=0, sleep = 15)

for ang in rotangles :
    x = ang / ((np.pi) / 36)
    if int(x) > 0:
        for i in range(abs(int(x))):
            swarm0.rotation(((np.pi) / 36))
            swarm0.command(duration=0.2, inorder=0, sleep=0.2)
        timeHelper.sleep(15)
    else :
        for i in range(abs(int(x))):
            swarm0.rotation(-((np.pi) / 36))
            swarm0.command(duration=0.2, inorder=0, sleep=0.2)
        timeHelper.sleep(15)

swarm0.navigation(Point(0,0,-1) ,relative = True)
swarm0.command(duration=2.5, inorder=0, sleep = 2.5)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)
timeHelper.sleep(5)
