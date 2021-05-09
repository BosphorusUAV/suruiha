from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms
import numpy as np

n = 9
for uav in uavs[n:]:
    uav.land(z=0, duration=0, sleep=0)

uavs = uavs[:9]

duration = 5
d = 10
wait = 3

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

rotangles = [(np.pi) / 3, (np.pi) / 4, - (np.pi) / 6,  (np.pi) / 2, - 3 * (np.pi) / 2]

swarm0.changeFormation(
    formation_type='ucgen',
    uav_distance=1,
    center=Point(None, None, 1)
)
swarm0.command(duration = 5, inorder=0, sleep = 5)

for ang in rotangles :
    x = ang / ((np.pi) / 36)
    if x > 0:
        for i in range(abs(int(x))):
            swarm0.rotation(((np.pi) / 36))
            swarm0.command(duration=0.2, inorder=0, sleep=0.2)
            timeHelper.sleep(wait)
    else :
        for i in range(abs(int(x))):
            swarm0.rotation(-((np.pi) / 36))
            swarm0.command(duration=0.2, inorder=0, sleep=0.2)
            timeHelper.sleep(wait)

swarm0.navigation(Point(0,0,-1) ,relative = True)
swarm0.command(duration=d, inorder=0, sleep = d)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0)
timeHelper.sleep(5)
