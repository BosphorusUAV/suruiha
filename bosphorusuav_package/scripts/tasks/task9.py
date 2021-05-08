from point import Point
from uav import UAV, uavs, timeHelper
from formation import Formation
from swarm import Swarm, swarms

n = 9
for uav in uavs[n:]:
    uav.land(z=0, duration=2, sleep=0)

uavs = uavs[:9]

duration=10
d = 10
wait = 30

swarm0 = Swarm(uavs)

timeHelper.sleep(duration)

rotangles = [30 / 180, 45 / 180, -15 / 180,  90 / 180, -270 / 180]

swarm0.navigation(Point(0, 0, 1), relative=True)
swarm0.command(duration=5, inorder=0, sleep=10)

for ang in rotangles :
    x = ang / (15/180)
    for i in range((int)x):
        swarm0.rotation(15/180)
        swarm0.command(duration=5, inorder=0, sleep=0.05)
    timeHelper.sleep(wait)

for uav in uavs:
    uav.land(z=0, duration=2, sleep=0.5)
timeHelper.sleep(5)
